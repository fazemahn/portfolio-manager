import datetime as dt
import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
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
        TO DO: Output to JSON to be passed to the front-end for presentation.
               Change output plots to whatever is desired from the front-end.

        Function that plots the output for the end user. Histogram with a PDF fit is a placeholder.
        """
        # Histogram for the price frequencies, number of bins can be adjusted
        plt.figure(figsize=(10, 6))
        plt.hist(self.monte_sims[1], bins=10, density=True)

        # simulation mean and standard deviation values
        sim_mu, sim_sig = norm.fit(self.monte_sims[1])

        # Probability Density Function
        xmin, xmax = plt.xlim() # set the xmin and xmax along the x-axis for the pdf
        x = np.linspace(xmin, xmax)
        p = norm.pdf(x, sim_mu, sim_sig)

        # Plots frequencies of the Monte Carle simulations fit to normal distribution
        plt.plot(x, p, 'k') # normal distribution fit
        plt.xlabel('Adjusted Closing Price')
        plt.ylabel('Probability Density')
        title = "Histogram for 100 Simulations of Adjusted Closing Price 1 Day into the Future\nPDF fit results: mu = %.4f,  sigma = %.4f" % (sim_mu, sim_sig)
        plt.title(title)
        plt.show()
