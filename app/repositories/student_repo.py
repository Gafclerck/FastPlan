from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.database import Database

class StudentRepo:
    @staticmethod
    def add(student, class_id):
        engine = Database.get_engine()
        with engine.begin() as conn:
            # try:
            user_id = conn.execute(
                insert(Database.user_table),{
                    "name" : student.name,
                    "surname" : student.surname,
                    "email" : student.email,
                    "password" : student.password,
                    "role" : student.role
                }
            ).lastrowid
            conn.execute(
                insert(Database.student_table),
                {
                "id":user_id,
                "class_id": class_id,
                }
            )
            # except (SQLAlchemyError, DBAPIError):
            #     conn.rollback()
            #     return "Une erreur s'est produite ressayer"
                
    # @staticmethod
    # def getAll():
    #     user_table = Database.user_table
    #     prof_table = Database.prof_table
    #     query = select(user_table).join(prof_table, prof_table.c.id == user_table.c.id)
    #     engine = Database.get_engine()
    #     with engine.begin() as conn:
    #         return conn.execute(query).all()

    @staticmethod
    def getStudentById(id):
        user_table = Database.user_table
        student_table = Database.student_table
        query = select(user_table, student_table).join_from(student_table, user_table).where(
            student_table.c.id == id
        )
        engine = Database.get_engine()
        with engine.connect() as conn:
            return conn.execute(query).fetchone()
