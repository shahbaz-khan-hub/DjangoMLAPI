from rest_framework import serializers
#from models import CarPricePredictionModel
from django.conf import settings

from .models import CarPricePredictionModel
from carapi.settings import INSTALLED_APPS

class CarPricePredictionModelSerializers(serializers.ModelSerializer):
    class Meta:
        model=CarPricePredictionModel
        feilds= '__all__'