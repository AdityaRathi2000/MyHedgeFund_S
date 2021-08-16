import pandas as pd
import datetime as dt
import numpy as np
import time
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import urllib.request as webInfo
import plotly.figure_factory as ff
import requests
from bs4 import BeautifulSoup
import MHF_fundamentals as mhf_f
import warnings
warnings.filterwarnings("ignore")

#streamlit run /Users/adityarathi/PycharmProjects/new_MHF/main.py

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.title('Welcome to MyHedgeFund')

    ticker_input = st.text_input("Please enter ticker symbol of company you are interested in", '')
    start_day = 1
    start_month = 1  # date.strftime("%B")
    start_year = 2020

    req_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    sector_industry_list = mhf_f.sector_industry(ticker_input, req_headers)
    if (ticker_input != ''):
        st.write("**{}** is part of **{}** sector and **{}** industry".format(ticker_input, sector_industry_list[0],
                                                                          sector_industry_list[1]))

        ############################################################################################
        ############################################################################################
        ############################################################################################
        start = dt.datetime(start_year, start_month, start_day)
        end = dt.datetime.now().date()
        end_diff_format = end.strftime('%m/%d/%Y')
        year = start_year

        sector_var = ""
        industry_var = ""

        tracking_fundamentals = ["Total Revenue", "Gross Profit", "Operating Expense", "Operating Income", \
                                 "Basic EPS", "Normalized Income", "EBIT"]
        globalResultsDict = {}
        for i in tracking_fundamentals:
            globalResultsDict[i] = 0

        st.write("# *FINANCIALS*")
        df_financials = mhf_f.financial_table(ticker_input, end_diff_format, req_headers)
        st.write(df_financials)

        mhf_f.four_year_increasing(df_financials, "Total Revenue", globalResultsDict)
        # st.write("**{}: ({})**".format("Total Revenue", globalResultsDict["Total Revenue"]))

        mhf_f.four_year_increasing(df_financials, "Gross Profit", globalResultsDict)
        mhf_f.four_year_decreasing(df_financials, "Operating Expense", globalResultsDict)
        mhf_f.four_year_increasing(df_financials, "Operating Income", globalResultsDict)
        mhf_f.four_year_increasing_noTTM(df_financials, "Basic EPS", globalResultsDict)
        mhf_f.four_year_increasing(df_financials, "Normalized Income", globalResultsDict)
        mhf_f.four_year_increasing(df_financials, "EBIT", globalResultsDict)

        st.write("# *Peer Analysis*")
        competitor_df = mhf_f.competitor_func(ticker_input, req_headers)
        st.table(competitor_df)

        st.write("# *Current Affairs*")
        news_df, df_1 = mhf_f.news_df_create(ticker_input, req_headers)
        st.write(df_1, unsafe_allow_html=True)

        st.write("# *Insider Trading*")
        insider_df = mhf_f.insider_df_creation(ticker_input, req_headers)
        st.table(insider_df)

        st.write("# *ETF Exposure*")
        etf_df = mhf_f.etf_exposure_create(ticker_input, req_headers)
        st.table(etf_df)

        ############################################################################################
        ############################################################################################
        ############################################################################################