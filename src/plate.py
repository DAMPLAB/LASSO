class Plate:
    def __init__(self, name, rows, columns):
        self.name = name
        self.plateArray = []
        self.rows = rows
        self.columns = columns

        for x in range(0, rows):
            singleRow = []
            for y in range(0, columns):
                singleRow.append(None)

            self.plateArray.append(singleRow)

    def setWell(self, row, column, partName):
        self.plateArray[row][column] = partName

    def removeWell(self, row, column):
        self.plateArray[row][column] = None

    def getWellContents(self, row, column):
        return self.plateArray[row][column]

    def getWell(self, partName):
        coordinates = []
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                wellContents = self.plateArray[x][y]
                if wellContents is not None:
                    if wellContents == partName:
                        coordinates.append((x, y))

        return coordinates

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
