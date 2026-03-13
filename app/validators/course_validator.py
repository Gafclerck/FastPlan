import re

class CourseValidator:
    @staticmethod
    def validate_name(name):
        if not name or not isinstance(name, str):
            return "L'intitulé est obligatoire et doit être une chaîne."
        if len(name.strip()) < 2:
            return "L'intitulé doit contenir au moins 2 caractères."       
        return None

    @staticmethod
    def validate_duration(duration):
        if duration is None or duration == "":
            return "La durée est obligatoire."
        if isinstance(duration, str):
            if not duration.strip().isdigit():
                return "La durée doit être un nombre entier."
            duration_value = int(duration)
        elif isinstance(duration, int):
            duration_value = duration
        else:
            return "La durée doit être un nombre entier."
        if duration_value <= 0:
            return "La durée doit être un nombre positif."
        if duration_value > 100:
            return "La durée ne peut pas dépasser 100 heures."
        return None

    @staticmethod
    def validate_state(state):
        if not state or not isinstance(state, str):
            return "L'état est obligatoire et doit être une chaîne."
        if len(state.strip()) < 2:
            return "L'état doit contenir au moins 2 caractères."
        return None

    @staticmethod
    def validate_course(name, duration):
        errors = []
        name_error = CourseValidator.validate_name(name)
        if name_error:
            errors.append(name_error)
        duration_error = CourseValidator.validate_duration(duration)
        if duration_error:
            errors.append(duration_error)
        return errors if errors else None
