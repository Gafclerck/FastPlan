from app.models.user import User

class Student(User):
    def __init__(self, name, surname, email, password):
        super().__init__(name, surname, email, password, role= "student")