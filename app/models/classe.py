class Classe : 
    def __init__(self, level:str, field:str, academic_year,tag=None):
        self.level = level
        self.field = field
        self.academic_year = academic_year
        self.tag = tag

    @property
    def name(self):
        name =  f"{self.level}-{self.field}"
        if self.tag : name += f"-{self.tag}"
        return name