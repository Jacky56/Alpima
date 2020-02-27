import sys
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from py._xmlgen import raw


def plot_dr_ratio(portfolio_index, dr):
    """
	:param portfolio_index: pandas Dataframe object of the portfolio index
	:param dr: pandas Dataframe object of the DR ratio
	"""

    # do your magic here
    portfolio_index.plot()
    plt.show()
    dr.plot()
    plt.show()


def rolling_dr_ratio(df, rolling_window_size=200):
    """
	calculates and plots the dr ratio.
	
    :param df: the dataframe contains the daily total return price change, the weights and the portfolio index.
    :param rolling_window_size: default to 200 days.
    :return: None.
    """
    # some tests

    # calculate the rolling DR ratio
    # dr = ...

    """
    
    Portfolio_Index = 𝑝𝑜𝑟𝑡𝑓𝑜𝑙𝑖𝑜 𝑑𝑎𝑖𝑙𝑦???
    
    
    sum(Weight * std(TR_Change) )/std(Portfolio_Index)
    
    I will use numpy for this because it will be a disservice to that library if not used in this case.
    
    """

    # dr = pd.DataFrame([],columns=["Date", "Ratio"])
    # for i in range(300):
    #     time_frame = df.iloc[i:i+rolling_window_size]
    #
    #     """
    #     np.sum oddly doesnt sum all dimensions
    #     """
    #     ratio = np.sum(np.sum(np.std(time_frame["TR_Change"], axis=0) * time_frame["Weight"])) / np.std(time_frame["Portfolio_Index"])
    #     date = time_frame.index.values[-1]
    #
    #     dr = dr.append({"Date": date, "Ratio": ratio}, ignore_index=True)
    #
    #
    # print(dr.describe())
    # print(dr.())
    # # plot index and the rolling dr

    t = df["TR_Change"].rolling(rolling_window_size).apply(lambda x: np.std(x, axis=0))
    w = df["Weight"]
    p = df["Portfolio_Index"].rolling(rolling_window_size).std()

    """
    Math is correct, but fails to plot (runtime issue)
    """
    dr = (w*t).sum(axis=1) / p


    print(p.describe())
    print((w*t).sum(axis=1).describe())

    plot_dr_ratio(df["Portfolio_Index"], dr)






if __name__=="__main__":
    df = pd.read_csv("dr.csv", index_col=0, header=[0,1])
    rolling_dr_ratio(df)