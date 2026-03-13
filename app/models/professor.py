from app.models.user import User

class Professor(User):
    def __init__(self, name, surname, email, telephone, speciality, password):
        super().__init__(name, surname, email, password, role="professor")
        self.telephone = telephone
        self.speciality = speciality