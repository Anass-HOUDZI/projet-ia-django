from django.urls import path

from . import views

app_name = 'map'

urlpatterns = [
    path('', views.map_view, name='index'),
    path('api/pois/', views.api_pois, name='api_pois'),
]
