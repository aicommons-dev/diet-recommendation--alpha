from pyexpat import model

# import torch
from django.shortcuts import render, redirect


# Create your views here.
from fastai.basic_train import load_learner
from fastai.core import defaults
from fastai.imports import torch
from fastai.vision import open_image

import os


def home(request):
    return render(request, 'webapp/home.html')


def dashboard(request):
    return render(request, 'webapp/dashboard.html')


def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        img = request.FILES['photo']
        img_pred = process_photo(img)
        print(img_pred)

        return redirect('home')

    # display empty form if new request  or filled form with error messages when an invalid was submitted
    return render(request, 'webapp/home.html')


def process_photo(img):
    # Saving the working directory and model directory
    cwd = os.getcwd()
    path = cwd + '/model'
    defaults.device = torch.device('cpu')  # set device to cpu
    # Loading the saved model using fastai's load_learner method
    model = load_learner(path, 'export.pkl')
    pred_class, pred_idx, outputs = model.predict(open_image(img))
    # pred_class, pred_idx, outputs = model.predict(img)
    return str(pred_class)


def register_user(request):
    pass
