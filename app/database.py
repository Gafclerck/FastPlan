import os
from sqlalchemy import create_engine
from sqlalchemy import MetaData, ForeignKey, Table, Column, String, Integer, Text, Date, DateTime, Time, func
from flask import current_app

class Database:
    meta_obj = MetaData()
    engine = None
    user_table = Table(
        "users",
        meta_obj,
        Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
        Column("name", String(200), nullable=False),
        Column("surname", String(200), nullable=False),
        Column("email", String(200), unique=True, nullable=False),
        Column("password", Text, nullable=False),
        Column("role", String(50), nullable=False, default="student"),
    )
    prof_table = Table(
        "profs",
        meta_obj,
        Column("id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False),
        Column("speciality", String(200), nullable=False),
        Column("telephone", String(20), nullable=False),
    )
    class_table = Table(
        "classes",
        meta_obj,
        Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
        Column("level", String(100), nullable=False),
        Column("field", String(100), nullable=False),
        Column("academic_year", String(15), nullable=False),
        Column("tag", String(2), nullable=True)
    )
    student_table = Table(
        "students",
        meta_obj,
        Column("id", Integer, ForeignKey("users.id"), primary_key=True, nullable=False),
        Column("class_id", Integer, ForeignKey("classes.id"), nullable=False),
    )
    course_table = Table(
        "courses",
        meta_obj,
        Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
        Column("name", String(100), nullable=False),
        Column("duration", Integer, nullable=False , default=30),
        Column("state", String(200), nullable=False),
        Column("creation_date", DateTime, nullable=False, default=func.now()),
        Column("prof_id", Integer ,  ForeignKey("profs.id"), nullable=False)
    )
    class_course_table = Table(
        "course_class",
        meta_obj,
        Column("id", Integer, primary_key=True, autoincrement=True, nullable=False),
        Column("class_id", ForeignKey("classes.id"), nullable=False),
        Column("course_id", ForeignKey("courses.id"), nullable=False),
    )

    time_slot_table = Table(
        "time_slot",
        meta_obj,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("day_of_week", Integer, nullable=False),
        Column("start_time", Time, nullable=False),
        Column("end_time", Time, nullable=False),
    )

    availability_table = Table(
        "availability",
        meta_obj,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("prof_id", Integer, ForeignKey("profs.id"), nullable=False),
        Column("time_slot_id", Integer, ForeignKey("time_slot.id"), nullable=False),
        Column("status", String(20), nullable=False, default="available"),
    )

    seance_table = Table(
        "seances",
        meta_obj,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("date", DateTime, nullable=False, server_default=func.now()),
        Column("slot_id", Integer, ForeignKey("time_slot.id"), nullable=False),
        Column("course_id", Integer, ForeignKey("courses.id"), nullable=False),
    )

    class_seance_table = Table(
        "class_seance",
        meta_obj,
        Column("id", Integer, primary_key=True, nullable=False, autoincrement=True),
        Column("state", String(50), nullable=False, default="planned"),
        Column("class_id", Integer, ForeignKey("classes.id"), nullable=False),
        Column("seance_id", Integer, ForeignKey("seances.id"), nullable=False),
    )

    @classmethod
    def init_engine(cls, app=None):
        if cls.engine is not None:
            return cls.engine
        if app is None:
            app = current_app
        echo_sql = os.environ.get("SQLALCHEMY_ECHO", "").lower() in ("1", "true", "yes")
        cls.engine = create_engine(
            app.config.get("DATABASE_URL", "sqlite:///default.db"),
            echo=echo_sql,
        )
        return cls.engine
    
    @classmethod
    def get_engine(cls):
        if cls.engine is None:
            cls.init_engine()
        return cls.engine

    @classmethod
    def init_db(cls, app=None):
        engine = cls.init_engine(app)
        cls.meta_obj.create_all(bind=engine)
