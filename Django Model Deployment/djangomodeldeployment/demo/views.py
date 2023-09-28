from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import pickle
import pandas as pd
import json
import numpy as np
from django.http import HttpResponse
from django.template import loader


# We will load the model into memory when the server starts
# and then use it to make predictions

# This is the function that will be called when a request is made to the server
# at the URL http://localhost:8000/predict
# The @csrf_exempt decorator is necessary to allow POST requests to the server
# without a CSRF token

# The objective is to predict CO2 levels
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def predict(request):
    if request.method == 'POST':
        model = pickle.load(open('model.pkl', 'rb'))
        year = int(request.POST['year'])
        co2 = float(request.POST['co2'])
        school_enrollment_primary = float(request.POST['school_enrollment_primary'])
        school_enrollment_secondary = float(request.POST['school_enrollment_secondary'])
        electric_power_consumption = float(request.POST['electric_power_consumption'])
        prediction = model.predict([[year, co2, school_enrollment_primary, school_enrollment_secondary, electric_power_consumption]])
        prediction = np.round(prediction, 2)
        return render(request, 'index.html', {'prediction': prediction})
    else:
        return render(request, 'index.html', {})