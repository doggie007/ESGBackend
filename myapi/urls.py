from django.urls import path
from .views import ESGView, AzureAnalysis

urlpatterns = [
    path('esg/',ESGView.as_view(),name="esg"),
    path('analysis/',AzureAnalysis.as_view(),name="analysis"),
]
