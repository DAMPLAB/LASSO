from part import Part
from combination import Combination
from plate import Plate


class Storage:
    def __init__(self):
        self.registry = {}
        self.combinations = {}
        self.plates = {}

    # Registry
    def addPartToRegistry(self, partName, partType, partVolume):
        part = Part(partName, partType, partVolume)
        self.registry[partName] = part

    def getPartFromRegistry(self, partName):
        if partName in self.registry:
            return self.registry[partName]
        else:
            return None

    def removePartFromRegistry(self, partName):
        if partName in self.registry:
            del self.registry[partName]

    def generateSortedParts(self):
        return self.registry.values().sort()

    # Combinations
    def addCombination(self, combinationName, partNames):
        partsList = []
        for name in partNames:
            part = self.registry[name]
            if part.getRemainingVolume() > 0:
                part.removeVolume(1)
            else:
                raise Exception('Not enough volume for ' + name)
            partsList.append(part)

        combination = Combination(combinationName, partsList)
        self.combinations[combinationName] = combination

    def getCombination(self, combinationName):
        if combinationName in self.combinations:
            return self.combinations[combinationName]
        else:
            return None

    def removeCombination(self, combinationName):
        if combinationName in self.combinations:
            del self.combinations[combinationName]

    # Plates
    def addPlate(self, plateName, rows, columns):
        plate = Plate(plateName, rows, columns)
        self.plates[plateName] = plate

    def getPlate(self, plateName):
        if plateName in self.plates:
            return self.plates[plateName]
        else:
            return None

    def removePlate(self, plateName):
        if plateName in self.plates:
            del self.plates[plateName]
