from django.conf import settings
from django.db import models


class ResumeAnalysis(models.Model):
    """
    Stores a completed resume analysis for an authenticated user.

    The main scores are stored separately for efficient history listing,
    while the complete analysis response is stored in JSON format so the
    full results page can be reopened later.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resume_analyses",
    )

    resume_name = models.CharField(
        max_length=255,
    )

    job_description = models.TextField()

    ats_readiness_score = models.PositiveSmallIntegerField(
        default=0,
    )

    resume_match_score = models.PositiveSmallIntegerField(
        default=0,
    )

    analysis_result = models.JSONField(
        default=dict,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.resume_name} - "
            f"{self.created_at:%Y-%m-%d %H:%M}"
        )