from django.db import models


class LadderGeneration(models.Model):
    session_key = models.CharField(max_length=40, db_index=True)
    start = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    steps = models.PositiveIntegerField()
    window = models.PositiveIntegerField()
    result = models.JSONField()
    warnings = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

