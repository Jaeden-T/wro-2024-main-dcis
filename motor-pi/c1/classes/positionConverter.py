class positionConverter():
    def __init__(self, collem, row):
        self.carCenterY = 0
        self.carCenterX = 0
        
        self.arrayCol = collem
        self.arrayRow = row
    
        print("CAR INT")
        print(self.arrayCol, self.arrayRow)
        
    def getArrayCoords(self, carX, carY):
        arrayCollum = self.arrayCol - carX
        arrayRow = self.arrayRow + carY
        return arrayRow, arrayCollum
    
    def getCarCoords(self, arrayCol, arrayRow):
        carX = self.arrayCol - arrayCol
        carY = arrayRow - self.arrayRow
        return carX, carY
