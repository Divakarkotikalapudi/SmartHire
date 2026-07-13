from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .analysis import analyze_resume_match
from .ats import analyze_ats
from .job_parser import parse_job_description
from .keywords import analyze_keywords
from .models import ResumeAnalysis
from .parser import parse_resume
from .recommendations import generate_recommendations
from .serializers import (
    ResumeAnalysisHistorySerializer,
    ResumeAnalysisSerializer,
)
from .utils import extract_resume_text


class ResumeAnalysisView(APIView):
    """
    Analyzes a resume against a job description.

    The user must be authenticated.

    After the analysis is completed successfully, the complete
    analysis result is saved to the database and returned to
    the frontend.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResumeAnalysisSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        resume = serializer.validated_data[
            "resume"
        ]

        job_description = serializer.validated_data[
            "job_description"
        ]

        # ---------------------------------------------------------------
        # 1. EXTRACT RESUME TEXT
        # ---------------------------------------------------------------

        resume_text = extract_resume_text(
            resume
        )

        # ---------------------------------------------------------------
        # 2. PARSE RESUME
        # ---------------------------------------------------------------

        parsed_resume = parse_resume(
            resume_text
        )

        # ---------------------------------------------------------------
        # 3. PARSE JOB DESCRIPTION
        # ---------------------------------------------------------------

        parsed_job = parse_job_description(
            job_description
        )

        # ---------------------------------------------------------------
        # 4. ATS READINESS ANALYSIS
        # ---------------------------------------------------------------

        ats_analysis = analyze_ats(
            parsed_resume
        )

        # ---------------------------------------------------------------
        # 5. JOB MATCH ANALYSIS
        # ---------------------------------------------------------------

        match_analysis = analyze_resume_match(
            parsed_resume,
            parsed_job,
        )

        # ---------------------------------------------------------------
        # 6. KEYWORD ANALYSIS
        # ---------------------------------------------------------------

        keyword_analysis = analyze_keywords(
            resume_text,
            job_description,
            parsed_job,
        )

        # ---------------------------------------------------------------
        # 7. GENERATE RECOMMENDATIONS
        # ---------------------------------------------------------------

        recommendations = generate_recommendations(
            match_analysis,
            ats_analysis,
            keyword_analysis,
        )

        # ---------------------------------------------------------------
        # 8. BUILD FINAL ANALYSIS RESULT
        # ---------------------------------------------------------------

        analysis_result = {
            "message": (
                "Resume analyzed successfully."
            ),

            "resume_name": resume.name,

            "scores": {
                "ats_readiness_score": (
                    ats_analysis[
                        "ats_readiness_score"
                    ]
                ),

                "resume_match_score": (
                    match_analysis[
                        "resume_match_score"
                    ]
                ),
            },

            "summary": {
                "ats_readiness_level": (
                    ats_analysis[
                        "readiness_level"
                    ]
                ),

                "match_level": (
                    match_analysis[
                        "match_level"
                    ]
                ),

                "top_actions": (
                    recommendations[
                        "top_actions"
                    ]
                ),
            },

            "resume_analysis": {
                "candidate": (
                    parsed_resume.get(
                        "candidate",
                        {},
                    )
                ),

                "contact": (
                    parsed_resume.get(
                        "contact",
                        {},
                    )
                ),

                "sections": (
                    parsed_resume.get(
                        "sections",
                        {},
                    )
                ),

                "parser_confidence": (
                    parsed_resume.get(
                        "parser_confidence",
                        {},
                    )
                ),
            },

            "job_analysis": parsed_job,

            "match_analysis": (
                match_analysis
            ),

            "keyword_analysis": (
                keyword_analysis
            ),

            "ats_analysis": (
                ats_analysis
            ),

            "recommendations": (
                recommendations
            ),
        }

        # ---------------------------------------------------------------
        # 9. SAVE ANALYSIS TO DATABASE
        # ---------------------------------------------------------------

        saved_analysis = ResumeAnalysis.objects.create(
            user=request.user,

            resume_name=resume.name,

            job_description=job_description,

            ats_readiness_score=(
                ats_analysis[
                    "ats_readiness_score"
                ]
            ),

            resume_match_score=(
                match_analysis[
                    "resume_match_score"
                ]
            ),

            analysis_result=analysis_result,
        )

        # Add the database ID to the response.
        # This will later allow the frontend to reopen
        # this exact saved analysis.
        analysis_result["analysis_id"] = (
            saved_analysis.id
        )

        # Keep the saved JSON result consistent with
        # the response returned to the frontend.
        saved_analysis.analysis_result = (
            analysis_result
        )

        saved_analysis.save(
            update_fields=[
                "analysis_result",
                "updated_at",
            ]
        )

        # ---------------------------------------------------------------
        # 10. RETURN RESULT TO FRONTEND
        # ---------------------------------------------------------------

        return Response(
            analysis_result,
            status=status.HTTP_201_CREATED,
        )


class ResumeAnalysisHistoryView(
    ListAPIView
):
    """
    Returns all saved analyses belonging to the
    currently authenticated user.

    The newest analysis is returned first because
    the model uses ordering = ["-created_at"].
    """

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = (
        ResumeAnalysisHistorySerializer
    )

    def get_queryset(self):
        return ResumeAnalysis.objects.filter(
            user=self.request.user
        )


class ResumeAnalysisDetailView(
    RetrieveAPIView
):
    """
    Returns one saved analysis belonging to the
    currently authenticated user.

    Filtering by request.user prevents users from
    accessing another user's analysis by changing
    the analysis ID in the URL.
    """

    permission_classes = [
        IsAuthenticated
    ]

    serializer_class = (
        ResumeAnalysisHistorySerializer
    )

    lookup_field = "pk"

    def get_queryset(self):
        return ResumeAnalysis.objects.filter(
            user=self.request.user
        )