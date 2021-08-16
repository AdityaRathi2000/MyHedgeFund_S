import pandas as pd
import datetime as dt
import numpy as np
import time
import matplotlib.pyplot as plt
import urllib.request as webInfo
import requests
from bs4 import BeautifulSoup
import streamlit as st
import warnings
warnings.filterwarnings("ignore")
import altair as alt
import math

# Section 2
def financial_table(ticker, end_diff_format, req_headers):
    financials = 'https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    with requests.Session() as s:
        url = financials
        r = s.get(url, headers=req_headers)
    soup_is = BeautifulSoup(r.content, 'lxml')

    all_titls = soup_is.find_all('div', class_='D(tbr)')
    if (len(all_titls) == 0):
        print("Data for {} is currently unavailable, plrease try again later!".format(ticker))
        return pd.DataFrame()

    column_titles = []
    temp_list = []
    final = []
    index = 0
    for title in all_titls[0].find_all('div', class_='D(ib)'):
        column_titles.append(title.text)
    while index <= len(all_titls)-1:
        temp = all_titls[index].find_all('div', class_='D(tbc)')
        for line in temp:
            temp_list.append(line.text)
        final.append(temp_list)
        temp_list = []
        index+=1

    df = pd.DataFrame(final[1:])
    df.columns = column_titles
    #df = df[:-5]
    df = df.T

    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header

    df_1 = df.rename(columns = {'Breakdown': 'Year'}, inplace = False)
    df_1.index.name = '' # Remove the index name
    df_1.rename(index={'ttm': end_diff_format},inplace=True) #Rename ttm in index columns to end of the year
    df_1 = df_1.reset_index()
    df_1 = df_1.rename(columns = {'': 'Year'}, inplace = False)
    df_1["Year"] = df_1["Year"].apply(lambda x: dt.datetime.strptime(str(x), '%m/%d/%Y'))
    df_1["Year"] = df_1["Year"].apply(lambda x: x.year)
    return df_1

# Section 3
def sector_industry(ticker, req_headers):
    sector_var = ""
    industry_var = ""

    # Sector
    sector = 'https://finance.yahoo.com/quote/' + ticker + '/profile?p=' + ticker

    with requests.Session() as s:
        url = sector
        r = s.get(url, headers=req_headers)
    soup_is = BeautifulSoup(r.content, 'html.parser')

    chooser = 0
    for g in soup_is.find_all('p', attrs={'class': 'D(ib) Va(t)'}):
        for spans in g.find_all('span'):
            if (chooser == 0):
                chooser += 1
                continue;
            elif (chooser == 1):
                chooser += 1
                sector_var = spans.text
                continue;
            elif (chooser == 2):
                chooser += 1
                continue;
            elif (chooser == 3):
                chooser += 1
                industry_var = spans.text
                continue;
    return [sector_var, industry_var]

# Section 4
def roe_roa(ticker, req_headers):
    ## ROE
    key_stats = 'https://finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker
    roa = ""
    roe = ""

    with requests.Session() as s:
        url = key_stats
        r = s.get(url, headers=req_headers)
    soup_is = BeautifulSoup(r.content, 'html.parser')

    counter = 0
    finding = soup_is.find('div', attrs={'class': 'Mb(10px) Pend(20px) smartphone_Pend(0px)'})
    if (finding is None): return ['0%','0%']
    for each in finding.find_all('td', attrs={'class': "Fw(500) Ta(end) Pstart(10px) Miw(60px)"}):
        if (counter == 0):
            counter+=1
            continue
        elif (counter == 1):
            counter+=1
            continue
        elif (counter == 2):
            counter+=1
            continue
        elif (counter == 3):
            counter+=1
            continue
        elif (counter == 4):
            counter+=1
            roa = each.text
            continue
        elif (counter == 5):
            counter+=1
            roe = each.text
            continue
        else:
            break
    return [roa, roe]

# Section 5.1
def four_year_increasing(df, title, globalResultsDict):
    st.write("**{}**".format(title))

    df_small = df[["Year", title]][::-1]
    df_small[title] = df_small[title].apply(lambda x: int(float(x.replace(',', '').replace('-', '0'))))

    bar_chart = alt.Chart(df_small).mark_bar(size=50).encode(
        x=alt.X('Year:O', axis=alt.Axis(tickCount=df.shape[0])),
        y=title
    ).properties(
        title=title,
        width=700,
        height=350
    )
    st.altair_chart(bar_chart)

    m, b = np.polyfit(df_small["Year"], df_small[title], 1)
    globalResultsDict[title] = "Sell"  # sell signal
    if m > 0:
        globalResultsDict[title] = "Buy"



