from django.urls import path
from .views import buscar
from .views import buscar, home_scraper

urlpatterns = [
    path("", home_scraper, name="scraper_home"),
    path("buscar/", buscar, name="buscar"),
]
