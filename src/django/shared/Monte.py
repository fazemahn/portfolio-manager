import datetime as dt
import json
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import mpld3
from scipy.stats import norm


class Monte:

    def __init__(self, ticker, sim_amount, time_steps, start, end=dt.datetime.now(), data_source='yahoo'):
        """
        Initialization function for the Monte object.

        :param ticker: the ticker label associated with a stock
        :param sim_amount: the amount of simulations to be done
        :param time_steps: the number of time steps into the future the simualtion will go
        :param start: the start datetime for the simulations
        :param end: the end datetime for the simulations. Present time is default.
        :param data_source: data source from where the stock data is derived. Yahoo finance is the default.
        """

        self.ticker = ticker
        self.sim_amount = sim_amount
        self.time_steps = time_steps
        self.start = start
        self.end = end
        self.data_source = data_source
        self.data = pd.DataFrame()
        self.monte_sims = pd.DataFrame()
        self.figure = plt.figure(figsize=(16,10))
        
    def create_DataFrame(self):
        """
        Function that creates the DataFrame object where the stock data will be stored.
        """

        self.data[self.ticker] = pdr.DataReader(self.ticker, data_source=self.data_source, 
                                                start=self.start, end=self.end)['Adj Close']
    
    def simulate(self):
        """
        Function that does the necessary calculations for the simulation data.
        """
        np.random.seed(8)

        # Initial data values needed to set up the simulations.
        log_returns = np.log(1 + self.data.pct_change()) # percentage change between current and prior element
        mu = log_returns.mean() # average/mean
        var = log_returns.var() # variance
        drift = mu - (0.5 * var) # stochastic drift
        sigma = log_returns.std() # standard deviation
        daily_returns = np.exp(drift.to_numpy() + sigma.to_numpy() * norm.ppf(np.random.rand(self.time_steps, self.sim_amount)))

        # Takes last data point in stock data as as the starting point for the simulations
        initial = self.data.iloc[-1]
        self.monte_sims = np.zeros_like(daily_returns)
        self.monte_sims[0] = initial

        # Fills monte_sims with simulated prices which are pseudorandomized with daily_returns
        for t in range(1, self.time_steps):
            self.monte_sims[t] = self.monte_sims[t - 1] * daily_returns[t]

    def plot(self):
        """
        Function that sends

        :returns: html_str which is a string that contains the graphical output for the matplotlib plots
        :rtype: str
        """
        # Creating the fig object for the matplotlib canvas
        fig, axs = plt.subplots(2, 2, figsize = (16,10))
        
        # Stock Data Subplot ################################################################
        stock_plot = axs[0, 0]
        
        stock_plot.plot(self.data)
        stock_plot.set_xlabel('Date')
        stock_plot.set_ylabel('Adjusted Closing Price')
        stock_plot.set_title("Adjusted Closing Prices Over Time")

        # Single Future Price Subplot #######################################################
        plt.subplot(2,2,3)

        single = []
        for item in self.monte_sims:
            single.append(item[0])

        plt.plot(single)
        plt.xlabel('Days into the Future')
        plt.ylabel('Adjusted Closing Price')
        title = "Single Set of Simulations for Adjusted Closing Prices"
        plt.title(title)

        # Multiple Future Price Subplot #####################################################
        plt.subplot(2,2,4)

        plt.plot(self.monte_sims)
        plt.xlabel('Days into the Future')
        plt.ylabel('Adjusted Closing Price')
        title = "Monte Carlo Simulations for Adjusted Closing Prices"
        plt.title(title)

        # PDF Fit Subplot ###################################################################
        plt.subplot(2,2,2)

        # Histogram for the price frequencies, number of bins can be adjusted
        plt.hist(self.monte_sims[1], bins=10, density=True)

        # Probability Density Function
        sim_mu, sim_sig = norm.fit(self.monte_sims[1]) # Simulation mean and standard deviation values
        xmin, xmax = plt.xlim() # set the xmin and xmax along the x-axis for the pdf
        x = np.linspace(xmin, xmax)
        p = norm.pdf(x, sim_mu, sim_sig)

        # Plots frequencies of the Monte Carle simulations fit to normal distribution
        plt.plot(x, p, 'k') # normal distribution fit
        plt.xlabel('Adjusted Closing Price')
        plt.ylabel('Probability Density')
        title = "Histogram for Simulations of Adjusted Closing Price 1 Day into the Future\nPDF fit results: mu = %.4f,  sigma = %.4f" % (sim_mu, sim_sig)
        plt.title(title)

        # Save the figure to HTML string ##################################################
        plt.tight_layout()
        self.figure = plt.gcf()
        
        html_str = mpld3.fig_to_html(self.figure) # saves figure to string of html

        return html_str

    def get_json(self):
        """
        Function that converts the figure to Python dictionary which is directly json-serializable.

        :returns: plot_dict which 
        """
        
        plot_dict = mpld3.fig_to_dict(self.figure) # saves figure dictionary
        plot_json = json.dumps(plot_dict, indent=4) # converts dictionary to json

        return plot_json