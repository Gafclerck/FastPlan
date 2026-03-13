class User():
    def __init__(self, name, surname, email, password, role="student"):
        self.name = name
        self.surname = surname
        self.email = email
        self.password = password
        self.role = role