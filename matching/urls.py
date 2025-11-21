from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='matching_home'),

    # clusters + recommendations + graph
    path('clusters/', views.show_clusters, name='matching_clusters'),
    path('recommendations/<int:student_id>/', views.show_recommendations, name='matching_recommendations'),
    path('graph/', views.show_graph, name='matching_graph'),

    path('invitations/', views.show_invitations, name='invitations'),
    path('invitations/respond/<int:invite_id>/<str:action>/', views.respond_invitation, name='respond_invitation'),

    path('student/<int:user_id>/', views.view_student_profile, name='student_profile'),


]
