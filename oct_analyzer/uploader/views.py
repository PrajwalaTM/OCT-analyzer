from django.shortcuts import render
from django.conf import settings
from .models import ImageModel
from .forms import ImageForm
import matplotlib.pyplot as plt
from predictor import predict
import time
# Create your views here.

def model_form_upload(request):
    saved = False
    #lastimage= ImageModel.objects.last()
    #imagefile= lastimage.image
    imagefile=None
    template = 'uploader/home.html'
    #if request.method == 'POST':
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        print("Form IS VAAAALIDDD")
        form.save()
        saved=True 
        lastimage= ImageModel.objects.last()
        print(str(lastimage))
        imagefile= lastimage.image
        #print("Lifes screwed")
        #print(request.method)
        #form = ImageForm()
    return render(request, template, {'form':form,'saved':saved,'imagefile':imagefile})

def post_upload(request):
    lastimage= ImageModel.objects.last()
    imagefile= lastimage.image
    print(str(imagefile))
    path = "/home/prajwala/Videos/oct_analyzer"+settings.MEDIA_URL+str(imagefile)
    results_path =  "/home/prajwala/Videos/oct_analyzer"+settings.MEDIA_URL+"results/"
    first,name = str(imagefile).split("/")
    results = predict(path,results_path,name)
    #im = Image.fromarray(results['final_image'])
    input_path = str(imagefile)
    output_path = "results/"+name
    return render(request, 'uploader/upload.html',{'results':results,'output_path':output_path,'input_path':input_path})