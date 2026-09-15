from rest_framework import serializers

from ladder.models import LadderGeneration


class LadderRequestSerializer(serializers.Serializer):
    start = serializers.CharField(max_length=255)
    target = serializers.CharField(max_length=255)
    steps = serializers.IntegerField(min_value=1)
    window = serializers.IntegerField(min_value=0, default=5)


class LadderGenerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LadderGeneration
        fields = (
            "id",
            "start",
            "target",
            "steps",
            "window",
            "result",
            "warnings",
            "created_at",
        )
