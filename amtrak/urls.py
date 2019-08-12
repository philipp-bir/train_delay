from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/train-id/<slug:train_id>/timestamp/<int:timestamp>', views.get_prediction,name="json_prediction"), 
    path('predict/post',views.prediction_post,name='prediction_post'),
]
