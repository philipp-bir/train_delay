# Generated by Django 2.2.4 on 2019-08-16 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amtrak', '0002_auto_20190813_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='traindata',
            name='destination',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='traindata',
            name='origin',
            field=models.TextField(null=True),
        ),
    ]
