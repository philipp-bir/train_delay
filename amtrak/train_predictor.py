from .predictions import ColumnTransform, Predictor
import datetime
import math

def predict_train(train_id,timestamp):
    #train_id,timestamp
    departure=datetime.datetime.fromtimestamp(timestamp)
    season=lambda d:math.cos(2*math.pi*(d.timetuple().tm_yday)/(365+int(d.year%4==0)))
    entry={"train_id":[train_id], "nr_of_stations": [20], "dep_timestamp":[timestamp], "weekday": [departure.weekday()], "season": [season(departure)], "duration":[6*3600]}
    return {"estimate":float(p.predict(entry)[0])}


p=Predictor("amtrak/ct_dict.pickle","amtrak/bst.pickle")
