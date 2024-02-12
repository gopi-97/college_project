from django.urls import path
from .views import *
urlpatterns = [
    path("dashboard/",load_dash,name='dashboard'),
    path('Rice/',riceCultivation,name ='rice-details'),
    path('Rice-cultivation/',cultivationPractice,name ='cultivation-practice'),
    path('cropconsultants/',cropConsultants,name ='crop-consultants'),
    path('externalLinks/',externalLinks,name ='external-links'),
    path('diseasePests/',diseaseAndPests,name ='disease-pests'),
]