from app.repositories.seance_repo import SeanceRepo

class SeanceCtrl:
    @staticmethod
    def create(course_id, slot_id, class_ids):
        error_mess = SeanceRepo.add(course_id, slot_id, class_ids)
        if error_mess:
            raise ValueError(error_mess)

    @staticmethod
    def get_seance_by_class_id(class_id):
        return SeanceRepo.getSeances(target="class", target_id=class_id)
    
    @staticmethod
    def get_seance_by_prof_id(prof_id):
        return SeanceRepo.getSeances(target="prof", target_id=prof_id)
