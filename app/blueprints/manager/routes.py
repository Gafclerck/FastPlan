import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from sqlalchemy import select, func
from app.controllers.class_controller import ClassCtrl
from app.controllers.course_controller import CourseCtrl
from app.controllers.seance_controller import SeanceCtrl
from app.controllers.prof_controller import ProfCtrl
from app.controllers.availability_controller import AvailabilityCtrl
from app.database import Database
from app.config import Config

bp = Blueprint("manager", __name__, url_prefix="",
                template_folder=os.path.join(Config.APP_DIR, "templates", "manager"))

_DAYS = [
    {"value": 0, "label": "Lun"},
    {"value": 1, "label": "Mar"},
    {"value": 2, "label": "Mer"},
    {"value": 3, "label": "Jeu"},
    {"value": 4, "label": "Ven"},
    {"value": 5, "label": "Sam"},
    {"value": 6, "label": "Dim"},
]

@bp.route("/dashboard", methods=["GET"])
def dashboard():
    engine = Database.get_engine()
    with engine.begin() as conn:
        totals = {
            "classes": conn.execute(select(func.count()).select_from(Database.class_table)).scalar() or 0,
            "profs": conn.execute(select(func.count()).select_from(Database.prof_table)).scalar() or 0,
            "students": conn.execute(select(func.count()).select_from(Database.student_table)).scalar() or 0,
            "courses": conn.execute(select(func.count()).select_from(Database.course_table)).scalar() or 0,
            "seances": conn.execute(select(func.count()).select_from(Database.seance_table)).scalar() or 0,
            "slots": conn.execute(select(func.count()).select_from(Database.time_slot_table)).scalar() or 0,
            "availabilities": conn.execute(select(func.count()).select_from(Database.availability_table)).scalar() or 0,
            "class_courses": conn.execute(select(func.count()).select_from(Database.class_course_table)).scalar() or 0,
        }

        state_rows = conn.execute(
            select(
                Database.class_seance_table.c.state,
                func.count().label("count"),
            ).group_by(Database.class_seance_table.c.state)
        ).all()
        seance_state_counts = {row.state: row.count for row in state_rows}

        recent_courses = conn.execute(
            select(
                Database.course_table.c.name.label("course_name"),
                Database.course_table.c.creation_date,
                Database.course_table.c.state,
                Database.course_table.c.duration,
                Database.user_table.c.name.label("prof_name"),
                Database.user_table.c.surname.label("prof_surname"),
            )
            .join(Database.prof_table, Database.course_table.c.prof_id == Database.prof_table.c.id)
            .join(Database.user_table, Database.user_table.c.id == Database.prof_table.c.id)
            .order_by(Database.course_table.c.creation_date.desc())
            .limit(6)
        ).all()

        recent_seances = conn.execute(
            select(
                Database.seance_table.c.date,
                Database.course_table.c.name.label("course_name"),
                Database.class_table.c.level.label("class_level"),
                Database.class_table.c.field.label("class_field"),
                Database.class_table.c.tag.label("class_tag"),
                Database.class_seance_table.c.state.label("seance_state"),
                Database.time_slot_table.c.day_of_week,
                Database.time_slot_table.c.start_time,
                Database.time_slot_table.c.end_time,
            )
            .join(Database.course_table, Database.course_table.c.id == Database.seance_table.c.course_id)
            .join(Database.class_seance_table, Database.seance_table.c.id == Database.class_seance_table.c.seance_id)
            .join(Database.class_table, Database.class_table.c.id == Database.class_seance_table.c.class_id)
            .join(Database.time_slot_table, Database.time_slot_table.c.id == Database.seance_table.c.slot_id)
            .order_by(Database.seance_table.c.date.desc())
            .limit(6)
        ).all()

    days_map = {d["value"]: d["label"] for d in _DAYS}
    return render_template(
        "dashboard.html",
        totals=totals,
        seance_state_counts=seance_state_counts,
        recent_courses=recent_courses,
        recent_seances=recent_seances,
        days_map=days_map,
    )

