from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Root URL mapped to home view
    path('chatbot/', views.chatbot, name='chatbot'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('chatbot/logout/', views.logout, name='logout'),
]
