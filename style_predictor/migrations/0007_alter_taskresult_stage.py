# Generated by Django 5.2 on 2025-05-01 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("style_predictor", "0006_alter_taskresult_stage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskresult",
            name="stage",
            field=models.IntegerField(
                choices=[(1, "FILE_UPLOAD"), (2, "GAME"), (3, "CHESS_STYLE")], default=1
            ),
        ),
    ]
