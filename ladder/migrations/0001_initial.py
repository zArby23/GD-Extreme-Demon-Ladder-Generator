from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="LadderGeneration",
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
                ("session_key", models.CharField(db_index=True, max_length=40)),
                ("start", models.CharField(max_length=255)),
                ("target", models.CharField(max_length=255)),
                ("steps", models.PositiveIntegerField()),
                ("window", models.PositiveIntegerField()),
                ("result", models.JSONField()),
                ("warnings", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
