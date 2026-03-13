from app.models.classe import Classe
from app.repositories.class_repo import ClassRepo
from app.repositories.course_repo import CourseRepo
from app.validators.class_validator import ClassValidator

class ClassCtrl:
    @staticmethod
    def create(level, field, academic_year, tag=None):
        errors = ClassValidator.validate_class(level, field, academic_year, tag)
        if errors:
            raise ValueError(", ".join(errors))
        if ClassRepo.getByItems(level, field, academic_year, tag):
            raise ValueError("Cette classe existe deja")
        classe = Classe(level, field, academic_year, tag)
        ClassRepo.add(classe)
        
    @staticmethod
    def get_all():
        return ClassRepo.getAll()
    
    @staticmethod
    def get_class_by_id(id):
        return ClassRepo.getById(id)

    @staticmethod
    def get_classes_by_prof_id(prof_id):
        return ClassRepo.getByProfId(prof_id)

    @staticmethod
    def add_course_to_class(class_id, course_id):
        if not class_id:
            raise ValueError("Classe introuvable.")
        if not course_id:
            raise ValueError("Veuillez choisir un cours.")
        try:
            class_id = int(class_id)
            course_id = int(course_id)
        except ValueError:
            raise ValueError("Identifiants invalides.")
        if not ClassRepo.getById(class_id):
            raise ValueError("Classe introuvable.")
        if not CourseRepo.getById(course_id):
            raise ValueError("Cours introuvable.")
        if ClassRepo.hasCourseInClass(class_id, course_id):
            raise ValueError("Ce cours est déjà associé à cette classe.")
        error = ClassRepo.addCourseToClass(class_id, course_id)
        if error:
            raise ValueError(error)
