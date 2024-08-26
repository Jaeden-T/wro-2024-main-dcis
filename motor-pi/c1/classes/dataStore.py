import datetime

#* Note All Data is rounded to intiger 
class DataStoreObject():
    def __init__(self, ultN: float, ultS: float, ultE: float,ultW: float, imu: float):
        self.time = datetime.datetime.now()
        self.ult_N = round(ultN, 3)
        self.ult_S = round(ultS ,3)
        self.ult_E = round(ultE,3)
        self.ult_W = round(ultW, 3)
        self.imu = round(imu, 3)
    def exportData(self):
        return f"{self.time},{self.ult_N}, {self.ult_S}{self.ult_E},{self.ult_W},{self.imu}"
    
    def getIntNorth(self):
        return int(round(self.ult_N))
        
    def getIntSouth(self):
        return int(round(self.ult_S))
            
    def getIntEast(self):
        return int(round(self.ult_E))
            
    def getIntWest(self):
        return int(round(self.ult_West))