# Section 5.2
def four_year_increasing_noTTM(df, title, globalResultsDict):
    st.write("**{}**".format(title))

    df_small = df[["Year", title]][1:5]
    df_small = df_small[::-1]
    df_small[title] = df_small[title].apply(lambda x: int(float(x.replace(',', '').replace('-', '0'))))

    bar_chart = alt.Chart(df_small).mark_bar(size=50).encode(
        x=alt.X('Year:O', axis=alt.Axis(tickCount=df.shape[0])),
        y=title
    ).properties(
        title=title,
        width=700,
        height=350
    )
    st.altair_chart(bar_chart)

    m, b = np.polyfit(df_small["Year"], df_small[title], 1)

    globalResultsDict[title] = "Sell"  # sell signal
    if m > 0:
        globalResultsDict[title] = "Buy"

# Section 5.3
def four_year_decreasing(df, title, globalResultsDict):
    st.write("**{}**".format(title))

    df_small = df[["Year", title]][::-1]
    df_small[title] = df_small[title].apply(lambda x: int(float(x.replace(',', '').replace('-', '0'))))

    bar_chart = alt.Chart(df_small).mark_bar(size=50).encode(
        x=alt.X('Year:O', axis=alt.Axis(tickCount=df.shape[0])),
        y=title
    ).properties(
        title=title,
        width=700,
        height=350
    )
    st.altair_chart(bar_chart)

    m, b = np.polyfit(df_small["Year"], df_small[title], 1)

    globalResultsDict[title] = "Sell"  # sell signal
    if m < 0:
        globalResultsDict[title] = "Buy"


# Section 6
# Getting competitors
def competitor_func(ticker, req_headers):
    competitors = 'https://csimarket.com/stocks/competitionNO3.php?code={}'.format(ticker)
    with requests.Session() as s:
        url = competitors
        r = s.get(url, headers=req_headers)
    soup_is = BeautifulSoup(r.content, 'html.parser')

    competitor_list = []
    for v_1 in soup_is.find_all('table', attrs={'class': 'osnovna_tablica_bez_gifa'}):
        for v_2 in v_1.find_all('tr', attrs={'onmouseover': "this.className='bgplv'"}):
            for v_3 in v_2.find_all('td', attrs={'class': "plavat svjetlirub dae al"}):
                competitor_list.append(v_3.text)

    #COMPARISONS
    watchList_comps = competitor_list[0:5]
    watchList_comps.append(ticker)

    compare_list = ['Trailing P/E', 'Forward P/E', 'PEG Ratio (5 yr expected)', 'Price/Sales (ttm)', 'Price/Book (mrq)', 'Enterprise Value/Revenue', 'Enterprise Value/EBITDA', 'Return on Assets(%)', 'Return on Equity(%)']
    competitor_df = pd.DataFrame(compare_list)

    for i in watchList_comps:
      comparisons = 'https://finance.yahoo.com/quote/' + i + '/key-statistics?p=' + i
      with requests.Session() as s:
          url = comparisons
          try:
            r = s.get(url, headers=req_headers)
          except:
            time.sleep(10)
            r = s.get(url, headers=req_headers)

      soup_is = BeautifulSoup(r.content, 'html.parser')
      data_list = []
      ent_skipper = 0
      for g in soup_is.find_all('tr', attrs={'class': 'Bxz(bb) H(36px) BdB Bdbc($seperatorColor) fi-row Bgc($hoverBgColor):h'}):
        if (len(g) == 0): break
        for forward_pe in g.find_all('td', attrs={'class': "Fw(500) Ta(end) Pstart(10px) Miw(60px)"}):
          data_stock = forward_pe.text
          if(ent_skipper == 0):
            ent_skipper+=1
            break
          if(data_stock == "N/A"):
              data_stock = 0;
          data_list.append(float(str(data_stock).replace(',','')))
      roa_roe_list = roe_roa(i, req_headers)
      data_list.append(float(roa_roe_list[0].replace('N/A','0').replace('%','')))
      data_list.append(float(roa_roe_list[1].replace('N/A','0').replace('%','')))

      if (len(competitor_df) != len(data_list)):
          continue;

      competitor_df[i] = data_list

    competitor_df["Peer Average"] = competitor_df.mean(axis=1).apply(lambda x: round(x, 2))
    competitor_df["Peer Median"] = competitor_df.median(axis=1).apply(lambda x: round(x, 2))
    return competitor_df

