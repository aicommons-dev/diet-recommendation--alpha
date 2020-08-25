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
        food_name = process_photo(img)
        food_obj = get_food_class(food_name)
        if food_obj is not None:
            print(food_obj)
            balanced = 'Your meal is balanced' if food_obj.balanced else 'Your meal is not balanced'
            lacking = 'None' if balanced else f'Your meal lacks {food_obj.nutrients_absent}'
            desc = f'Your meal is rich in {food_obj.major_nutrients} ' \
                   f'which is good for {food_obj.major_nutrients_functions}'
            deficient = food_obj.deficient_nutrients
            complement = food_obj.food_complement

            prediction = {
                'name': food_obj.food_class,
                'calories': calories,
                'balanced': balanced,
                'description': desc,
                'absent': lacking,
                'deficient': deficient,
                'complement': complement
            }

            return render(request, 'webapp/home.html', prediction)

        return render(request, 'webapp/home.html', {'name': 'Unidentified food class. I\'m still learning new food '
                                                            'classes.'})


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
