from django import forms
from .models import TrainData

import datetime

class TrainForm(forms.Form):
    
    #train_id = forms.CharField(max_length=6)
    train_id = forms.ModelChoiceField(queryset=TrainData.objects.all(),widget=forms.Select(attrs={'class': 'submit-on-change'}))
    departure_day = forms.DateField(input_formats=['%m/%d/%Y'],initial=lambda: datetime.date.today().strftime('%m/%d/%Y'),
                    widget=forms.TextInput(attrs={'class': 'submit-on-change'}))
    
    
