from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .analysis import analyze_resume_match
from .ats import analyze_ats
from .job_parser import parse_job_description
from .keywords import analyze_keywords
from .parser import parse_resume
from .recommendations import generate_recommendations
from .serializers import ResumeAnalysisSerializer
from .utils import extract_resume_text


class ResumeAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResumeAnalysisSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        resume = serializer.validated_data[
            "resume"
        ]

        job_description = (
            serializer.validated_data[
                "job_description"
            ]
        )

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

        match_analysis = (
            analyze_resume_match(
                parsed_resume,
                parsed_job,
            )
        )

        # ---------------------------------------------------------------
        # 6. KEYWORD ANALYSIS
        # ---------------------------------------------------------------

        keyword_analysis = (
            analyze_keywords(
                resume_text,
                job_description,
                parsed_job,
            )
        )

        # ---------------------------------------------------------------
        # 7. GENERATE RECOMMENDATIONS
        # ---------------------------------------------------------------

        recommendations = (
            generate_recommendations(
                match_analysis,
                ats_analysis,
                keyword_analysis,
            )
        )

        # ---------------------------------------------------------------
        # 8. BUILD FINAL RESPONSE
        # ---------------------------------------------------------------

        return Response(
            {
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

                "job_analysis": (
                    parsed_job
                ),

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
            },
            status=status.HTTP_200_OK,
        )