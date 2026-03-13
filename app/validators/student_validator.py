from app.validators.user_validator import UserValidator
import re

class StudentValidator(UserValidator):
    @staticmethod
    def validate_student(name, surname, email, password, confirm_password):
        errors = []
        user_errors = UserValidator.validate_user(name, surname, email, password)
        if user_errors:
            errors.extend(user_errors)
        if not password:
            errors.append("Password is required")
        if password != confirm_password:
            errors.append("Unmatching passwords")
        return errors if errors else None