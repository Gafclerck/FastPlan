from app.models.course import Course
from app.repositories.course_repo import CourseRepo
from app.validators.course_validator import CourseValidator

class CourseCtrl:
    @staticmethod
    def create(prof_id, name, duration, classes):
        errors = CourseValidator.validate_course(name=name, duration=duration)
        if errors:
            raise ValueError(", ".join(errors))
        course = Course(name, duration)
        error_message = CourseRepo.add(prof_id, course, classes)
        if error_message:
            raise ValueError(error_message)
        
    @staticmethod
    def get_all():
        return CourseRepo.getAll()
    
    @staticmethod
    def get_course_by_prof_id(id):
        return CourseRepo.getCourseByProfId(id)
    
    @staticmethod
    def get_course_by_class_id(id):
        return CourseRepo.getCourseByClassId(id)

    @staticmethod
    def get_all():
        return CourseRepo.getAll()

    @staticmethod
    def get_by_id(id):
        return CourseRepo.getById(id)
