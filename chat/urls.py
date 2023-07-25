from django.urls import path, include
from chat import views
from django.contrib.auth.views import LoginView, LogoutView
 
 
urlpatterns = [
    path("", views.ChatView, name="chatview"),
    
]