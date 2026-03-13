import re

class UserValidator:
    @staticmethod
    def validate_name(name):
        if not name or not isinstance(name, str):
            return "Name is required and must be a string."
        if len(name.strip()) < 2:
            return "Name must be at least 2 characters long."
        if not re.match(r'^[-\w\s]+$', name):
            return "Name can only contain letters and spaces."
        return None

    @staticmethod
    def validate_surname(surname):
        if not surname or not isinstance(surname, str):
            return "Surname is required and must be a string."
        if len(surname.strip()) < 2:
            return "Surname must be at least 2 characters long."
        if not re.match(r'^[-\w\s]+$', surname):
            return "Surname can only contain letters and spaces."
        return None

    @staticmethod
    def validate_email(email):
        if not email or not isinstance(email, str):
            return "Email is required and must be a string."
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return "Invalid email format."
        return None

    @staticmethod
    def validate_password(password):
        # if not password or not isinstance(password, str):
        #     return "Password is required and must be a string."
        # if len(password) < 8:
        #     return "Password must be at least 8 characters long."
        # if not re.search(r'[A-Z]', password):
        #     return "Password must contain at least one uppercase letter."
        # if not re.search(r'[a-z]', password):
        #     return "Password must contain at least one lowercase letter."
        # if not re.search(r'\d', password):
        #     return "Password must contain at least one digit."
        return None

    @staticmethod
    def validate_role(role):
        if not role or not isinstance(role, str):
            return "Role is required and must be a string."
        valid_roles = ["student", "professor", "admin"]
        if role not in valid_roles:
            return f"Role must be one of: {', '.join(valid_roles)}."
        return None

    @staticmethod
    def validate_user(name, surname, email, password, role="student"):
        errors = []
        name_error = UserValidator.validate_name(name)
        if name_error:
            errors.append(name_error)
        surname_error = UserValidator.validate_surname(surname)
        if surname_error:
            errors.append(surname_error)
        email_error = UserValidator.validate_email(email)
        if email_error:
            errors.append(email_error)
        password_error = UserValidator.validate_password(password)
        if password_error:
            errors.append(password_error)
        role_error = UserValidator.validate_role(role)
        if role_error:
            errors.append(role_error)
        return errors if errors else None