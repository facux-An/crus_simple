from django.urls import path
from .views import home_scraper, buscar

urlpatterns = [
    path("", home_scraper, name="scraper_home"),
    path("buscar/", buscar, name="buscar"),
]
