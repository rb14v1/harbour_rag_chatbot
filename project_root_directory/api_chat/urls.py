from django.urls import path

from api_chat import views

app_name = 'api_chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='chat'),
]
