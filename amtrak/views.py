from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from amtrak.train_predictor import predict_train
from .forms import TrainForm

import datetime
# Create your views here.

def index(request):
    #return HttpResponse('Hello from Python!')
    return render(request, "amtrak/index.html",{"form":TrainForm()})
    
def get_prediction(request,train_id,timestamp):
    prediction=predict_train(train_id,timestamp)
    return HttpResponse(f'Prediction for train #{train_id} @ {timestamp}: {prediction} minutes delayed!')
    
def prediction_post(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            d=form.cleaned_data["departure_day"]
            timestamp=int(datetime.datetime(d.year,d.month,d.day).timestamp())
            train_id=form.cleaned_data["train_id"]
            prediction=predict_train(train_id,timestamp)
            return JsonResponse(prediction)
