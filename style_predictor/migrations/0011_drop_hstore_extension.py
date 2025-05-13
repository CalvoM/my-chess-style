from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("style_predictor", "0010_alter_taskresult_result"),
    ]

    operations = [
        migrations.RunSQL(
            sql="DROP EXTENSION IF EXISTS hstore;",
            reverse_sql="CREATE EXTENSION IF NOT EXISTS hstore;",
        ),
    ]