@bp.route("/timetable", methods=["GET", "POST"])
def timetable():
    classes = ClassCtrl.get_all()
    if not classes:
        flash("Aucune classe disponible.", "error")
        return render_template(
            "timetable.html",
            classes=[],
            classe=None,
            selected_class_id=None,
            days=_DAYS,
            time_rows=[],
            seances_by_slot={},
        )

    selected_id = classes[0].id
    if request.method == "POST":
        selected_id = request.form.get("class_id") or selected_id
    try:
        selected_id = int(selected_id)
    except (TypeError, ValueError):
        selected_id = classes[0].id

    classe = ClassCtrl.get_class_by_id(selected_id)
    if not classe:
        classe = classes[0]
        selected_id = classe.id

    slots = AvailabilityCtrl.get_time_slots()
    rows_map = {}
    for slot in slots:
        key = (slot.start_time, slot.end_time)
        if key not in rows_map:
            rows_map[key] = {}
        rows_map[key][slot.day_of_week] = slot

    time_rows = []
    for start_time, end_time in sorted(rows_map.keys()):
        label = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        time_rows.append({"label": label, "by_day": rows_map[(start_time, end_time)]})

    seances = SeanceCtrl.get_seance_by_class_id(selected_id)
    seances_by_slot = {}
    for row in seances:
        seances_by_slot.setdefault(row.slot_id, []).append(row)

    return render_template(
        "timetable.html",
        classes=classes,
        classe=classe,
        selected_class_id=selected_id,
        days=_DAYS,
        time_rows=time_rows,
        seances_by_slot=seances_by_slot,
    )

@bp.route("/creneaux", methods=["GET", "POST"])
def creneaux():
    profs = ProfCtrl.get_all()
    if not profs:
        flash("Aucun professeur disponible.", "error")
        return render_template(
            "prof_timetable.html",
            profs=[],
            prof=None,
            selected_prof_id=None,
            days=_DAYS,
            time_rows=[],
            seances_by_slot={},
        )

    selected_id = profs[0].id
    if request.method == "POST":
        selected_id = request.form.get("prof_id") or selected_id
    try:
        selected_id = int(selected_id)
    except (TypeError, ValueError):
        selected_id = profs[0].id

    prof = ProfCtrl.get_prof_by_id(selected_id)
    if not prof:
        prof = profs[0]
        selected_id = prof.id

    slots = AvailabilityCtrl.get_time_slots()
    rows_map = {}
    for slot in slots:
        key = (slot.start_time, slot.end_time)
        if key not in rows_map:
            rows_map[key] = {}
        rows_map[key][slot.day_of_week] = slot

    time_rows = []
    for start_time, end_time in sorted(rows_map.keys()):
        label = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        time_rows.append({"label": label, "by_day": rows_map[(start_time, end_time)]})

    seances = SeanceCtrl.get_seance_by_prof_id(selected_id)
    seances_by_slot = {}
    for seance in seances:
        seances_by_slot.setdefault(seance.slot_id, []).append(seance)

    return render_template(
        "prof_timetable.html",
        profs=profs,
        prof=prof,
        selected_prof_id=selected_id,
        days=_DAYS,
        time_rows=time_rows,
        seances_by_slot=seances_by_slot,
    )


