# Generated by Django 4.2.7 on 2023-12-04 13:17

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Grievance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("semester", models.CharField(max_length=255)),
                ("department", models.CharField(max_length=255)),
                ("hostel", models.CharField(max_length=255)),
                ("location", models.CharField(max_length=255)),
                ("complaint_text", models.TextField()),
                ("complaint_date", models.DateTimeField(auto_now_add=True)),
                (
                    "complaint_status",
                    models.CharField(default="Pending", max_length=255),
                ),
                ("complaint_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Hostel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("vacancy", models.IntegerField()),
                ("lat", models.FloatField()),
                ("lng", models.FloatField()),
            ],
        ),
    ]
