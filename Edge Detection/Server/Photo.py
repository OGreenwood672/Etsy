import cv2
import PIL

import json

class Photo:
    def __init__(self,ClientNumber):
        self.ClientNumber = ClientNumber
        self.image = self.Load()
    
    def Load(self):
        return cv2.imread(f"../clients/{self.ClientNumber}/Original.png")

    def Save(self):
        cv2.imwrite(f"../clients/{self.ClientNumber}/Result.png", self.image)

    def ConvertToEdge(self, t1, t2):
        self.image = cv2.Canny(self.image, t1, t2)
    
    def InverseImage(self):
        self.image = 255 - self.image
    
    def UpdateImage(self):
        with open(f"../clients/{self.ClientNumber}/Rules.json", "r") as f:
            CurrentRules = json.load(f)

        t1 = 0
        if "EdgeThreshold1" in CurrentRules.keys():
            t1 = int(CurrentRules["EdgeThreshold1"])
        t2 = 0
        if "EdgeThreshold2" in CurrentRules.keys():
            t2 = int(CurrentRules["EdgeThreshold2"])
        if t1 < t2:
            self.ConvertToEdge(t1, t2)
        
        if "InvertColours" in CurrentRules.keys():
            if CurrentRules["InvertColours"]:
                self.InverseImage()
        
        self.Save()
    



if __name__ == "__main__":
    CLIENT = 1
    imgObj = Photo(f"./clients/{CLIENT}/Original.png", CLIENT)
    imgObj.ConvertToEdge()
    imgObj.InverseImage()
    imgObj.Save(f"./clients/{CLIENT}/Result.png")