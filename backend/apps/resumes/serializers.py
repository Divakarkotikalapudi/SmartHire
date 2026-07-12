from pathlib import Path

from rest_framework import serializers


class ResumeAnalysisSerializer(serializers.Serializer):
    resume = serializers.FileField(required=True)

    job_description = serializers.CharField(
        required=True,
        allow_blank=False,
    )

    def validate_resume(self, file):
        allowed_extensions = {".pdf", ".docx"}

        extension = Path(file.name).suffix.lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        return file