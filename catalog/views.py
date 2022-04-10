from django.shortcuts import render
import yfinance as yf
import pandas as pd
import os
import json
import numpy as numpy
from django.http import HttpResponse


tickerCompanyList = {
    'Activision Blizzard': 'ATVI', 
    'Adobe': 'ADBE', 
    'ADP': 'ADP', 
    'Airbnb': 'ABNB', 
    'Align': 'ALGN', 
    'Alphabet (Class A)': 'GOOGL', 
    'Alphabet (Class C)': 'GOOG', 
    'Amazon': 'AMZN', 'AMD': 'AMD', 'American Electric Power': 'AEP', 'Amgen': 'AMGN', 'Analog Devices': 'ADI', 'Ansys': 'ANSS', 'Apple': 'AAPL', 'Applied Materials': 'AMAT', 'ASML': 'ASML', 'AstraZeneca': 'AZN', 'Atlassian': 'TEAM', 'Autodesk': 'ADSK', 'Baidu': 'BIDU', 'Biogen': 'BIIB', 'Booking Holdings': 'BKNG', 'Broadcom': 'AVGO', 'Cadence': 'CDNS', 'Charter Communications': 'CHTR', 'Cintas': 'CTAS', 'Cisco': 'CSCO', 'Cognizant': 'CTSH', 'Comcast': 'CMCSA', 'Constellation': 'CEG', 'Copart': 'CPRT', 'Costco': 'COST', 'CrowdStrike': 'CRWD', 'CSX': 'CSX', 'Datadog': 'DDOG', 'DexCom': 'DXCM', 'DocuSign': 'DOCU', 'Dollar Tree': 'DLTR', 'eBay': 'EBAY', 'Electronic Arts': 'EA', 'Exelon': 'EXC', 'Fastenal': 'FAST', 'Fiserv': 'FISV', 'Fortinet': 'FTNT', 'Gilead': 'GILD', 'Honeywell': 'HON', 'Idexx Laboratories': 'IDXX', 'Illumina': 'ILMN', 'Intel': 'INTC', 'Intuit': 'INTU', 'Intuitive Surgical': 'ISRG', 'JD.com': 'JD', 'Keurig Dr Pepper': 'KDP', 'KLA': 'KLAC', 'Kraft Heinz': 'KHC', 'Lam Research': 'LRCX', 'Lucid': 'LCID', 'Lululemon': 'LULU', 'Marriott International': 'MAR', 'Marvell': 'MRVL', 'Match Group': 'MTCH', 'MercadoLibre': 'MELI', 'Meta': 'FB', 'Microchip': 'MCHP', 'Micron': 'MU', 'Microsoft': 'MSFT', 'Moderna': 'MRNA', 'Mondelēz International': 'MDLZ', 'Monster Beverage': 'MNST', 'NetEase': 'NTES', 'Netflix': 'NFLX', 'Nvidia': 'NVDA', 'NXP': 'NXPI', "O'Reilly Automotive": 'ORLY', 'Okta': 'OKTA', 'Old Dominion Freight Line': 'ODFL', 'Paccar': 'PCAR', 'Palo Alto Networks': 'PANW', 'Paychex': 'PAYX', 'PayPal': 'PYPL', 'PepsiCo': 'PEP', 'Pinduoduo': 'PDD', 'Qualcomm': 'QCOM', 'Regeneron': 'REGN', 'Ross Stores': 'ROST', 'Seagen': 'SGEN', 'Sirius XM': 'SIRI', 'Skyworks': 'SWKS', 'Splunk': 'SPLK', 'Starbucks': 'SBUX', 'Synopsys': 'SNPS', 'T-Mobile': 'TMUS', 'Tesla': 'TSLA', 'Texas Instruments': 'TXN', 'Verisign': 'VRSN', 'Verisk': 'VRSK', 'Vertex': 'VRTX', 'Walgreens Boots Alliance': 'WBA', 'Workday': 'WDAY', 'Xcel Energy': 'XEL', 'Zoom': 'ZM', 'Zscaler': 'ZS'

}

