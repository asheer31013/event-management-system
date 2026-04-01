from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('reports/', views.organizer_report, name='organizer_report'),
    path('export-report/', views.export_report, name='export_report'),
    path('certificate/<int:registration_id>/', views.download_certificate, name='download_certificate'),
]