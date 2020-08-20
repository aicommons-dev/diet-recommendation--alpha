from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from multiselectfield import MultiSelectField


class Activity(models.Model):
    label = models.CharField(max_length=20)
    value = models.IntegerField()
    category = models.CharField(max_length=20)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.label


class Calorie(models.Model):
    food_class = models.CharField(max_length=50, blank=False)
    measurement = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=50,blank=True)
    calories = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.food_class}: {self.calories}'


class Foodservoire(models.Model):
    food_class = models.CharField(max_length=50)

    nutrient_classes = (
        (1, 'Carbohydrates'),
        (2, 'Protein'),
        (3, 'Vitamins'),
        (4, 'Fats and Oil'),
        (5, 'Mineral'),
        (6, 'Water'),
    )
    nutrients_present = MultiSelectField(choices=nutrient_classes, max_choices=6, blank=False)
    nutrients_absent = MultiSelectField(choices=nutrient_classes, max_choices=5, blank=True)
    balanced = models.BooleanField()

    def __str__(self):
        return self.food_class
