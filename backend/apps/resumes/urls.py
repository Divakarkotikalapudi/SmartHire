from django.urls import path

from .views import ResumeAnalysisView


app_name = "resumes"

urlpatterns = [
    path("analyze/", ResumeAnalysisView.as_view(), name="analyze"),
]