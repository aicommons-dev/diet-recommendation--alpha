from pyexpat import model

# import torch
from django.shortcuts import render

# Create your views here.
from fastai.basic_train import load_learner
from fastai.core import defaults
from fastai.imports import torch
from fastai.vision import open_image

import os

from .models import Foodservoire, Activity


def home(request):
    return render(request, 'webapp/home.html')


def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        # parse the form inputs
        activity = request.POST['activity']
        category = request.POST['category']
        height = request.POST['height']
        gender = request.POST['gender']
        age = request.POST['age']
        img = request.FILES['photo']

        # Ideal Calories = IdealBody weight(Kg) * Activity Level
        # Ideal Body weight = Height(cm) - 100
        # convert height from feet to cm and get calculate ideal body weight
        ideal_body_weight = (30.48 * int(height)) - 100
        activity_level = get_activity_level(activity, gender, category)
        ideal_calories = ideal_body_weight * activity_level
        idc = f'{ideal_calories:.2f}'
        calories = 'Your ideal daily calories intake is ' + idc

        # get food class from the model
        food_class = process_photo(img)
        is_balanced, absent = describe_food_class(food_class)
        print('balanced', is_balanced, absent)

        balanced = 'Your meal is balanced' if is_balanced else 'Your meal is not balanced'
        lacking = 'None' if is_balanced else 'Kindly add to your meal ' + str(absent)

        prediction = {
            'name': food_class,
            'calories': calories,
            'balanced': balanced,
            'absent': lacking
        }

        return render(request, 'webapp/home.html', prediction)

    # display empty form if new request  or filled form with error messages when an invalid was submitted
    return render(request, 'webapp/home.html')


def describe_food_class(food):
    result = Foodservoire.objects.filter(food_class__icontains=food)
    if len(result) > 0:
        return result[0].balanced, result[0].nutrients_absent
    return None, None


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
