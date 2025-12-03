from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .views import test_email

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', LogoutView.as_view(next_page="login"), name='logout'),
     path("test-email/", test_email, name="test_email"),
]
