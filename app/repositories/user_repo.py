from sqlalchemy import select
from app.database import Database

class UserRepo:    
    @staticmethod
    def getByEmail(email):
        user_table = Database.user_table
        query = select(user_table).where(user_table.c.email == email)
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
