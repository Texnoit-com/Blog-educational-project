from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_reset/',
         PasswordResetView.as_view(template_name='users/'
                                                 'password_reset_form.html'),
         name='password_reset_form'),
    path('password_change/',
         views.PasswordChange.as_view(),
         name='password_change'),
    path('password_change/done/',
         views.Done,
         name='password_change_done'),
]
