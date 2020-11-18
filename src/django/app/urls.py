from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'app-home'),
    path('favourites/', views.favourites, name = 'app-favourites'),
    path ('search/', views.searchName, name = 'app-search'),
    path('simulate/<str:stockSymbol>/', views.simulate, name = 'app-simulate'),

]
