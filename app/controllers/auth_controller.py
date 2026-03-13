from flask import session
from werkzeug.security import check_password_hash
from app.repositories.user_repo import UserRepo
from app.validators.user_validator import UserValidator

class AuthCtrl:
    def login(email, password):
        mail_error = UserValidator.validate_email(email)
        if mail_error:
            raise ValueError(mail_error)
        if not password:
            raise ValueError("Password is required")
        user = UserRepo.getByEmail(email)

        if not user:
            raise ValueError("Account not found ")
        if not check_password_hash(user.password, password):
        # if not user.password == password:
            raise ValueError("email or password incorrect")
        
        return user

    def register():
        pass