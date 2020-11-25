from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from datetime import datetime, timedelta
from django.urls import reverse

from app.models import Comment, Stock, User, Trader, Message
import http.client
import json #to parse finance API
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    """
    """

    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def remcom(request, commID):
    """
    """

    Comment.objects.get(pk=commID).delete()
    return HttpResponse("Comment Removed")

def remfav(request, stockSymbol):
    """
    """

    # need to check if already in the list before increasing popularity
    # not done for now.
    stock = Stock.objects.filter(ticker=stockSymbol).first()
    curruser = request.user
    curruser.trader.favorites.remove(stock)
    stock.popularity -= 1
    stock.save()

    return HttpResponse("Favorite Removed")

def addfav(request, stockSymbol, stockName):
    """
    """
    
    stock = Stock.objects.filter(ticker=stockSymbol).first()
    if not stock:
        stock = Stock.objects.create(ticker=stockSymbol, name=stockName)
    curruser = request.user
    curruser.trader.favorites.remove(stock)
    stock.popularity += 1
    stock.save()
    curruser.trader.favorites.add(stock)
    print("Added To Favorites")
    return HttpResponse("Favorites are Added")

def home (request):
    """
    """
    
    #get top five stocks in descending order by popularity
    allstocks = Stock.objects.order_by('popularity').reverse()[:5]
    if request.user.is_authenticated:
        try:
            request.user.trader
        except:
            t = Trader.objects.create(user_id=request.user.id)
            t.save()
            favInfo = t.favorites.all()
            return render(request, 'app/home.html',{'topstocks': allstocks, 'sidepanels': favInfo})
        favInfo = request.user.trader.favorites.all()
        return render(request, 'app/home.html',{'topstocks': allstocks, 'sidepanels': favInfo})
    else:
        return render(request, 'app/home.html',{'topstocks': allstocks})


def favourites (request):
    """
    """

    if request.user.is_authenticated:
        comments = Comment.objects.filter(posted_by = request.user)
        favInfo = request.user.trader.favorites.order_by('id')
        discussions = Comment.objects.filter(about__in=favInfo).order_by('-posted_on')
        print(discussions)
        return render(request, 'app/favourites.html', {'content': favInfo, 'comments': comments, 'discussions': discussions})
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
    favInfo = {}
    if not stockRecord:
        stockRecord = Stock.objects.create(ticker=stockSymbol, name=stockInfo['name'])
    elif request.user.is_authenticated:
        favInfo = request.user.trader.favorites.all()
        if request.user.trader.favorites.filter(ticker=stockSymbol).first():
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

    allstocks = Stock.objects.order_by('popularity').reverse()[:5]
    return render(request, 'app/simulate.html', {'stockInfo':stockInfo, 'commentInfo':commentInfo, 'dateInfo': dateInfo, 'sidepanels': favInfo, 'topstocks': allstocks})

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

        allstocks = Stock.objects.order_by('popularity').reverse()[:5]

        if request.user.is_authenticated:
            favorites = request.user.trader.favorites.filter(ticker__in=tickerArray)
            for favorite in favorites:
                results[favorite.ticker]['isFavorite'] = True
            favInfo = request.user.trader.favorites.all()
            return render(request, 'app/searchForm.html', {'results': results, 'sidepanels': favInfo, 'topstocks': allstocks})

    return render(request, 'app/searchForm.html', {'results': results, 'topstocks': allstocks})

def messages(request):
    """
    """

    if request.method == "POST":
        try:
            recipient = User.objects.get(username=request.POST['username'])
            newmessage = Message.objects.create(text=request.POST['message_body'], sender=request.user)
            recipient.trader.messages.add(newmessage)
            return HttpResponseRedirect(reverse('app-messages'))
        except(KeyError, User.DoesNotExist):
            return HttpResponseRedirect(reverse('app-messages'))
            # return render(request, 'app/messages.html', {'error_message': "Please type correct Username"})
    messagelist = request.user.trader.messages.order_by('date').reverse()
    print(messagelist)
    # return HttpResponseRedirect(reverse('app-messages', args=({'messages': messagelist},)))
    return render(request, 'app/messages.html', {'messages': messagelist})

def remmessage(request, id):
    """
    """

    Message.objects.get(pk=id).delete()
    return HttpResponse("Message Removed")
