from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clusters/', views.get_clusters, name='get_clusters'),
    path('recommendations/<int:student_id>/', views.get_recommendations, name='get_recommendations'),
]
