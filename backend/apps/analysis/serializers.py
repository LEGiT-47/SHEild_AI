from rest_framework import serializers


class AnalyzeUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    user_id = serializers.CharField(required=False, allow_blank=True)


class AnalysisResponseSerializer(serializers.Serializer):
    case_id = serializers.CharField()
    verdict = serializers.ChoiceField(choices=["DEEPFAKE", "AUTHENTIC"])
    is_fake = serializers.BooleanField()
    confidence = serializers.FloatField()
    risk_level = serializers.ChoiceField(choices=["HIGH", "MEDIUM", "LOW"])
    artifacts = serializers.ListField(child=serializers.CharField())
    traceability = serializers.ListField(child=serializers.DictField())
    action_steps = serializers.ListField(child=serializers.CharField())
    file_url = serializers.CharField()
    analyzed_at = serializers.DateTimeField()
