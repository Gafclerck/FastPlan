from sqlalchemy import delete, insert, select

from app.database import Database


class AvailabilityRepo:
    @staticmethod
    def get_time_slots():
        table = Database.time_slot_table
        engine = Database.get_engine()
        query = select(table).order_by(table.c.day_of_week, table.c.start_time)
        with engine.connect() as conn:
            return conn.execute(query).all()

    @staticmethod
    def get_available_slot_ids(prof_id):
        table = Database.availability_table
        engine = Database.get_engine()
        query = select(table.c.time_slot_id).where(
            table.c.prof_id == prof_id,
            table.c.status == "available",
        )
        with engine.connect() as conn:
            return [row.time_slot_id for row in conn.execute(query).all()]

    @staticmethod
    def set_availability(prof_id, time_slot_ids):
        table = Database.availability_table
        engine = Database.get_engine()
        unique_ids = list({int(x) for x in time_slot_ids})
        with engine.begin() as conn:
            conn.execute(delete(table).where(table.c.prof_id == prof_id))
            if unique_ids:
                rows = [
                    {
                        "prof_id": prof_id,
                        "time_slot_id": slot_id,
                        "status": "available",
                    }
                    for slot_id in unique_ids
                ]
                conn.execute(insert(table), rows)
