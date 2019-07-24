class Combination:
    def __init__(self, name, partNameList):
        self.name = name
        self.partNameList = partNameList

    def getName(self):
        return self.name

    def getPartsList(self):
        return self.partNameList

    def setName(self, name):
        self.name = name

    def setParts(self, partNameList):
        self.partNameList = partNameList

    # def generateTypeList(self):
    #     typeList = []
    #     for part in self.partsList:
    #         typeList.append(part.getType())

    #     return typeList