@bp.route("/profs", methods=["POST", "GET"])
@bp.route("profs/add", methods=["POST", "GET"])
def professors():
    if request.method == "POST":
        try:
            ProfCtrl.create_professor(
                request.form.get("name"),
                request.form.get("surname"),
                request.form.get("email"),
                request.form.get("telephone"),
                request.form.get("speciality")
            )
            flash("Professor added successfully!", "success")
            return redirect(url_for(".professors"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for(".professors"))
    elif request.method == "GET":
        profs = ProfCtrl.get_all()
        return render_template("profs.html", profs=profs)

@bp.route("profs/prof/<prof_id>", methods=["POST", "GET"])
def professor(prof_id=None):
    if request.method == "POST":
        try:
            CourseCtrl.create(
                prof_id = prof_id,
                name = request.form.get("name"),
                duration = request.form.get("duration"),
                classes = request.form.getlist("classe"),
            )
            flash("Course added successfully !", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for(".professor", prof_id=prof_id))
    elif request.method == "GET":
        prof = ProfCtrl.get_prof_by_id(int(prof_id))
        courses = CourseCtrl.get_course_by_prof_id(prof_id)
        classes = ClassCtrl.get_all()
        return render_template("prof.html", prof = prof, prof_courses = courses, classes = classes)


@bp.route("/classes", methods=["POST", "GET"])
@bp.route("classes/add", methods=["POST", "GET"])
def classes():
    if request.method == "POST":
        try:
            ClassCtrl.create(
                level=request.form.get("level"),
                field=request.form.get("field"),
                academic_year=request.form.get("academic_year"),
                tag=request.form.get("tag")
            )
            flash("Class ajouté avec succes", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for(".classes"))
    elif request.method == "GET":
        classes = ClassCtrl.get_all()
        return render_template("classes.html", classes = classes)

@bp.route("classes/classe/<class_id>", methods=["POST", "GET"])
def classe(class_id=None):
    if request.method == "POST":
        try:
            ClassCtrl.add_course_to_class(
                class_id=class_id,
                course_id=request.form.get("classe"),
            )
            flash("Cours ajouté à la classe avec succès !", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for(".classe", class_id=class_id))
    elif request.method == "GET":
        classe = ClassCtrl.get_class_by_id(int(class_id))
        courses = CourseCtrl.get_course_by_class_id(class_id)
        all_courses = CourseCtrl.get_all()
        print(courses)
        print(courses)
        return render_template("classe.html", classe=classe, class_courses = courses, all_courses = all_courses)

@bp.route("classes/classe/<class_id>/timetable", methods=["GET", "POST"])
def classe_timetable(class_id=None):
    try:
        class_id = int(class_id)
    except (TypeError, ValueError):
        flash("Classe introuvable.", "error")
        return redirect(url_for(".classes"))

    classe = ClassCtrl.get_class_by_id(class_id)
    if not classe:
        flash("Classe introuvable.", "error")
        return redirect(url_for(".classes"))

    if request.method == "POST":
        try:
            SeanceCtrl.create(
                course_id=request.form.get("course_id"),
                slot_id=request.form.get("slot_id"),
                class_ids = request.form.getlist("class_ids")
            )
            flash("seance ajouter avec succes !", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for(".classe_timetable", class_id=class_id))

    slots = AvailabilityCtrl.get_time_slots()
    days_map = {d["value"]: d["label"] for d in _DAYS}

    rows_map = {} # on a les heures avec les slot cle(08-10h) valeue(de tous le jours)
    for slot in slots:
        key = (slot.start_time, slot.end_time)
        if key not in rows_map:
            rows_map[key] = {}
        rows_map[key][slot.day_of_week] = slot
    # print(rows_map)

    time_rows = []
    for start_time, end_time in sorted(rows_map.keys()):
        label = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        time_rows.append({"label": label, "by_day": rows_map[(start_time, end_time)]})
    # print(time_rows)
    slot_options = []
    for slot in slots: # exemple {"id":1 , "label": lun 08-10}
        day_label = days_map.get(slot.day_of_week, str(slot.day_of_week))
        label = f"{day_label} {slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}"
        slot_options.append({"id": slot.id, "label": label})
    # print(slot_options)
    seances = SeanceCtrl.get_seance_by_class_id(class_id)
    seances_by_slot = {}
    for row in seances:
        seances_by_slot.setdefault(row.slot_id, []).append(row)
    
    courses = CourseCtrl.get_course_by_class_id(class_id)
    classes = ClassCtrl.get_all()

    return render_template(
        "classe_timetable.html",
        classe=classe,
        days=_DAYS,
        time_rows=time_rows,
        seances_by_slot=seances_by_slot,
        courses=courses,
        classes=classes,
        slot_options=slot_options,
    )
