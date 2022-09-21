from config.views import (
                        SendPetitionView, SponsorDetailView,
                        AddStudentView, StudentFilterByStudentTypeView,
                        StudentFilterByUniversityView, StudentDetailView,
                        SponsorView, SponsorFilterByStatusAndMoneyView,
                        SponsorFilterByStatusView, SponsorFilterByMoneyView,
                        SponsorFilterByDateView, DashboardView, SponsorshipView,
                        SponsorShipDetailView
                        
                        )
from django.urls import path


urlpatterns = [
    path('send-petition/', SendPetitionView.as_view()),
    path('sponsor/<int:pk>/', SponsorDetailView.as_view()),
    path("student/", AddStudentView.as_view()),
    path('studentsbytype/<str:student_type>/',StudentFilterByStudentTypeView.as_view()),
    path('studentsbyuniver/<int:pk>/', StudentFilterByUniversityView.as_view()),
    path('student<int:pk>/', StudentDetailView.as_view()),
    path('sponsors/', SponsorView.as_view()),
    path('statistics/', DashboardView.as_view()),
    path('sponsors-filter/<str:status>/<str:sponsorship_money>/', SponsorFilterByStatusAndMoneyView.as_view()),
    path('sponsors-filter/<str:sponsorship_money>/', SponsorFilterByMoneyView.as_view()),
    path('sponsors-filter/<str:status>/', SponsorFilterByStatusView.as_view()),
    path('sponsors-filter/<str:from_date>/<str:to_date>/', SponsorFilterByDateView.as_view()),
    path('sponsorship/', SponsorshipView.as_view()),
    path('sponsorship/<int:pk>/', SponsorShipDetailView.as_view()),
    
]