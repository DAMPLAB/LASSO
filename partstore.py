import part
import json
from sbol import *

typeDictionary = {'Promoter' : SO_PROMOTER, 'Terminator' : SO_TERMINATOR, 'CDS' : SO_CDS, 'Insulator' : 'http://identifiers.org/so/SO_0000627'}


class PartStore:
    def __init__(self):
        self.parts = []
        self.componentDefinitions = []

    def addPart(self, name, type, volume):
        mypart = part.Part(name, type, volume)
        self.parts.append(mypart)

        cd = ComponentDefinition(name)

        cd.roles = typeDictionary[type]
        self.componentDefinitions.append(cd)

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
        del self.componentDefinitions[removeIndex]

    def loadJSON(self, filename):
        with open(filename) as json_file:
            existingParts = json.load(json_file)
            for jsonPart in existingParts['Parts']:
                newpart = part.Part(jsonPart['Part Name'],jsonPart['Type'],jsonPart['Volume'])
                self.parts.append(newpart)
                cd = ComponentDefinition(jsonPart['Part Name'])
                cd.roles = typeDictionary[jsonPart['Type']]
                self.componentDefinitions.append(cd)

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
