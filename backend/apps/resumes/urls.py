from django.urls import path

from .views import (
    ResumeAnalysisDetailView,
    ResumeAnalysisHistoryView,
    ResumeAnalysisView,
)


app_name = "resumes"


urlpatterns = [
    # Create a new resume analysis
    path(
        "analyze/",
        ResumeAnalysisView.as_view(),
        name="analyze",
    ),

    # Get all analyses belonging to the logged-in user
    path(
        "history/",
        ResumeAnalysisHistoryView.as_view(),
        name="history",
    ),

    # Get one specific analysis belonging to the logged-in user
    path(
        "history/<int:pk>/",
        ResumeAnalysisDetailView.as_view(),
        name="analysis-detail",
    ),
]