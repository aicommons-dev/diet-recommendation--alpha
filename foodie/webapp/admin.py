from django.contrib import admin
from .models import Foodservoire, Calorie, Activity, Disease

# Register your models here.
admin.site.register(Foodservoire)
admin.site.register(Calorie)
admin.site.register(Activity)
admin.site.register(Disease)
