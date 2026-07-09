from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_csv, name="upload_csv"),
    path("dashboard/", views.dashboard, name="dashboard_latest"),
    path("dashboard/<int:batch_id>/", views.dashboard, name="dashboard"),
]
