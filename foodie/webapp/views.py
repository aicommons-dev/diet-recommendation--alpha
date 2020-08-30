from pyexpat import model

# import torch
from django.shortcuts import render

# Create your views here.
from fastai.basic_train import load_learner
from fastai.core import defaults
from fastai.imports import torch
from fastai.vision import open_image

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import os

from .models import Foodservoire, Activity, Disease


def home(request):
    return render(request, 'webapp/home.html')


def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        # parse the form inputs
        activity = request.POST['activity']
        disease = request.POST['disease']
        category = request.POST['category']
        height = request.POST['height']
        gender = request.POST['gender']
        age = request.POST['age']
        img = request.FILES['photo']

        # convert height from feet to cm and get calculate ideal body weight
        ideal_body_weight = (30.48 * int(height)) - 100
        activity_level = get_activity_level(activity, gender, category)
        ideal_calories = ideal_body_weight * activity_level
        idc = f'{ideal_calories:.2f}'
        calories = 'Your ideal daily calories intake is ' + idc

        # get food class from the model
        food_name = process_photo(img)
        food_obj = get_food_class(food_name)
        if food_obj is not None:
            balanced = 'Your meal is balanced. Keep it up.' if food_obj.balanced \
                else f'Your meal lacks {str(food_obj.nutrients_absent).title()} '
            desc = f'Your meal is rich in {str(food_obj.major_nutrients).title()} ' \
                   f'which is good for {food_obj.major_nutrients_functions}'
            complement = f'Your meal can be supplemented with foods rich in {str(food_obj.deficient_nutrients).title()} ' \
                         f'such as {food_obj.food_complement}. Remember to drink lots of water for proper digestion.'

            prediction = {
                'name': food_obj.food_class.title(),
                'calories': calories,
                'balanced': balanced,
                'description': desc,
                'complement': complement if food_obj.food_complement is not None else '',
                'disease': get_disease_recommendation(disease)
            }

            return render(request, 'webapp/home.html', prediction)

        return render(request, 'webapp/home.html', {'name': 'Unidentified food class. I\'ll keep learning new food '
                                                            'classes to improve my knowledge base.'})


def correct_model(file, corrected):
    g_login = GoogleAuth()
    g_login.LocalWebserverAuth()
    drive = GoogleDrive(g_login)


def get_disease_recommendation(disease):
    if disease == 'null':
        return 'No disease condition'
    dis = Disease.objects.filter(code=disease)
    dis = dis[0]
    print(dis)
    recommendation = f'You indicated {dis.name}. You should add {dis.take_nutrient} ' \
                     f'to your meals and avoid {dis.avoid_nutrient}'
    return recommendation


def get_food_class(food_class):
    food = Foodservoire.objects.filter(food_class__icontains=food_class)
    if len(food) > 0:
        return food[0]
    return None


def process_photo(img):
    # Saving the working directory and model directory
    cwd = os.getcwd()
    path = cwd + '/model'
    defaults.device = torch.device('cpu')  # set device to cpu
    # Loading the saved model using fastai's load_learner method
    model = load_learner(path, 'export.pkl')
    pred_class, pred_idx, outputs = model.predict(open_image(img))

    return str(pred_class)


def get_activity_level(label, gender, category):
    activity = Activity.objects.filter(label=label, gender=gender, category=category)
    if activity is not None:
        return activity[0].value
    return 0
