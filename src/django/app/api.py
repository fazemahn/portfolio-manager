from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import Http404
from datetime import datetime, timedelta



def simulate (request):
    if request.method == 'GET':
        print(request.GET)
        return HttpResponse("HELLO")
    return HttpResponseBadRequest()

