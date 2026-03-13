from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from app.database import Database

class ProfRepo:
    @staticmethod
    def add(prof):
        user_table = Database.user_table
        prof_table = Database.prof_table
        query1 = insert(user_table).returning(user_table.c.id)
        query2 = insert(prof_table)
        engine = Database.get_engine()
        with engine.begin() as conn:
            try:
                user_id = conn.execute(
                    query1,{
                        "name" : prof.name,
                        "surname" : prof.surname,
                        "email" : prof.email,
                        "password" : prof.password,
                        "role" : prof.role
                    }
                ).lastrowid
                conn.execute(
                    query2,
                    {
                    "id":user_id,
                    "speciality": prof.speciality,
                    "telephone": prof.telephone,
                    }
                )
            except (SQLAlchemyError, DBAPIError):
                conn.rollback()
                return "Une erreur s'est produite ressayer"
                
    @staticmethod
    def getAll():
        user_table = Database.user_table
        prof_table = Database.prof_table
        query = select(user_table).join(prof_table, prof_table.c.id == user_table.c.id)
        engine = Database.get_engine()
        with engine.begin() as conn:
            return conn.execute(query).all()


    @staticmethod
    def getProfById(id):
        user_table = Database.user_table
        prof_table = Database.prof_table
        query = select(user_table, prof_table).join_from(prof_table, user_table).where(
            prof_table.c.id == id
        )
        engine = Database.get_engine()
        with engine.connect() as conn:
            return conn.execute(query).fetchone()
