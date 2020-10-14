from .dehaze import *
from .noise import *
# PATH = "/home/bansal/Desktop/Single-Image-Haze-Removal-master/image/city.jpg"
# img = (skimage.io.imread(PATH).astype(np.float32))

import skimage.io
import numpy as np
from django.shortcuts import HttpResponse,render
from .forms import ImageUploadForm
def homepage(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            img = (skimage.io.imread(request.FILES['img']).astype(np.float32))
            print(img.shape)
            n = Noise(img,0,1)
            img = n.addNoise()
            d = dehaze(img)
            d.getDehazedImage()
            return render(request,'index.html',{'result':True})
        return render(request,'index.html')
    else:
        form  = ImageUploadForm()
        return render(request,'index.html',{'form': form})