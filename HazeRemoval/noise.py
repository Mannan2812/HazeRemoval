import numpy as np
class Noise:
    def __init__(self,image, mean, stdVar):
        self.image = image
        self.mean = mean
        self.stdVar = stdVar
    def addNoise(self):
        row, col, ch = self.image.shape
        sigma = self.stdVar**0.5
        gauss = np.random.normal(self.mean, sigma, (row, col, ch))
        gauss = np.abs(gauss.reshape(row, col, ch))
        noisy = self.image + gauss
        return noisy