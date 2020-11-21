from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.home, name = 'app-home'),
    path('favourites/', views.favourites, name = 'app-favourites'),
    path ('search/', views.searchName, name = 'app-search'),
    path('simulate/<str:stockSymbol>/', views.simulate, name = 'app-simulate'),
    path ('search/', views.searchName),
    path('api/simulate', api.simulate, name = 'api-simulate')

]
