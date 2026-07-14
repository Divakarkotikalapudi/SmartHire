from pathlib import Path

from rest_framework import serializers

from .models import ResumeAnalysis


MAX_RESUME_FILE_SIZE = 5 * 1024 * 1024
MAX_JOB_DESCRIPTION_LENGTH = 20_000


class ResumeAnalysisSerializer(serializers.Serializer):
    """
    Validates the input required to perform a new resume analysis.
    """

    resume = serializers.FileField(
        required=True,
    )

    job_description = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=MAX_JOB_DESCRIPTION_LENGTH,
    )

    def validate_resume(self, file):
        allowed_extensions = {
            ".pdf",
            ".docx",
        }

        extension = Path(
            file.name
        ).suffix.lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        if file.size > MAX_RESUME_FILE_SIZE:
            raise serializers.ValidationError(
                "Resume file size must not exceed 5 MB."
            )

        return file

    def validate_job_description(
        self,
        value,
    ):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Job description cannot be empty."
            )

        return value


class ResumeAnalysisHistorySerializer(
    serializers.ModelSerializer
):
    """
    Serializes saved resume analyses for the History page
    and for reopening a previous analysis.
    """

    class Meta:
        model = ResumeAnalysis

        fields = (
            "id",
            "resume_name",
            "job_description",
            "ats_readiness_score",
            "resume_match_score",
            "analysis_result",
            "created_at",
            "updated_at",
        )

        read_only_fields = fields