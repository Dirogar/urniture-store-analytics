from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.MainPage.as_view())
]
