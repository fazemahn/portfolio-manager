from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import Http404

from Monte import Monte
import datetime as dt
import numpy as np 
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from scipy.stats import norm


def simulate (request):
    """
    """

    if request.method == 'GET':
        print(request.GET)
        return HttpResponse("HELLO")
    return HttpResponseBadRequest()