def ticker_selected(request):
    if(request.GET.get('ticker-value')):
        
        company_ticker = str(request.GET.get('ticker-value'))
        company_name = tickerCompanyList[company_ticker]
        company_y = yf.Ticker(company_name)
        dataFrame = company_y.sustainability
        if(dataFrame is None):
            socialScore = 'Does Not Exist'
            environmentScore = 'Does Not Exist'
            governancePercentile = 'Does Not Exist'
            price = '${:,.2f}'.format(company_y.info['regularMarketPrice'])
            esgTotal = 'Does Not Exist'

        else:
            esg_data = pd.DataFrame.transpose(company_y.sustainability)
            esg_data['company_ticker'] = str(company_y.ticker)
            str_socialScore =  str(esg_data['socialScore'].values)
            socialScore = str_socialScore.strip('[]')
            str_environmentScore = str(esg_data['environmentScore'].values)
            environmentScore = str_environmentScore.strip('[]')
            str_governancePercentile = str(esg_data['governancePercentile'].values)
            if(str_governancePercentile == '[None]'):
                governancePercentile = 0.00
            else:
                governancePercentile = str_governancePercentile.strip('[]')
            price = '${:,.2f}'.format(company_y.info['regularMarketPrice'])
            str_esgTotal = str(esg_data['environmentScore'].values + esg_data['socialScore'].values)
            esgTotal = str_esgTotal.strip('[]')

        financials = company_y.financials
        print(financials)
        finance_results = financials.to_html()
        finance_results = finance_results.replace('<tr>', '<tr align="center">')

        hist = company_y.history(period="1y", interval="1m")
        print(type(hist))
        hist_results = hist.to_html()

        
    

        context = {
            'company_ticker': company_ticker,
            'company_name': company_name,
            'social_score': socialScore,
            'environmental_score': environmentScore,
            'governance_percentile': governancePercentile,
            'total_esg_risk_score': esgTotal,
            'price': price,
            'financials': finance_results,
            'hist': hist_results
            # 'news': news
        }

        # Render the HTML template index.html with the data in the context variable
        return render(request, 'index.html', context=context)



def index(request):
    company_ticker = "Amazon"
    company_name = tickerCompanyList[company_ticker]
    company_y = yf.Ticker(company_name)
    esg_data = pd.DataFrame.transpose(company_y.sustainability)
    esg_data['company_ticker'] = str(company_y.ticker)
    str_socialScore =  str(esg_data['socialScore'].values)
    socialScore = str_socialScore.strip('[]')
    
    str_environmentScore = str(esg_data['environmentScore'].values)
    environmentScore = str_environmentScore.strip('[]')
    
    str_governancePercentile = str(esg_data['governancePercentile'].values)
    #print(str_governancePercentile)

    if(str_governancePercentile == '[None]'):
        governancePercentile = 0.00
    else:
        #str_governancePercentile.strip('[]')
        governancePercentile = str_governancePercentile.strip('[]')

    
    price = '${:,.2f}'.format(company_y.info['regularMarketPrice'])
    
    str_esgTotal = str(esg_data['environmentScore'].values + esg_data['socialScore'].values)
    esgTotal = str_esgTotal.strip('[]')

    financials = company_y.financials
    finance_results = financials.to_html()

    hist = company_y.history(start="2021-01-04", end="2022-04-04", interval="1mo")
    hist_results = hist.to_html()
    

    # news = company_y.news

    context = {
        'company_ticker': company_ticker,
        'company_name': company_name,
        'social_score': socialScore,
        'environmental_score': environmentScore,
        'governance_percentile': governancePercentile,
        'total_esg_risk_score': esgTotal,
        'price': price,
        'financials': finance_results,
        'hist': hist_results
        # 'news': news
    }

    pd.set_option('expand_frame_repr', False)
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    # There are 4 tables on the Wikipedia page
    # we want the last table

    payload=pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100')
    ticker_table = payload[3]

    # df = ticker_table[['Company','Ticker']]
    dc = ticker_table['Company']
    # dictionaryObject = df.to_dict()
    dictionaryObject2 = dc.to_dict()
    dc2 = dc.to_string(index=False)
    # dc.set_index('Company', inplace=True)


    # print(dictionaryObject)
    # print(type(dictionaryObject))
    print(dc.values)
    # print(type(dc2))
    # print(dictionaryObject2)



    # print(df)
    # print(type(df))

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

