import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from app.blueprints.auth.auth import auth_requied
from app.controllers.prof_controller import ProfCtrl
from app.controllers.course_controller import CourseCtrl
from app.controllers.class_controller import ClassCtrl
from app.controllers.availability_controller import AvailabilityCtrl
from app.controllers.seance_controller import SeanceCtrl

bp = Blueprint("professor", __name__, url_prefix="/professor")

_DAYS = [
    {"value": 0, "label": "Lun"},
    {"value": 1, "label": "Mar"},
    {"value": 2, "label": "Mer"},
    {"value": 3, "label": "Jeu"},
    {"value": 4, "label": "Ven"},
    {"value": 5, "label": "Sam"},
    {"value": 6, "label": "Dim"},
]

def _get_current_prof():
    user_id = session.get("user_id")
    role = session.get("role")
    if not user_id or role != "professor":
        return None
    return ProfCtrl.get_prof_by_id(int(user_id))

@bp.route("/", methods=["POST", "GET"])
@bp.route("/courses", methods=["POST", "GET"])
@auth_requied
def courses():
    if request.method == "POST":
        return redirect(url_for("professor.courses"))
    elif request.method == "GET":
        prof = _get_current_prof()
        if not prof:
            flash("Veuillez vous connecter avec un compte professeur.", "error")
            return redirect(url_for("auth.login"))
        courses = CourseCtrl.get_course_by_prof_id(prof.id)
        return render_template("professor/courses.html", prof=prof, courses=courses)

@bp.route("/classes", methods=["GET"])
@auth_requied
def classes():
    prof = _get_current_prof()
    if not prof:
        flash("Veuillez vous connecter avec un compte professeur.", "error")
        return redirect(url_for("auth.login"))
    classes = ClassCtrl.get_classes_by_prof_id(prof.id)
    return render_template("professor/classes.html", prof=prof, classes=classes)


@bp.route("/availability", methods=["GET", "POST"])
@auth_requied
def availability():
    prof = _get_current_prof()
    if not prof:
        flash("Veuillez vous connecter avec un compte professeur.", "error")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        slot_ids = request.form.getlist("time_slot_id")
        try:
            slot_ids = [int(x) for x in slot_ids]
        except ValueError:
            flash("Sélection invalide.", "error")
            return redirect(url_for("professor.availability"))
        AvailabilityCtrl.set_availability(prof.id, slot_ids)
        flash("Disponibilités mises à jour.", "success")
        return redirect(url_for("professor.availability"))

    slots = AvailabilityCtrl.get_time_slots()
    checked_ids = set(AvailabilityCtrl.get_available_slot_ids(prof.id))

    rows_map = {}
    for slot in slots:
        key = (slot.start_time, slot.end_time)
        if key not in rows_map:
            rows_map[key] = {}
        rows_map[key][slot.day_of_week] = slot

    time_rows = []
    for start_time, end_time in sorted(rows_map.keys()):
        label = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
        time_rows.append(
            {
                "label": label,
                "by_day": rows_map[(start_time, end_time)],
            }
        )

    return render_template(
        "professor/availability.html",
        prof=prof,
        days=_DAYS,
        time_rows=time_rows,
        checked_ids=checked_ids,
    )

@bp.route("/time_table")
@auth_requied
def time_table():
    prof = _get_current_prof()
    if not prof:
        flash("Veuillez vous connecter avec un compte professeur.", "error")
        return redirect(url_for("auth.login"))

    slots = AvailabilityCtrl.get_time_slots()
    rows_map = {} # on a les heures avec les slot cle(08-10h) valeue(de tous le jours)
    for slot in slots:
        key = f"{slot.start_time.strftime("%H:%M")}-{slot.end_time.strftime("%H:%M")}"
        if key not in rows_map:
            rows_map[key] = {}
        rows_map[key][slot.day_of_week] = slot


    seances = SeanceCtrl.get_seance_by_prof_id(prof.id)
    print(seances)
    seances_by_slot = {}
    for seance in seances:
        seances_by_slot[seance.slot_id] = seance

    return render_template(
        "professor/prof_time_table.html",
        prof = prof,
        days = _DAYS,
        seances_by_slot = seances_by_slot,
        rows_map = rows_map,
        seances = seances
    )