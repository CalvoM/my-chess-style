# Generated by Django 5.2 on 2025-05-01 20:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("style_predictor", "0005_taskresult_stage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskresult",
            name="stage",
            field=models.IntegerField(
                choices=[(1, "File Upload"), (2, "Game"), (3, "Chess Style")], default=1
            ),
        ),
    ]
