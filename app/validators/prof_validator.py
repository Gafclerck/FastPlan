from app.validators.user_validator import UserValidator
import re

class ProfValidator(UserValidator):
    @staticmethod
    def validate_telephone(telephone):
        if not telephone or not isinstance(telephone, str):
            return "Telephone is required and must be a string."
        # Allow digits, spaces, hyphens, parentheses
        if not re.match(r'^[\d\s +\-\(\)]+$', telephone):
            return "Telephone can only contain digits, spaces, hyphens, and parentheses."
        # Remove non-digits to check length
        digits_only = re.sub(r'\D', '', telephone)
        if len(digits_only) < 7 or len(digits_only) > 15:
            return "Telephone number must be between 7 and 15 digits."
        return None

    @staticmethod
    def validate_speciality(speciality):
        if not speciality or not isinstance(speciality, str):
            return "Speciality is required and must be a string."
        if len(speciality.strip()) < 2:
            return "Speciality must be at least 2 characters long."
        return None

    @staticmethod
    def validate_professor(name, surname, email, telephone, speciality, password=None):
        errors = []
        user_errors = UserValidator.validate_user(name, surname, email, password)
        if user_errors:
            errors.extend(user_errors)
        tel_error = ProfValidator.validate_telephone(telephone)
        if tel_error:
            errors.append(tel_error)
        spec_error = ProfValidator.validate_speciality(speciality)
        if spec_error:
            errors.append(spec_error)
        return errors if errors else None