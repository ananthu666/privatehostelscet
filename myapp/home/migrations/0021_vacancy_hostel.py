# Generated by Django 5.0.6 on 2024-07-12 20:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_vacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='hostel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.hostel'),
        ),
    ]
