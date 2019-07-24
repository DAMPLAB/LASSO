class Plate:
    def __init__(self, rows, columns):
        self.plateArray = []
        self.rows = rows
        self.columns = columns

        for x in range(0, rows):
            singleRow = []
            for y in range(0, columns):
                singleRow.append(None)

            self.plateArray.append(singleRow)

    def setWell(self, row, column, part):
        self.plateArray[row][column] = part

    def removeWell(self, row, column):
        self.plateArray[row][column] = None

    def getWellContents(self, row, column):
        return self.plateArray[row][column]

    def getWell(self, part):
        partName = part.getName()
        coordinates = []
        for x in range(0, self.rows):
            for y in range(0, self.columns):
                wellContents = self.plateArray[x][y]
                if wellContents is not None:
                    if wellContents.getName() == partName:
                        coordinates.append((x, y))

        return coordinates
