# Generated by Django 2.2.4 on 2019-08-13 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amtrak', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='traindata',
            name='departure_time_of_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='traindata',
            name='train_id',
            field=models.CharField(max_length=6, unique=True),
        ),
    ]
