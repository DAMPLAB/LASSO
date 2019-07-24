class Part:
    def __init__(self, name, type, volume):
        self.name = name
        self.type = type
        self.volume = volume
        self.remainingVolume = volume

    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getVolume(self):
        return self.volume

    def getRemainingVolume(self):
        return self.remainingVolume

    def setName(self, name):
        self.name = name

    def setType(self, type):
        self.type = type

    def setVolume(self, volume):
        self.volume = volume

    def setRemainingVolume(self, volume):
        self.remainingVolume = volume

    def removeVolume(self, volume):
        self.remainingVolume -= volume

    def __lt__(self, other):
        if self.type == other.type:
            return self.name < other.name
        else:
            return self.type < other.type
