from django.urls import path

from . import views2

urlpatterns = [
    path('admin-signup', views2.AdminSignup.as_view()),
    path('admin-signin', views2.AdminSignin.as_view()),
    path('admin-forgot-password', views2.AdminForgotPassword.as_view()),
    path('admin-reset-password', views2.AdminResetPassword.as_view()),
]
