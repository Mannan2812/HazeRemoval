# from dehaze import *
# from noise import *
# PATH = "/home/bansal/Desktop/Single-Image-Haze-Removal-master/image/city.jpg"
# img = (skimage.io.imread(PATH).astype(np.float32))
# n = Noise(img,0,1)
# img = n.addNoise()
# d = dehaze(img)
# d.getDehazedImage()
from django.shortcuts import HttpResponse,render
def homepage(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,'index.html')