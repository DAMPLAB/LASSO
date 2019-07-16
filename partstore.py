import part
import json

class PartStore:
    def __init__(self):
        self.parts = []

    def addPart(self, name, type, volume):
        mypart = part.Part(name, type, volume)
        self.parts.append(mypart)

    def findPart(self,name):
        thepart = None
        for part in self.parts:
            if part.name == name:
                thepart = part
        return thepart

    def removePart(self, name, type, volume):
        removeIndex = -1
        for index, partIter in enumerate(self.parts):
            if partIter.getName() == name and partIter.getType() == type and partIter.getVolume() == volume:
                removeIndex = index
                break

        del self.parts[removeIndex]

    def loadJSON(self, filename):
        with open(filename) as json_file:
            existingParts = json.load(json_file)
            for jsonPart in existingParts['Parts']:
                newpart = part.Part(jsonPart['Part Name'],jsonPart['Type'],jsonPart['Volume'])
                self.parts.append(newpart)
        return self.parts

    def saveJSON(self, filename):
        partsList = []
        for part in self.parts:
            partDictionary = {}

            partDictionary['Part Name'] = part.getName()
            partDictionary['Type'] = part.getType()
            partDictionary['Volume'] = part.getVolume()

            partsList.append(partDictionary)

        jsonDictionary = {'Parts': partsList}

        with open(filename, 'w') as json_file:
            json.dump(jsonDictionary, json_file, indent=4)
