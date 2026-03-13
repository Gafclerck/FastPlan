from sqlalchemy import delete, insert, select
from app.database import Database
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

class SeanceRepo:
    @staticmethod
    def add(course_id, slot_id, class_ids):
        seance_table = Database.seance_table
        class_seance = Database.class_seance_table
        engine = Database.get_engine()
        unique_ids = list({int(x) for x in class_ids})
        with engine.begin() as conn:
            try :
                seance_id = conn.execute(
                    insert(seance_table),
                    {
                        "slot_id":slot_id,
                        "course_id":course_id
                    }
                ).lastrowid
                if not seance_id: raise SQLAlchemyError
                rows = [
                    {
                        "seance_id": seance_id,
                        "class_id": class_id,
                    }
                    for class_id in unique_ids
                ]
                conn.execute(insert(class_seance), rows)
            except (SQLAlchemyError, DBAPIError):
                conn.rollback()
                return "Echec de l'ajout veillez reessayer"

    @staticmethod
    def getSeanceByClass(class_id):
        return SeanceRepo.getSeances(target="class", target_id=class_id)
    
    @staticmethod
    def getSeanceByProfId(prof_id):
        return SeanceRepo.getSeances(target="prof", target_id=prof_id)

    @staticmethod
    def getSeances(target, target_id):
        seance_table = Database.seance_table
        class_seance = Database.class_seance_table
        course_table = Database.course_table
        class_table = Database.class_table
        slot_table = Database.time_slot_table
        prof_table = Database.prof_table
        user_table = Database.user_table
        engine = Database.get_engine()

        if target == "class":
            condition = class_seance.c.class_id == target_id
        elif target == "prof":
            condition = course_table.c.prof_id == target_id
        else:
            raise ValueError("target must be 'prof' or 'class'")

        with engine.begin() as conn:
            return conn.execute(
                select(
                    seance_table.c.id,
                    seance_table.c.course_id,
                    seance_table.c.slot_id,
                    seance_table.c.date,
                    class_seance.c.state,
                    user_table.c.name.label("prof_name"),
                    user_table.c.surname.label("prof_surname"),
                    class_table.c.field.label("class_field"),
                    class_table.c.level.label("class_level"),
                    class_table.c.tag.label("class_tag"),
                    course_table.c.name.label("course_name"),
                    slot_table.c.day_of_week,
                )
                .join(course_table, course_table.c.id == seance_table.c.course_id)
                .join(class_seance, seance_table.c.id == class_seance.c.seance_id)
                .join(class_table, class_table.c.id == class_seance.c.class_id)
                .join(slot_table, slot_table.c.id == seance_table.c.slot_id)
                .join(prof_table, course_table.c.prof_id == prof_table.c.id)
                .join(user_table, user_table.c.id == prof_table.c.id)
                .where(condition)
            ).all()
