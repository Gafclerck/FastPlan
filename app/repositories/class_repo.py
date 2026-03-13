from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.database import Database

class ClassRepo:
    @staticmethod
    def add(classe):
        class_table = Database.class_table
        query = insert(class_table)
        engine = Database.get_engine()
        with engine.begin() as conn:
            try:
                conn.execute(
                    query,{
                        "level" : classe.level,
                        "field" : classe.field,
                        "academic_year" : classe.academic_year,
                        "tag" : classe.tag,
                    }
                )
            except (SQLAlchemyError, DBAPIError):
                conn.rollback()
                
    @staticmethod
    def getAll():
        class_table = Database.class_table
        query = select(class_table)
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).all()

    @staticmethod
    def getByItems(level, field, academic_year, tag):
        class_table = Database.class_table
        query = select(class_table).where(
            class_table.c.level == level,
            class_table.c.field == field,
            class_table.c.academic_year == academic_year,
            class_table.c.tag == tag
        )
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).all()
    
    @staticmethod
    def getById(id):
        class_table = Database.class_table
        query = select(class_table).where(
            class_table.c.id == id
        )
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).fetchone()

    @staticmethod
    def getByProfId(prof_id):
        class_table = Database.class_table
        class_course_table = Database.class_course_table
        course_table = Database.course_table
        query = (
            select(class_table)
            .join(class_course_table, class_course_table.c.class_id == class_table.c.id)
            .join(course_table, course_table.c.id == class_course_table.c.course_id)
            .where(course_table.c.prof_id == prof_id)
            .distinct()
        )
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).all()

    @staticmethod
    def hasCourseInClass(class_id, course_id):
        class_course_table = Database.class_course_table
        query = select(class_course_table.c.id).where(
            class_course_table.c.class_id == class_id,
            class_course_table.c.course_id == course_id
        )
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).fetchone()

    @staticmethod
    def addCourseToClass(class_id, course_id):
        class_course_table = Database.class_course_table
        query = insert(class_course_table)
        engine = Database.get_engine()
        with engine.begin() as conn:
            try:
                conn.execute(
                    query, {
                        "class_id": class_id,
                        "course_id": course_id
                    }
                )
                return None
            except (SQLAlchemyError, DBAPIError):
                conn.rollback()
                return "Echec de l'association du cours à la classe."