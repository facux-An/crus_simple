from django.urls import path
from . import views

urlpatterns = [
    path('', views.listado, name='listado'),
    path('crear/', views.crear, name='crear'),
    path('<int:id>/editar/', views.editar, name='editar'),
    path('<int:id>/borrar/', views.borrar, name='borrar'),
]
