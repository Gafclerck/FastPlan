from werkzeug.security import generate_password_hash
from app.models.student import Student
from app.repositories.user_repo import UserRepo
from app.repositories.student_repo import StudentRepo
from app.validators.student_validator import StudentValidator

class StudentCtrl:
    @staticmethod
    def register(name, surname, email, password, confirm_password, class_id):
        validation_errors = StudentValidator.validate_student(name, surname, email, password, confirm_password)
        if validation_errors:
            raise ValueError("; ".join(validation_errors))
        user = UserRepo.getByEmail(email)   
        if user:
            raise ValueError("Compte deja existant")
        password = generate_password_hash(password)
        student = Student(name, surname, email, password)
        erreur = StudentRepo.add(student, class_id = class_id)
        if erreur:
            raise ValueError("Échec de la création du compte.")

    # @staticmethod
    # def get_all():
    #     return ProfRepo.getAll()

    @staticmethod
    def get_student_by_id(id):
        return StudentRepo.getStudentById(id)

    # @staticmethod
    # def get_prof_by_user_id(user_id):
    #     return ProfRepo.getProfByUserId(user_id)
