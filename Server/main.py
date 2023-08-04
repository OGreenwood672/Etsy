import cv2
import PIL

class Photo:
    def __init__(self, path):
        self.image = self.Load(path)
    
    def Load(self, path):
        return cv2.imread(path)

    def Save(self, path):
        cv2.imwrite(path, self.image)

    def ConvertToEdge(self):
        self.image = cv2.Canny(self.image, 50, 100)
    
    def InverseImage(self):
        self.image = 255 - self.image
    



if __name__ == "__main__":
    CLIENT = 1
    imgObj = Photo(f"./clients/{CLIENT}/Original.png")
    imgObj.ConvertToEdge()
    imgObj.InverseImage()
    imgObj.Save(f"./clients/{CLIENT}/Result.png")