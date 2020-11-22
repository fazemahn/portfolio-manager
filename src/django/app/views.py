from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from datetime import datetime, timedelta

from app.models import Comment, Stock, User, Trader
import http.client
import json #to parse finance API
# Create your views here.

def addfav(request, stockSymbol, stockName):
    stock = Stock.objects.filter(ticker=stockSymbol).first()
    if not stock:
        stock = Stock.objects.create(ticker=stockSymbol, name=stockName)
    curruser = request.user
    curruser.trader.favorites.add(stock)
    print("Added To Favorites")
    return HttpResponse("Favorites are Added")
    
def home (request):
    """
    """

    return render(request, 'app/home.html')

def favourites (request):
    """
    """
    return render(request, 'app/favourites.html')

def simulate (request, stockSymbol):
    """
    """

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


    stockRecord = Stock.objects.filter(ticker=stockSymbol).first()
    if not stockRecord:
        stockRecord = Stock.objects.create(ticker=stockSymbol, name=stockInfo['name'])
    elif request.user.is_authenticated and request.user.trader.favorites.filter(ticker=stockSymbol).first():
        stockInfo['isFavorite'] = True
        

    if request.method == "POST":
        Comment.objects.create(text=request.POST.get('comment_body'), posted_by=request.user, about=stockRecord)

    #find all comments for the stock that was clicked on
    comments = Comment.objects.filter(about__ticker=stockSymbol)

    #gather all information about each comment

    i = 0
    for comment in comments:
        commentInfo[i] = {}
        commentInfo[i]["user"] = str(comment.posted_by)
        commentInfo[i]["date"] = str(comment.posted_on)
        commentInfo[i]["content"] = comment.text
        i += 1
    dateInfo = {}
    dateInfo["max"] = datetime.today().strftime('%Y-%m-%d')
    dateInfo["default"] = (datetime.today() - timedelta(days=31)).strftime('%Y-%m-%d')
    dateInfo["min"] = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')


    return render(request, 'app/simulate.html', {'stockInfo':stockInfo, 'commentInfo':commentInfo, 'dateInfo': dateInfo})

def searchName(request):
    """
    """
    
    results = {}
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

        #loop through the quotes dictionary to find relevant information
        #and save them as dictionaries into args
        #each dictionary in args is a different stock
        #also save all results into stocks table. TO DO
        tickerArray = []
        for stock in data['quotes']:
            if stock['quoteType'] == "EQUITY": # Only interested in equities (stocks)
                symbol = stock['symbol']
                tickerArray.append(symbol)
                results[symbol] = {}
                results[symbol]['exchange'] = stock['exchange']
                try:
                    results[symbol]['name'] = stock['longname']
                except:
                    try:
                        results[symbol]['name'] = stock['shortname']
                    except:
                        results[symbol]['name'] = "Name Unavailable"
        if request.user.is_authenticated:
            favorites = request.user.trader.favorites.filter(ticker__in=tickerArray)
            for favorite in favorites:
                results[favorite.ticker]['isFavorite'] = True

    return render(request, 'app/searchForm.html', {'results': results})
