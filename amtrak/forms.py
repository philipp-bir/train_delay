from django import forms

import datetime

class TrainForm(forms.Form):
    
    train_id = forms.CharField(max_length=6)
    departure_day = forms.DateField(input_formats=['%m/%d/%Y'],initial=lambda: datetime.date.today().strftime('%m/%d/%Y'))
    
    
