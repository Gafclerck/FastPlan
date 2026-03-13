from werkzeug.security import generate_password_hash
from app.models.professor import Professor
from app.repositories.professor_repo import ProfRepo
from app.repositories.user_repo import UserRepo
from app.validators.prof_validator import ProfValidator

class ProfCtrl:
    @staticmethod
    def create_professor(name, surname, email, telephone, speciality):
        validation_errors = ProfValidator.validate_professor(name, surname, email, telephone, speciality)
        if validation_errors:
            raise ValueError("; ".join(validation_errors))
        user = UserRepo.getByEmail(email)
        if user:
            raise ValueError("Compte deja existant")
        password = generate_password_hash("pass") # to be modify
        prof = Professor(name, surname, email, telephone, speciality, password)
        erreur = ProfRepo.add(prof)
        if erreur:
            raise ValueError("Echec de la cration du compte")

    @staticmethod
    def get_all():
        return ProfRepo.getAll()

    @staticmethod
    def get_prof_by_id(id):
        return ProfRepo.getProfById(id)

    @staticmethod
    def get_prof_by_user_id(user_id):
        return ProfRepo.getProfByUserId(user_id)
