from django.shortcuts import render
from django.http import HttpResponse

from shared import dbmanager

import http.client
import json



# Create your views here.

def home (request):
    return render(request, 'app/home.html')

def favourites (request):
    return render(request, 'app/favourites.html')

def searchName(request):
    args = {}
    if request.method == "POST":
        req = request.POST.get('searchBar')

        conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")

        headers = {
            'x-rapidapi-key': "d9ef4f5324msh8ace8b2abea3cc2p18ac4ajsn03ca9ecf4926",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }

        conn.request("GET", "/auto-complete?q="+req+"&region=US", headers=headers)

        res = conn.getresponse()
        resBody= res.read()
        data = json.loads(resBody)

        i = 0
        #data.decode("utf-8")
        for exchange in data['quotes']:
            args[i] = {}
            args[i]["exchange"] = exchange['exchange']
            try:
                args[i]["name"] = exchange['longname']
            except:
                try:
                    args[i]["name"] = exchange['shortname']
                except:
                    args[i]["name"] = "Name Unavailable"
            args[i]["symbol"] = exchange['symbol']
            args[i]["type"] = exchange['quoteType']
            i += 1
        print(args)
    return render(request, 'app/searchForm.html', {'args':args})
