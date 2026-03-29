from functools import wraps
from flask import Blueprint, render_template, request, redirect, flash, url_for, session
from app.controllers.auth_controller import AuthCtrl
from app.controllers.student_controller import StudentCtrl
from app.controllers.class_controller import ClassCtrl

bp = Blueprint("auth", __name__)

def auth_required(func):
    @wraps(func)
    def decorated_func(*args, **kargs):
        if not session.get("user_id") or not session.get("role"):
            return redirect(url_for("auth.login"))
        return func(*args, **kargs)
    return decorated_func


def manager_required(func):
    """Session valide et rôle gestionnaire uniquement."""

    @wraps(func)
    def decorated_func(*args, **kwargs):
        if not session.get("user_id") or not session.get("role"):
            return redirect(url_for("auth.login"))
        if session.get("role", "").lower() != "gestionnaire":
            flash("Accès réservé aux gestionnaires.", "error")
            role = session.get("role", "").lower()
            if role == "professor":
                return redirect(url_for("professor.courses"))
            if role == "student":
                return redirect(url_for("student.courses"))
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return decorated_func


@bp.route("/", methods= ["POST", "GET"])
@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        try:
            user = AuthCtrl.login(
                email = request.form.get("email"),
                password = request.form.get("password")
            )
            session["user_id"] = user.id
            session["role"] = user.role
            match user.role.lower():
                case "gestionnaire":
                    return redirect(url_for("manager.dashboard"))
                case "professor":
                    return redirect(url_for("professor.courses"))
                case "student":
                    return redirect(url_for("student.courses"))
                case _:
                    flash("Rôle inconnu. Contactez l'administrateur.", "error")
                    session.clear()
                    return redirect(url_for(".login"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for(".login"))
    elif request.method == "GET":
        return render_template("auth/login.html")


@bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        try:
            StudentCtrl.register(
                name = request.form.get("name"),
                surname = request.form.get("surname"),
                email = request.form.get("email"),
                password = request.form.get("password"),
                confirm_password = request.form.get("confirm_password"),
                class_id = request.form.get("class_id")
            )
            return redirect(url_for(".login"))
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for(".register"))
    elif request.method == "GET":   
        classes = ClassCtrl.get_all()
        return render_template("auth/register.html", classes = classes)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for(".login"))
