import numpy as np
from matplotlib import pyplot as plt
import os
import skimage.color
import skimage.exposure
import skimage
import skimage.io
from cv2.ximgproc import guidedFilter
class dehaze:

    omega = 0.95
    top_p = 0.001
    patchSize = 15
    thresholdT = 0.1
    outDir = "./static/img/"
    

    def __init__(self, image):
        self.image = image
    
    def getDarkChannel(self, image):
        dimensionX, dimensionY, dimensionZ = image.shape
        darkCh = np.zeros((dimensionX, dimensionY), dtype=np.float32)
        paddedImg = np.pad(image, ((self.patchSize // 2, self.patchSize // 2),
                          (self.patchSize // 2, self.patchSize // 2), (0, 0)), 'edge')
        for i, j in np.ndindex(darkCh.shape):
            darkCh[i, j] = np.min(
                paddedImg[i:i + self.patchSize, j:j + self.patchSize, :])
        return darkCh
    
    def getAtmosphericLight(self):
        image=self.image
        topP=self.top_p
        darkCh=self.darkCh
        dimensionX, dimensionY = darkCh.shape
        flatImg = image.reshape(dimensionX * dimensionY, 3)
        flatDarkCh = darkCh.ravel()
        index_found = (-flatDarkCh).argsort()[:int(dimensionX * dimensionY * topP)]
        return np.max(flatImg.take(index_found, axis=0), axis=0)
    
    def getRawTransmission(self):
        atmLight = self.atmLight
        darkCh = self.getDarkChannel(self.image/atmLight);
        transmission = 1 - self.omega*darkCh
        print(transmission.shape)
        return transmission


    def getRefineTransmission(self):
        rawT = self.rawT
        print(rawT.shape)
        print(self.image.shape)
        refinedT = guidedFilter(self.image.astype(np.float32), rawT.astype(np.float32), 50, 1e-4)
        return refinedT

    def getRadiance(self):
        refinedT=self.refinedT
        atmosphere=self.atmLight
        image=self.image
        thresholdT=self.thresholdT
        clippedT = np.clip(refinedT, a_min=thresholdT, a_max=1.0)
        tiledT = np.zeros_like(image, dtype=np.float32) 
        for i in range(3):
            tiledT[:, :, i] = clippedT
        radiance = np.clip((image - atmosphere) / tiledT + atmosphere, a_min=0, a_max=255)
        return radiance

    def equalizeBrightness(self, dehazedImg):
        hsvImg = skimage.color.rgb2hsv(dehazedImg)
        hsvImg[..., 2] = skimage.exposure.equalize_hist(hsvImg[..., 2])
        finalImg = skimage.color.hsv2rgb(hsvImg)
        return finalImg

    def getDehazedImage(self):
        self.darkCh = self.getDarkChannel(self.image)
        skimage.io.imsave(os.path.join(self.outDir, 'dark.jpg'), np.uint8(self.darkCh))
        self.atmLight = self.getAtmosphericLight()
        self.rawT = self.getRawTransmission()
        self.refinedT=self.getRefineTransmission()
        skimage.io.imsave(os.path.join(
            self.outDir, 'raw_transmission.jpg'), (255 * self.rawT).astype(np.uint8))
        skimage.io.imsave(os.path.join(
            self.outDir, 'refine_transmission.jpg'), (255 * self.refinedT).astype(np.uint8))
        self.dehazedImg = self.getRadiance()
        skimage.io.imsave(os.path.join(self.outDir, 'noequalize.jpg'),
                      np.uint8(self.dehazedImg))
        equalized_img = self.equalizeBrightness(self.dehazedImg)
        skimage.io.imsave(os.path.join(self.outDir, 'equalize.jpg'), equalized_img)
        return equalized_img
