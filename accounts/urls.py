from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_user, name="logout"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),

    # Invitation system
    path("send-invite/<int:receiver_id>/", views.send_invitation, name="send_invitation"),
    path("my-invitations/", views.my_invitations, name="my_invitations"),
    path("approve/<int:invite_id>/", views.approve_invitation, name="approve_invitation"),
    path("reject/<int:invite_id>/", views.reject_invitation, name="reject_invitation"),
]
