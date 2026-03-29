from app.repositories.seance_repo import SeanceRepo
from app.controllers.course_controller import CourseCtrl
from app.controllers.availability_controller import AvailabilityCtrl


class SeanceCtrl:
    @staticmethod
    def create(course_id, slot_id, class_ids, class_context_id=None):
        if not class_ids:
            raise ValueError("Sélectionnez au moins une classe.")
        try:
            course_id = int(course_id)
            slot_id = int(slot_id)
        except (TypeError, ValueError):
            raise ValueError("Créneau ou cours invalide.")

        if class_context_id is not None and not CourseCtrl.is_course_assigned_to_class(
            course_id, class_context_id
        ):
            raise ValueError("Ce cours n'est pas attribué à cette classe.")

        course_row = CourseCtrl.get_by_id(course_id)
        if not course_row:
            raise ValueError("Cours invalide.")

        allowed_slots = set(AvailabilityCtrl.get_available_slot_ids(course_row.prof_id))
        if slot_id not in allowed_slots:
            raise ValueError(
                "Ce créneau n'est pas parmi les disponibilités du professeur pour ce cours."
            )

        error_mess = SeanceRepo.add(course_id, slot_id, class_ids)
        if error_mess:
            raise ValueError(error_mess)

    @staticmethod
    def get_seance_by_class_id(class_id):
        return SeanceRepo.getSeances(target="class", target_id=class_id)
    
    @staticmethod
    def get_seance_by_prof_id(prof_id):
        return SeanceRepo.getSeances(target="prof", target_id=prof_id)