# Section 7
def news_df_create(ticker, req_headers):
    news = 'https://www.marketwatch.com/investing/stock/' + ticker
    with requests.Session() as s:
        url = news
        r = s.get(url, headers=req_headers)
    soup_is = BeautifulSoup(r.content, 'html.parser')

    news_list = []
    for roe in soup_is.find_all('div', attrs={'class': 'collection__elements j-scrollElement'}):
        for ro_1 in roe.find_all('div'):
            for a in ro_1.find_all('a', attrs={'class': 'figure__image'}):

                img = a.find('img', alt=True)
                if (img is not None and img['alt'] == 'Read full story'):
                    news_list.append(a['href'])

    # Headlines
    headlines = []
    relevant_h = news_list[0:5];
    for article in relevant_h:
        with requests.Session() as s:
            url = article
            r = s.get(url, headers=req_headers)
        soup_is = BeautifulSoup(r.content, 'html.parser')

        for headline in soup_is.find_all('h1', attrs={'class': 'article__headline'}):
            headlines.append(headline.text)

    # DF
    news_df = pd.DataFrame()
    news_df["Headline"] = headlines
    news_df["Article Link"] = relevant_h
    news_df["Positivity Score"] = np.array(1)

    news_df['Article Link'] = news_df['Article Link'].apply(lambda x: f'<a target="_blank" href="{x}">Link</a>')
    news_df["Headline"] = news_df["Headline"].apply(lambda x: x.replace('\n', ""))
    df = news_df.to_html(escape=False)
    return news_df, df

def insider_df_creation(ticker, req_headers):
    insiders = 'http://openinsider.com/screener?s={}&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'.format(
        ticker)
    with requests.Session() as s:
        url = insiders
        try:
            r = s.get(url, headers=req_headers)
        except:
            time.sleep(5)
            r = s.get(url, headers=req_headers)

    soup_is = BeautifulSoup(r.content, 'html.parser')
    insider_columns = ['Filing Date', 'Trade Date', 'Ticker', 'Insider Name', 'Title', 'Trade Type', 'Price', 'Qty',
                       'Owned', 'Own', 'Value']

    insider_df = pd.DataFrame(columns=insider_columns)
    skip = 0
    for trades in soup_is.find_all('table', attrs={'class': 'tinytable'}):
        for trs in trades.find_all('tr'):
            curr_list = []
            for tds in trs.find_all('td'):
                if (len(tds.text) > 1):
                    curr_list.append(tds.text)
            if (len(curr_list) == len(insider_columns)):
                insider_df.loc[len(insider_df)] = curr_list

    indices_to_remove = []
    for idx, i in insider_df.iterrows():
        if (str(i['Ticker']).replace(' ', '') != ticker):
            indices_to_remove.append(idx)

    insider_df = insider_df.drop(indices_to_remove)
    insider_df["Trade Date"] = insider_df["Trade Date"].apply(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))
    insider_df_curr_year = insider_df[insider_df["Trade Date"].apply(lambda x: x.year == dt.datetime.now().year)]
    if (insider_df_curr_year.empty):
        return pd.DataFrame()
    insider_df_curr_year['Qty'] = insider_df_curr_year['Qty'].apply(lambda x: round(float(x.replace(',', '')), 2))
    insider_df_curr_year.loc[insider_df_curr_year['Qty'] <= 0, 'Type'] = 'Sale'
    insider_df_curr_year.loc[insider_df_curr_year['Qty'] > 0, 'Type'] = 'Buy'
    insider_df_curr_year_small = insider_df_curr_year[
        ["Trade Date", "Insider Name", "Title", "Type", "Price", "Qty", "Owned", "Own", "Value"]]
    insider_df_curr_year_small = insider_df_curr_year_small[0:10]

    insider_df_curr_year_small["Trade Date"] = insider_df_curr_year_small["Trade Date"].apply(lambda x: "{} {}".format(x.strftime('%B')[0:3], x.year))
    return insider_df_curr_year_small

