import pandas as pd


def same_timeseries(ts1, ts2):
    """
    return True if timeseries ts1 == timeseries ts2.

    :param ts1: pandas Dataframe object
    :param ts2: pandas Dataframe object
    :return: True if ts1 and ts2 are at least identical (Allowed Difference - 0.00001).
    """
    if len(ts1) == len(ts2):
        return (sum(ts1.values - ts2.values) < 10**-5).all()
    else:
        return False


def find_differences(bbg_df, quandl_df, match_df, csv_file_path=None):

    """
    prints or saves to csv the differences between two timeseries files.

    :param bbg_df: pandas Dataframe object
    :param quandl_df: pandas Dataframe object
    :param csv_file_path: path to save the output csv file (default=None)
    If csv_file_path is not None, will save the output to a csv file.
    :return: None.

    for each ticker find the start date of data from both sources,
    and prints True/False if prices series match since the common start date.
	
	In case one of the series (Quandl or BBG) is empty for a given ticker, will return -1 for that specific ticker.
	the ticker.

    Compare (BBG 'price' to quandl 'close price')

    CSV output example:
    
        Quandl Ticker, BBG Ticker, Quandl Start Date, BBG Start Date, Match since common start date?
        DOC US Equity , ABC, 2000-01-01, 1990-01-01, True
        ....
		....
		AYA US Equity , XYZ, 1999-01-01, 1990-01-01, False
		RME US Equity , GYS, -1, 1990-01-01, False
		WJP US Equity , AJS, -1, -1, True
        ...
        ...
        ...
        RLK US Equity , XTB, 1999-01-01, 1990-01-01, False
    
    """



    # write your code here.
    result = []

    """
    valid_match -> to filter all of the match that doesnt exist on the csv
    """
    valid_match = list(filter(lambda row: row[1][0] in quandl_df.columns and row[1][1] in bbg_df.columns, match_df.iterrows()))


    index = ["Quandl Ticker","BBG Ticker","Quandl Start Date","BBG Start Date","Match since common start date?"]

    """
    this df will store everything
    """
    big_df = pd.DataFrame([], columns=index)

    for match in valid_match:

        q_data = quandl_df[match[1][0]].reset_index().drop(["Open","High","Volume","Low"], axis=1)
        b_data = bbg_df[match[1][1]].reset_index().drop(["total_return_price"], axis=1)

        """
        I dont know if it should be OUTER JOIN or CONCAT
        The Question is unclear.
        """
        #df = q_data.merge(b_data, how="outer", left_on="Close", right_on="price")
        df = pd.concat([q_data, b_data], axis=1)


        df.fillna(-1, inplace=True)
        df["Match since common start date?"] = df["Close"] == df["price"]
        df["Quandl Ticker"] = match[1][0]
        df["BBG Ticker"] = match[1][1]
        df.drop(["Close", "price"],axis=1, inplace=True)
        df.rename({"Date": "Quandl Start Date", "index": "BBG Start Date"}, axis=1, inplace=True)
        big_df = big_df.append(df)

    
    # save csv if file path was specified:

    """
    reorder columns
    """
    big_df = big_df[index]

    big_df.to_csv(csv_file_path, index=False)

    print(big_df)

if __name__=="__main__":
    bbg_df = pd.read_csv("bbg_data_final.csv", header=[0,1], index_col=0)
    quandl_df = pd.read_csv("quandl_data_final.csv", header=[0,1], index_col=0)
    match_df = pd.read_csv("match_final.csv", header=None)
    find_differences(bbg_df, quandl_df, match_df, "output.csv")