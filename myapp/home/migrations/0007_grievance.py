# Generated by Django 4.2.7 on 2023-12-04 10:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0006_delete_grievance"),
    ]

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
    ]
