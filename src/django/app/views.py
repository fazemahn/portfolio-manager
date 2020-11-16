from django.shortcuts import render
from django.http import HttpResponse
from shared import dbmanager


# Create your views here.

def home (request):
    return render(request, 'app/home.html')

def favourites (request):
    return render(request, 'app/favourites.html')