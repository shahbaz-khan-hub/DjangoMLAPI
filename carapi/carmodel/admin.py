from django.contrib import admin
from carmodel.models import CarPricePredictionModel
# Register your models here
def new_func():
    admin.site.register(CarPricePredictionModel)

new_func()