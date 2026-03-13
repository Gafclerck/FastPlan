import os
from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.controllers.prof_controller import ProfCtrl
from app.controllers.course_controller import CourseCtrl
from app.controllers.class_controller import ClassCtrl
from app.config import Config

bp = Blueprint("profs", __name__, url_prefix="/profs",
                template_folder=os.path.join(Config.APP_DIR, "templates", "manager"))
