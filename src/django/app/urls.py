from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'app-home'),
    path('favourites/', views.favourites, name = 'app-favourites'),
    path('simulate/<str:stockSymbol>/', views.simulate, name = 'app-simulate'),
    path ('search/', views.searchName),

]
