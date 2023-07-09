from django.shortcuts import render
import joblib
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from rest_framework import viewsets
from django.core import serializers
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from carmodel.serializer import CarPricePredictionModelSerializers
from . forms import CarPricePredictionForm
from carmodel.forms import CarPricePredictionForm
from sklearn.linear_model import LinearRegression
from . models import CarPricePredictionModel
import pandas as pd
import numpy as np
from sklearn import preprocessing
from collections import defaultdict, Counter

class carsView(viewsets.ModelViewSet):
	queryset = CarPricePredictionModel.objects.all()
	serializer_class =  CarPricePredictionModelSerializers

def process_form(request):
    if request.method == 'POST':
        form = CarPricePredictionForm(request.POST)
        if form.is_valid():
            # Get the form data
        
            engine_capacity = form.cleaned_data['engine_capacity']
            model_year= form.cleaned_data['model_year']
            mileage = form.cleaned_data['mileage']
            company = form.cleaned_data['company']
            variant = form.cleaned_data['variant']
            engine_type = form.cleaned_data['engine_type']
            transmission = form.cleaned_data['transmission']
            body_type = form.cleaned_data['body_type']
            myDict = {
                'engine_capacity': [engine_capacity],
                'model_year': [model_year],
                'mileage': [mileage],
                'company': [company],
                'variant': [variant],
                'engine_type': [engine_type],
                'transmission': [transmission],
                'body_type': [body_type]
                }
            # Load the ML model and make predictions
            predictions = load_and_predict(myDict)
            messages.success(request,'Estimated price: {}'.format(predictions))

            return render(request,'myform/form.html',{'form':form})
    else:
         form = CarPricePredictionForm()
    return render(request,'myform/form.html',{'form':form})     

def load_and_predict(car_features):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the pickle file
    pickle_file = os.path.join(BASE_DIR, 'price_module.pkl')
    with open(pickle_file, 'rb') as file:
        model = pickle.load(file)

    df = pd.DataFrame([car_features])  # Create a DataFrame with the form data

    # Perform label encoding on specific columns
    encoded_df = perform_label_encoding(df, ['company', 'variant'])

    # Make predictions using the loaded model
    predictions = model.predict(encoded_df)

    return predictions

def perform_label_encoding(df, columns):
    # Perform label encoding on the specified columns
    encoded_df = df.copy()
    
    for column in columns:
        if column in encoded_df:
            label_encoder = encoded_df[column]
            encoded_df[column] = label_encoder.transform(encoded_df[column])
    
    return encoded_df




