from django.shortcuts import render
from django.http import HttpResponse

from shared import dbmanager

import http.client
import json #to parse finance API
from django.db import connection #access to default database in monte_project/settings.py



# Create your views here.

def home (request):
    return render(request, 'app/home.html')

def favourites (request):
    return render(request, 'app/favourites.html')

def simulate (request):
    stockInfo = {}
    commentInfo = {}

    if request.method == "POST":
        stockInfo['name'] = request.POST.get('stockName')
        stockInfo['symbol'] = request.POST.get('stockSymbol')

        #find all comments for the stock that was clicked on
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM comments WHERE Ticker = (%s)', (stockInfo['symbol'],))
        comments = cursor.fetchall()

        #gather all information about each comment
        i = 0
        for comment in comments:
            commentInfo[i] = {}
            commentInfo[i]["user"] = comment[0]
            commentInfo[i]["date"] = comment[2]
            commentInfo[i]["content"] = comment[3]
            i += 1
        #print(comments)
    return render(request, 'app/simulate.html', {'stockInfo':stockInfo, 'commentInfo':commentInfo})

def searchName(request):
    args = {}
    if request.method == "POST":
        req = request.POST.get('searchBar')
        #accessing yahoo finace api
        conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
        #api info
        headers = {
            'x-rapidapi-key': "d9ef4f5324msh8ace8b2abea3cc2p18ac4ajsn03ca9ecf4926",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            }

        conn.request("GET", "/auto-complete?q="+req+"&region=US", headers=headers)

        res = conn.getresponse()
        resBody= res.read()
        #json that holds all results from the auto-complete search query
        data = json.loads(resBody)
        i = 0

        #loop through the quotes dictionary to find relevant information
        #and save them as dictionaries into args
        #each dictionary in args is a different stock
        for exchange in data['quotes']:
            if exchange['quoteType'] == "EQUITY": # Only interested in equities (stocks)
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