def etf_exposure_create(ticker, req_headers):
    etf_exposure = 'https://etfdb.com/stock/{}/'.format(ticker)
    with requests.Session() as s:
        url = etf_exposure
        r = s.get(url, headers=req_headers)
    soup_is = BeautifulSoup(r.content, 'html.parser')

    ticker_list = []
    etf_name_list = []
    category_list = []
    expense_ratio_list = []
    weightage_list = []
    for etf_finder in soup_is.find_all('table', attrs={
        'class': 'table mm-mobile-table table-module2 table-default table-striped table-hover table-pagination'}):
        for tbody in etf_finder.find_all('tbody'):
            for tr in tbody.find_all('tr'):
                if (tr.find("td", attrs={'data-th': 'Ticker'}).a is not None):
                    ticker = tr.find("td", attrs={'data-th': 'Ticker'}).a.text
                else:
                    ticker = tr.find("td", attrs={'data-th': 'Ticker'}).text
                if (tr.find("td", attrs={'data-th': 'ETF'}).a is not None):
                    etf_name = tr.find("td", attrs={'data-th': 'ETF'}).a.text
                else:
                    etf_name = tr.find("td", attrs={'data-th': 'ETF'}).text
                if (tr.find("td", attrs={'data-th': 'ETFdb.com Category'}).a is not None):
                    category = tr.find("td", attrs={'data-th': 'ETFdb.com Category'}).a.text
                else:
                    category = tr.find("td", attrs={'data-th': 'ETFdb.com Category'}).text
                if (tr.find("td", attrs={'data-th': 'Expense Ratio'}).a is not None):
                    expense_ratio = tr.find("td", attrs={'data-th': 'Expense Ratio'}).a.text
                else:
                    expense_ratio = tr.find("td", attrs={'data-th': 'Expense Ratio'}).text
                if (tr.find("td", attrs={'data-th': 'Weighting'}).a is not None):
                    weightage = tr.find("td", attrs={'data-th': 'Weighting'}).a.text
                else:
                    weightage = tr.find("td", attrs={'data-th': 'Weighting'}).text
                ticker_list.append(ticker)
                etf_name_list.append(etf_name)
                category_list.append(category)
                expense_ratio_list.append(expense_ratio)
                weightage_list.append(weightage)

    ETF_exposure_df = pd.DataFrame()
    ETF_exposure_df['Ticker'] = ticker_list
    ETF_exposure_df['ETF Name'] = etf_name_list
    ETF_exposure_df['Category'] = category_list
    ETF_exposure_df['Expense Ratio'] = expense_ratio_list
    ETF_exposure_df['Weightage'] = weightage_list

    ETF_exposure_df_10 = ETF_exposure_df[0:10]
    return ETF_exposure_df_10

def analytics_helper(avg, med, switcher_avg, switcher_med):
    if (switcher_avg == "<g>greater</g>" and switcher_med == "<r>greater</r>" and avg > 100 or med > 100): return "<g>Buy</g> (But too high - kinda risky, kinda sus)"
    if (switcher_avg == "<g>greater</g>" and switcher_med == "<g>greater</g>"): return "<g>Buy</g>"
    if (switcher_avg == "<r>lesser</r>" and switcher_med == "<g>greater</g>" and avg < 2 and med > 5): return "<g>Buy</g>"
    if (switcher_avg == "<g>greater</g>" and switcher_med == "<r>lesser</r>" and avg > 5 and med < 2): return "<g>Buy</g>"
    return "<r>Sell</r>"

def competitor_analysis(df, ticker):
    new_df = df[[ticker, "Peer Average", "Peer Median"]]
    information_list = ['Trailing P/E', 'Forward P/E', 'PEG Ratio (5 yr expected)', 'Price/Sales (ttm)', 'Price/Book (mrq)','Enterprise Value/Revenue', 'Enterprise Value/EBITDA', 'Return on Assets(%)', 'Return on Equity(%)']
    results_list = []

    switcher_avg = ""
    switcher_med = ""
    for i in range(len(information_list)):
        new = new_df.at[i,ticker]
        old_avg = new_df.at[i,"Peer Average"]
        old_median = new_df.at[i, "Peer Median"]
        avg_per = (new - old_avg)/(old_avg) * 100
        median_per = (new - old_median) / (old_median) * 100
        if (avg_per < 0):
            switcher_avg = "<r>lesser</r>"
        elif (avg_per >= 0):
            switcher_avg = "<g>greater</g>"
        if (median_per < 0):
            switcher_med = "<r>lesser</r>"
        elif (median_per >= 0):
            switcher_med = "<g>greater</g>"
        results_list.append("{} {} is <strong>{}%</strong> {} than industry average, and <strong>{}%</strong> {} than industry median --> {}".format(ticker, information_list[i], round(abs(avg_per),2), switcher_avg, round(abs(median_per),2), switcher_med, analytics_helper(abs(avg_per), abs(median_per), switcher_avg, switcher_med)))

    return results_list