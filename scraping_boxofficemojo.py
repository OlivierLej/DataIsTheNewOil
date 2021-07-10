import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup
import urllib.request

years = [1977, 1978, 1979,
         1980, 1981, 1982,
         1983, 1984, 1985,
         1986, 1987, 1988,
         1989, 1990, 1991,
         1992, 1993, 1994,
         1995, 1996, 1997,
         1998, 1999, 2000,
         2001, 2002, 2003,
         2004, 2005, 2006,
         2007, 2008, 2009,
         2010, 2011, 2012,
         2013, 2014, 2015,
         2016, 2017, 2018,
         2019, 2020, 2021]
main_df = pd.DataFrame()

for year in years:
    try:
        year = str(year)
        url = 'https://www.boxofficemojo.com/weekly/by-year/' + year
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        table = soup.find("table")
        table_rows = table.find_all('tr')
        output = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [tr.text for tr in td]
            output.append(row)
        df = pd.DataFrame(output)
        df = df.iloc[1:]
        df.replace('-', np.nan, inplace=True)
        df.replace('false', np.nan, inplace=True)
        df.dropna(how='all', axis=1, inplace=True)
        cols = ['dates', 'top10gross_usd', 'top10gross_wow%', 'overallgross_usd', 'overallgross_wow%', 'releases', 'topmovie', 'week']
        df.columns = cols
        df['top10gross_usd'] = df['top10gross_usd'].str.replace('$', '')
        df['top10gross_usd'] = df['top10gross_usd'].str.replace(',', '')
        df['overallgross_usd'] = df['overallgross_usd'].str.replace('$', '')
        df['overallgross_usd'] = df['overallgross_usd'].str.replace(',', '')
        df['top10gross_usd'] = pd.to_numeric(df['top10gross_usd'], errors='coerce')
        df['overallgross_usd'] = pd.to_numeric(df['overallgross_usd'], errors='coerce')
        df['releases'] = pd.to_numeric(df['releases'], errors='coerce')
        df['week'] = pd.to_numeric(df['week'], errors='coerce')
        df.sort_values('week', ascending=True, inplace=True)
        first_day = df['dates'].iloc[0].split('-')[0] + ' ' + year
        first_day = datetime.datetime.strptime(first_day, '%b %d %Y')
        dates = pd.date_range(start=first_day, periods=len(df), freq='w-fri')
        df.index = dates
        df.drop(['dates', 'top10gross_wow%', 'overallgross_wow%'], axis=1, inplace=True)
        df.index.rename('date', inplace=True)
        main_df = pd.concat([main_df, df], axis=0)
    except Exception as e:
        print(e)
        pass

main_df
