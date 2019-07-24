class Combination:
    def __init__(self,name,partsList):
        self.name = name
        self.partsList = partsList
    
    def getName(self):
        return self.name
    
    def getPartsList(self):
        return self.partsList
    
    def setName(self,name):
        self.name = name
    
    def setParts(self,partsList):
        self.partsList = partsList