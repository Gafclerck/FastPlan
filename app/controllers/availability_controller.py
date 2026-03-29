from app.repositories.availability_repo import AvailabilityRepo

_DAY_LABELS = {
    0: "Lun",
    1: "Mar",
    2: "Mer",
    3: "Jeu",
    4: "Ven",
    5: "Sam",
    6: "Dim",
}


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

    @staticmethod
    def get_slot_options_for_prof(prof_id):
        """Créneaux dont le prof a déclaré une disponibilité, avec libellés (jour + heures)."""
        slots = AvailabilityRepo.get_time_slots()
        allowed = set(AvailabilityRepo.get_available_slot_ids(prof_id))
        options = []
        for slot in slots:
            if slot.id not in allowed:
                continue
            day_label = _DAY_LABELS.get(slot.day_of_week, str(slot.day_of_week))
            label = (
                f"{day_label} {slot.start_time.strftime('%H:%M')} - "
                f"{slot.end_time.strftime('%H:%M')}"
            )
            options.append({"id": slot.id, "label": label})
        return options
