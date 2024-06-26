from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    #path("flight-status", views.get_flight, name = "flight-stats"),
    path("", views.get_flight, name = "flight-stats2"),
    path("flight-status2", views.get_flight, name = "flight-stats2"),
    path('weather/<str:airport>/', views.weather, name='weather'),
    path('get-airlines', views.get_all_flights, name = "get-flights-airlines"),
    path('flight/<str:flight_number>', views.flight_info, name = "flights-stats3"),
    #path('flight/<str:flight_number>/', views.flight_detail, name='flight_detail'),
]