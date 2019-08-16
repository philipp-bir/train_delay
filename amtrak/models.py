from django.db import models

# Create your models here.

class TrainData(models.Model):
    
    train_id = models.CharField(max_length=6,unique=True)
    nr_of_stations = models.IntegerField()
    duration = models.IntegerField()
    departure_time_of_day = models.IntegerField(default=0)
    interval_below = models.FloatField()
    interval_above = models.FloatField()
    origin = models.TextField(null=True)
    destination = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.train_id} [{self.origin} - {self.destination}]"
