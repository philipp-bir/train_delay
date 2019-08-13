from .predictions import ColumnTransform, Predictor
from .models import TrainData

import datetime
import math

def predict_train(train_id,timestamp):
    #train_id,timestamp
    departure=datetime.datetime.fromtimestamp(timestamp)
    td=TrainData.objects.get(train_id=train_id)
    season=lambda d:math.cos(2*math.pi*(d.timetuple().tm_yday)/(365+int(d.year%4==0)))
    entry={"train_id":[train_id],
           "nr_of_stations": [td.nr_of_stations],
           "dep_timestamp":[timestamp+td.departure_time_of_day],
           "weekday": [departure.weekday()],
           "season": [season(departure)],
           "duration":[td.duration]
           }
    prediction=float(p.predict(entry)[0])
    lower_end=prediction+td.interval_below
    upper_end=prediction+td.interval_above
    return {"estimate":prediction,"estimate_below":lower_end,"estimate_above":upper_end}


p=Predictor("amtrak/data/ct_dict.pickle","amtrak/data/bst.pickle")
