from django.urls import path

from . import views


urlpatterns = [
    path('', views.AlertListCreateAPIView.as_view(), name='alert_list_create'),
    path('<int:pk>/', views.AlertRetrieveUpdateDestroyAPIView.as_view(), name='alert_retrieve_update_destroy'),
]
