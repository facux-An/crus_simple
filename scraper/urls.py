from django.urls import path
from . import views

urlpatterns = [
    path('', views.scrape_view, name='scrape'),
]
