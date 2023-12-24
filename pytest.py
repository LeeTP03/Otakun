class Person:
    
    def __init__(self, name):
        self.name = name
        self.age = 0
        self.height = 0
        self.weight = 0
        self.hair_color = ""


s = Person("Seth")
print(s.__dict__)