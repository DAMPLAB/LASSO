from part import Part
from combination import Combination
import json


def saveJSONRegistry(sortedParts):
    dictionaryList = []
    for part in sortedParts:
        partDictionary = {}
        partDictionary['Part Name'] = part.getName()
        partDictionary['Type'] = part.getType()
        partDictionary['Volume'] = part.getVolume()

        dictionaryList.append(partDictionary)

    jsonDictionary = {'Parts': dictionaryList}

    with open('registry.json', 'w') as json_file:
        json.dump(jsonDictionary, json_file, indent=4)


def loadJSONRegistry():
    loadedRegistry = {}
    with open('registry.json') as json_file:
        existingParts = json.load(json_file)
        for jsonPart in existingParts['Parts']:
            partName = jsonPart['Part Name']
            partType = jsonPart['Type']
            partVolume = jsonPart['Volume']
            newPart = Part(partName, partType, partVolume)

            loadedRegistry[partName] = newPart

    return loadedRegistry


def saveJSONCombinations(combinations):
    dictionaryList = []
    for combo in combinations:
        comboDictionary = {}
        comboDictionary['Combination Name'] = combo.getName()
        partsList = [name for name in combo.getPartsList()]
        comboDictionary['Parts'] = partsList

        dictionaryList.append(comboDictionary)

    jsonDictionary = {'Combinations': dictionaryList}

    with open('combinations.json', 'w') as json_file:
        json.dump(jsonDictionary, json_file, indent=4)


def loadJSONCombinations(registry):
    loadedCombinations = {}
    with open('combinations.json') as json_file:
        existingCombos = json.load(json_file)
        for jsonCombo in existingCombos['Combinations']:
            comboName = jsonCombo['Combination Name']
            partNameList = jsonCombo['Parts']

            inRegistry = True
            for partName in partNameList:
                if partName not in registry:
                    inRegistry = False

            if inRegistry:
                newCombination = Combination(comboName, partNameList)
                loadedCombinations[partName] = newCombination

    return loadedCombinations
