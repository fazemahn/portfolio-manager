import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime as dt
import json
import numpy as np
import pandas as pd
import pandas_datareader as pdr
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
        self.figure = plt.figure(figsize=(5,4))

        
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
    
    def plot_all(self):
        """
        Original function which generates one figure with 4 subplots made from user inputs. The 
        functions below this one separate all of the plots into their own figures.

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
        title = "Simulations 1 Day into the Future\nPDF fit results: mu = %.4f,  sigma = %.4f" % (sim_mu, sim_sig)
        plt.title(title)

        # Save the figure to HTML string ##################################################
        plt.tight_layout()
        self.figure = plt.gcf()
        
        html_str = mpld3.fig_to_html(self.figure) # saves figure to string of html

        return html_str
    
    def plot_history(self):
        """
        Function that plots the history of stock prices in the time frame set by the user.

        :returns: plot_history_str which is a string which contains the html for the graphical output.
        :rtype: str
        """

        stock_plot = self.data.plot(figsize=(5,4))
        stock_plot.set_xlabel('Date')
        stock_plot.set_ylabel('Adjusted Closing Price')
        stock_plot.set_title("Adjusted Closing Prices Over Time")

        history = plt.gcf()
        self.history = history

        plot_history_str = mpld3.fig_to_html(self.history) # saves figure to string of html
        plot_history_dict = mpld3.fig_to_dict(self.history)
        return plot_history_str, plot_history_dict

    def plot_pdf(self):
        """
        Function that plots the distribution of simulated prices of a given time step into the future.
        This histogram is fit to a Probability Density Function with the mean and standard deviation
        listed in the title.

        :returns: plot_pdf_str which is a string which contains the html for the graphical output.
        :rtype: str
        """
    
        # Histogram for the price frequencies, number of bins can be adjusted'
        fig = plt.figure(figsize=(5,4))
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
        title = "Simulations 1 Day into the Future\n(PDF fit results: mu = %.4f,  sigma = %.4f)" % (sim_mu, sim_sig)
        plt.title(title)

        plot_pdf_str = mpld3.fig_to_html(fig) # saves figure to string of html
        plot_pdf_dict = mpld3.fig_to_dict(fig)
        return plot_pdf_str, plot_pdf_dict
    
    def plot_single(self):
        """
        Function that plots the first element in each set of simulations after a given time step.
        These elements are plotted to show a single simulated projection line.

        :returns: plot_single_str which is a string which contains the html for the graphical output.
        :rtype: str
        """

        single = []
        for item in self.monte_sims:
            single.append(item[0])

        plt.figure(figsize=(5,4))
        plt.plot(single)
        plt.xlabel('Date')
        plt.ylabel('Adjusted Closing Price')
        plt.title('Simulated Adjusted Closing Prices Over Time')

        single = plt.gcf()

        plot_single_str = mpld3.fig_to_html(single) # saves figure to string of html
        plot_single_dict = mpld3.fig_to_dict(single)
        return plot_single_str, plot_single_dict
    
    def plot_multi(self):
        """
        Function that plots all of the price simualtions at each time step into the future.

        :returns: plot_multi_str which is a string which contains the html for the graphical output.
        :rtype: str
        """

        plt.figure(figsize=(5,4))
        plt.plot(self.monte_sims)
        plt.xlabel('Days into the Future')
        plt.ylabel('Adjusted Closing Price')
        title = "Monte Carlo Simulations for Adjusted Closing Prices"
        plt.title(title)

        multi = plt.gcf()

        plot_multi_str = mpld3.fig_to_html(multi) # saves figure to string of html
        plot_multi_dict = mpld3.fig_to_dict(multi)
        return plot_multi_str, plot_multi_dict
    
    def get_json(self, plot_history_dict, plot_pdf_dict, plot_single_dict, plot_multi_dict):
        """
        Function that returns the json data for the html plots.

        :returns: plot_json which is the json that contains the html strings for each plot.
        """

        plot_dict = {
            "plot_history" : plot_history_dict, 
            "plot_pdf" : plot_pdf_dict, 
            "plot_single" : plot_single_dict, 
            "plot_multi" : plot_multi_dict
        }

        plot_json = json.dumps(plot_dict, indent=4) # converts dictionary to json

        return plot_json

    def clear_figures(self):
        plt.close('all')


    '''
    def get_json(self):
        """
        Function that converts the figure to Python dictionary which is directly json-serializable.

        :returns: plot_dict
        """
        
        #plot_dict = mpld3.fig_to_dict(self.figure) # saves figure dictionary
        #plot_json = json.dumps(plot_dict, indent=4) # converts dictionary to json

        plot_history_dict = mpld3.fig_to_dict(self.plot_history)
        plot_history_json = json.dumps(plot_history_dict, indent=4)

        plot_pdf_dict = mpld3.fig_to_dict(self.plot_pdf)
        plot_pdf_json = json.dumps(plot_pdf_dict, indent=4)

        return plot_json
    '''
