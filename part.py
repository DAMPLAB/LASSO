class Part:
    def __init__(self, name, type, volume):
        self.name = name
        self.type = type
        self.volume = volume

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getVolume(self):
        return self.volume

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setVolume(self, volume):
        self.volume = volume
