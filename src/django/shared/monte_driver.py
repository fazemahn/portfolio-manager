from Monte import Monte
import datetime as dt
import numpy as np 
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
from scipy.stats import norm


"""
TO DO: Take proper front-end inputs to generate the user's desired output plot(s).
"""
# Placeholder example to show Monte object method implementation
mon = Monte('AMD', 100, 30, start=dt.datetime(2018,1,1), end=dt.datetime.now(), data_source='yahoo')
mon.create_DataFrame()
mon.simulate()

# creates html file of the Monte object's figure
html_str = mon.plot()
html_file = open("plots.html","w") # writes string to html file
html_file.write(html_str)
html_file.close()

# creates json file of the Monte object's figure
plot_json = mon.get_json()
json_file = open("plots.json","w")
json_file.write(plot_json)
json_file.close()
