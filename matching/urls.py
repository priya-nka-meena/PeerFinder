# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('clusters/', views.get_clusters, name='get_clusters'),
#     path('recommendations/<int:student_id>/', views.get_recommendations, name='get_recommendations'),
# ]

#new after db
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='matching_home'),  
    path('clusters/', views.show_clusters, name='matching_clusters'),
    path('recommendations/<int:student_id>/', views.show_recommendations, name='matching_recommendations'),
    path('graph/', views.show_graph, name='matching_graph'),
]

