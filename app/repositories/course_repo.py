from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.database import Database

class CourseRepo:
    @staticmethod
    def add(prof_id, course, classes):
        course_table = Database.course_table
        class_course_table = Database.class_course_table
        query = insert(course_table)
        engine = Database.get_engine()
        with engine.begin() as conn:
            try:
                course_id = conn.execute(
                    query,{
                        "prof_id": prof_id,
                        "name" : course.name,
                        "duration" : int(course.duration),
                        "state" : course.state,
                    }
                ).lastrowid
                for classe_id in classes:
                    conn.execute(
                        insert(class_course_table),
                        {
                            "course_id":course_id,
                            "class_id": classe_id
                        }
                    )
                return None
            except (SQLAlchemyError, DBAPIError)  as e:
                print(str(e))
                conn.rollback()
                return "Echec de L'ajout du cours resessayer"
                
    @staticmethod
    def getAll():
        course_table = Database.course_table
        prof_table = Database.prof_table
        user_table = Database.user_table
        query = select(course_table, user_table.c.name).join(
            prof_table, course_table.c.prof_id == prof_table.c.id
        ).join(user_table, user_table.c.id == prof_table.c.id)
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).all()

    @staticmethod
    def getCourseByProfId(id):
        course_table = Database.course_table
        query = select(course_table).where(
            course_table.c.prof_id == id
        )
        engine = Database.get_engine()
        with engine.connect() as conn:
            return conn.execute(query).all()
        
    @staticmethod
    def getCourseByClassId(id):
        course_table = Database.course_table
        class_course_table = Database.class_course_table
        query = select(course_table).join(class_course_table, class_course_table.c.course_id == course_table.c.id).where(
            class_course_table.c.class_id == id
        )
        engine = Database.get_engine()
        with engine.connect() as conn:
            return conn.execute(query).all()

    @staticmethod
    def getById(id):
        course_table = Database.course_table
        query = select(course_table).where(
            course_table.c.id == id
        )
        engine = Database.get_engine()
        with engine.connect() as conn:
            return conn.execute(query).fetchone()
