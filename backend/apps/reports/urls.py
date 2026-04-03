from django.urls import path

from apps.analysis.views import ReportView
from .views import ComplaintGeneratorView

urlpatterns = [
    path("generate/", ComplaintGeneratorView.as_view(), name="report-generate"),
    path("<str:case_id>/", ReportView.as_view(), name="report-by-case"),
]
