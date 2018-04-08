from django.shortcuts import render
from django.conf import settings
from .models import ImageModel
from .forms import ImageForm
import matplotlib.pyplot as plt
from predictor import predict,plot_hist
import time
import random
import numpy as np
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

def compare_scans(request):
    last_two_scans = ImageModel.objects.all().order_by('-id')[:2]
    print(last_two_scans)
    file1 = last_two_scans[0].get_name()
    file2 = last_two_scans[1].get_name()
    path1 = "/home/prajwala/Videos/oct_analyzer"+settings.MEDIA_URL+file1
    path2 = "/home/prajwala/Videos/oct_analyzer"+settings.MEDIA_URL+file2
    results_path =  "/home/prajwala/Videos/oct_analyzer"+settings.MEDIA_URL+"results/"
    first,name1 = file1.split("/")
    first,name2 = file2.split("/")
    result1 = predict(path1,results_path,name1)
    result2 = predict(path2,results_path,name2)
    context = {'file1':file1,'file2':file2}
    results = {'result1':result1,'result2':result2}
    
    plot_hist(result1,result2)
    return render(request,'uploader/compare.html',{'context':context,'results':results})