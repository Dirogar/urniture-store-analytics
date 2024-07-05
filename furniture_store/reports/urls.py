from django.urls import path

from .views import MainPage

app_name = 'reports'

urlpatterns = [
    path('', MainPage.as_view(), name='index')
]
