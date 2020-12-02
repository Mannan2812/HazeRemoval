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
            imgToDisplay = [0,0,0,0,0]
            img = (skimage.io.imread(request.FILES['img']).astype(np.float32))
            userImgChoice = form.cleaned_data['imgShow']
            if(userImgChoice.count('DCP')!=0): imgToDisplay[0] = 1
            if(userImgChoice.count('RawT')!=0): imgToDisplay[1] = 1
            if(userImgChoice.count('RefineT')!=0): imgToDisplay[2] = 1
            if(userImgChoice.count('PImg')!=0): imgToDisplay[3] = 1
            if(userImgChoice.count('FImg')!=0): imgToDisplay[4] = 1 
            print(img.shape)
            n = Noise(img,0,1)
            img = n.addNoise()
            d = dehaze(img)
            d.getDehazedImage()
            return render(request,'index.html',{'result':True, 'imgToDisplay' : imgToDisplay})
        return render(request,'index.html')
    else:
        form  = ImageUploadForm()
        return render(request,'index.html',{'form': form})