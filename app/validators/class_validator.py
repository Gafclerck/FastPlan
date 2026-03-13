import re

class ClassValidator:
    VALID_LEVELS = ["L1", "L2", "L3", "M1", "M2"]

    @staticmethod
    def validate_level(level):
        if not level or not isinstance(level, str):
            return "Le niveau est obligatoire et doit être une chaîne."
        normalized = level.strip().upper()
        if normalized not in ClassValidator.VALID_LEVELS:
            return f"Le niveau doit être l'un de : {', '.join(ClassValidator.VALID_LEVELS)}."
        return None

    @staticmethod
    def validate_field(field):
        if not field or not isinstance(field, str):
            return "La filière est obligatoire et doit être une chaîne."
        if len(field.strip()) < 2:
            return "La filière doit contenir au moins 2 caractères."
        if not re.match(r'^[-\w\s]+$', field):
            return "La filière ne peut contenir que des lettres, chiffres, espaces et tirets."
        return None

    @staticmethod
    def validate_academic_year(academic_year):
        if not academic_year or not isinstance(academic_year, str):
            return "L'année scolaire est obligatoire et doit être une chaîne."
        if not re.match(r'^\d{4}-\d{4}$', academic_year):
            return "L'année scolaire doit être au format AAAA-AAAA."
        start_year, end_year = map(int, academic_year.split("-"))
        if end_year != start_year + 1:
            return "L'année scolaire doit couvrir deux années consécutives (ex. 2025-2026)."
        return None

    @staticmethod
    def validate_tag(tag):
        if tag is None or tag == "":
            return None
        if not isinstance(tag, str):
            return "Le tag doit être une chaîne."
        cleaned = tag.strip().upper()
        if not re.match(r'^[A-Z]{1}$', cleaned):
            return "Le tag doit contenir 1 caractère lettres"
        return None

    @staticmethod
    def validate_class(level, field, academic_year, tag=None):
        errors = []
        level_error = ClassValidator.validate_level(level)
        if level_error:
            errors.append(level_error)
        field_error = ClassValidator.validate_field(field)
        if field_error:
            errors.append(field_error)
        year_error = ClassValidator.validate_academic_year(academic_year)
        if year_error:
            errors.append(year_error)
        tag_error = ClassValidator.validate_tag(tag)
        if tag_error:
            errors.append(tag_error)
        return errors if errors else None
