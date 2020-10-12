import numpy as np
from cv2.ximgproc import guidedFilter

class dehaze:

    omega = 0.95
    top_p = 0.001
    patchSize = 15
    thresholdT = 0.1


    def __init__(self, image):
        self.image = image
    
    def getDarkChannel(self):
        print(self.image)
    
    def getAtmosphericLight(self):
        image=self.image
        top_position=self.top_p
        darkchannel_prior=self.getDarkChannel()
        dimension_x, dimension_y = darkchannel_prior.shape
        flat_image = image.reshape(dimension_x * dimension_y, 3)
        flat_darkchannel_prior = darkchannel_prior.ravel()
        index_found = (-flat_darkchannel_prior).argsort()[:int(dimension_x * dimension_y * top_position)]
        return np.max(flat_image.take(index_found, axis=0), axis=0)
    
    def getRawTransmission(self):
        atmLight = self.getAtmosphericLight()
        transmission = 1 - self.omega*(self.getDarkChannel()/atmLight)
        return transmission


    def getRefineTransmission(self):
        rawT = self.getRawTransmission()
        refinedT = guidedFilter(self.image.astype(np.float32), rawT.astype(np.float32), 50, 1e-4)
        return refinedT

    def getRadiance(self):
        refinedT=self.getRefineTransmission()
        atmosphere=self.getAtmosphericLight()
        image=self.image
        thresholdT=self.thresholdT
        clipped_t = np.clip(refinedT, a_min=thresholdT, a_max=1.0)
        tiled_t = np.zeros_like(image, dtype=np.float32) 
        for i in range(3):
            tiled_t[:, :, i] = clipped_t
        radiance = np.clip((image - atmosphere) / tiled_t + atmosphere, a_min=0, a_max=255)
        return radiance

    def equalizeBrightness(self):
        print("Code Here")

    def getDehazedImage(self):
        print("Code Here")
