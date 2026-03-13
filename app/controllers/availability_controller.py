from app.repositories.availability_repo import AvailabilityRepo

class AvailabilityCtrl:
    @staticmethod
    def get_time_slots():
        return AvailabilityRepo.get_time_slots()

    @staticmethod
    def get_available_slot_ids(prof_id):
        return AvailabilityRepo.get_available_slot_ids(prof_id)

    @staticmethod
    def set_availability(prof_id, time_slot_ids):
        return AvailabilityRepo.set_availability(prof_id, time_slot_ids)
