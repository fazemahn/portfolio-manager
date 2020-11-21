from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from datetime import datetime, timedelta
from app.models import Comment, Stock, User, Trader
import http.client
import json #to parse finance API

# Create your views here.

def home (request):
    return render(request, 'app/home.html')

def favourites (request):
    return render(request, 'app/favourites.html')

def simulate (request, stockSymbol):

    conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
    #api info
    headers = {
        'x-rapidapi-key': "d9ef4f5324msh8ace8b2abea3cc2p18ac4ajsn03ca9ecf4926",
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        }

    conn.request("GET", f'/stock/v2/get-statistics?symbol={stockSymbol}&region=US', headers=headers)
    res = conn.getresponse()

    try:
        data = json.loads(res.read().decode("utf-8"))
    except:
        return render(request, 'app/error404.html')

    stockInfo = {}
    commentInfo = {}
    stockInfo['symbol'] = stockSymbol
    stockInfo['name'] = data["price"]["longName"]
    stockInfo['change'] = round(data["price"]["regularMarketChangePercent"]["raw"] * 100, 2)

    #find all comments for the stock that was clicked on

    #c = User.objects.filter(commentaboutname=l)
    comments = Comment.objects.filter(about__ticker=stockSymbol)

    #cursor = connection.cursor()
    #cursor.execute('SELECT * FROM comments WHERE Ticker = (%s)', (stockInfo['symbol'],))
    #comments = cursor.fetchall()

    #gather all information about each comment
    i = 0
    for comment in comments:
        commentInfo[i] = {}
        commentInfo[i]["user"] = str(comment.posted_by)
        commentInfo[i]["date"] = str(comment.posted_on)
        commentInfo[i]["content"] = comment.text
        i += 1
    #print(comments)
    dateInfo = {}
    dateInfo["max"] = datetime.today().strftime('%Y-%m-%d')
    dateInfo["default"] = (datetime.today() - timedelta(days=31)).strftime('%Y-%m-%d')
    dateInfo["min"] = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')


    return render(request, 'app/simulate.html', {'stockInfo':stockInfo, 'commentInfo':commentInfo, 'dateInfo': dateInfo})

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

    return render(request, 'app/searchForm.html', {'args':args})
