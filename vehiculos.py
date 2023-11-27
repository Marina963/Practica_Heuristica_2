class Vehiculos():
    def __init__(self, id, type, freezer):
        self.id = id
        self.type = type
        self.freezer = freezer

    def __str__(self):
        return self.id + "-" + self.type + "-" + self.freezer

