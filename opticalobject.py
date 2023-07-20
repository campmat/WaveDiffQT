import json

class OpticalObject:
    def __init__(self, name, pozZ, data, type, func, obj):
        self.name = name
        self.pozZ = pozZ
        self.data = data
        self.type = type
        self.func = func
        self.obj = obj
    
    def toJSON(self):
        return json.dumps({"name": self.name, "pozZ": self.pozZ, "type:": self.type, "func": self.func, "data": self.data})