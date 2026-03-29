from sqlalchemy import func, insert, select

from app.database import Database


class UserRepo:
    @staticmethod
    def create_user(name, surname, email, password_hash, role):
        """Insert a row in `users` only (no student/prof row). Returns new user id."""
        user_table = Database.user_table
        engine = Database.get_engine()
        with engine.begin() as conn:
            uid = conn.execute(
                insert(user_table),
                {
                    "name": name.strip(),
                    "surname": surname.strip(),
                    "email": email.strip().lower(),
                    "password": password_hash,
                    "role": role,
                },
            ).lastrowid
        return uid

    @staticmethod
    def getByEmail(email):
        user_table = Database.user_table
        em = (email or "").strip().lower()
        query = select(user_table).where(func.lower(user_table.c.email) == em)
        engine = Database.get_engine()
        with engine.begin() as conn:
            users = conn.execute(query).all()
            if len(users) >= 1:
                return users[0]
            return None
        
    @staticmethod
    def remove():
        pass

    @staticmethod
    def update():
        pass

    @staticmethod
    def get():
        pass
