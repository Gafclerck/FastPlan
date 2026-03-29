from flask import Blueprint, render_template, redirect, flash, url_for, session
from app.blueprints.auth.auth import auth_required
from app.controllers.course_controller import CourseCtrl
from app.controllers.student_controller import StudentCtrl
from app.controllers.availability_controller import AvailabilityCtrl
from app.controllers.seance_controller import SeanceCtrl

bp = Blueprint("student", __name__, url_prefix="/student")

_DAYS = [
    {"value": 0, "label": "Lun"},
    {"value": 1, "label": "Mar"},
    {"value": 2, "label": "Mer"},
    {"value": 3, "label": "Jeu"},
    {"value": 4, "label": "Ven"},
    {"value": 5, "label": "Sam"},
    {"value": 6, "label": "Dim"},
]

def _get_current_student():
    user_id = session.get("user_id")
    role = session.get("role")
    if not user_id or role != "student":
        return None
    return StudentCtrl.get_student_by_id(int(user_id))

@bp.route("/")
@bp.route("/courses")
@auth_required
def courses():
    student = _get_current_student()
    if not student:
        flash("Veuillez vous connecter avec un compte étudiant.", "error")
        return redirect(url_for("auth.login"))
    courses = CourseCtrl.get_course_by_class_id(student.class_id)
    return render_template("student/courses.html", student=student, courses=courses)

@bp.route("/time_table")
@auth_required
def timetable():
    student = _get_current_student()
    if not student:
        flash("Veuillez vous connecter avec un compte étudiant.", "error")
        return redirect(url_for("auth.login"))

    slots = AvailabilityCtrl.get_time_slots()
    rows_map = {}
    for slot in slots:
        key = f"{slot.start_time.strftime('%H:%M')}-{slot.end_time.strftime('%H:%M')}"
        if key not in rows_map:
            rows_map[key] = {}
        rows_map[key][slot.day_of_week] = slot

    seances = SeanceCtrl.get_seance_by_class_id(student.class_id)
    seances_by_slot = {}
    for seance in seances:
        seances_by_slot[seance.slot_id] = seance

    return render_template(
        "student/timetable.html",
        student = student,
        days = _DAYS,
        seances_by_slot = seances_by_slot,
        rows_map = rows_map
    )