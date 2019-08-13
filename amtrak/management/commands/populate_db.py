from django.core.management.base import BaseCommand, CommandError
from amtrak.models import TrainData

import csv

class Command(BaseCommand):
    help = 'Populates the traindata db.'

    def add_arguments(self, parser):
        parser.add_argument('train-data-file', type=str)

    def handle(self, *args, **options):
        TrainData.objects.all().delete()
        with open(options["train-data-file"]) as csv_file:
            csv_reader=csv.DictReader(csv_file)
            all_train_data=[]
            for row in csv_reader:
                td=TrainData(
                    train_id=row["train_id"],
                    nr_of_stations=int(row["nr_of_stations"]),
                    duration=int(row["duration"]),
                    interval_below=row["lower"],
                    interval_above=row["upper"],
                    departure_time_of_day=row["scheduled_dep_time_of_day"],
                )
                all_train_data+=[td]
            TrainData.objects.bulk_create(all_train_data)
                    
        
