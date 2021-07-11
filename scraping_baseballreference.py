import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup
import urllib.request

teams = ['NYM', 'ATL', 'PHI',
         'WSN', 'MIA', 'MIL',
         'CIN', 'CHC', 'STL',
         'PIT', 'SFG', 'LAD',
         'SDP', 'COL', 'ARI',
         'BOS', 'TBR', 'NYY',
         'TOR', 'BAL', 'CHW',
         'CLE', 'DET', 'MIN',
         'KCR', 'HOU', 'OAK',
         'SEA', 'LAA', 'TEX']
years = [1980, 1981, 1982,
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

for team in teams:
    for year in years:
        try:
            year = str(year)
            try:
                url = 'https://www.baseball-reference.com/teams/' + team + '/' + year + '-schedule-scores.shtml'
                page = urllib.request.urlopen(url)
            except Exception:
                pass
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find("table", {'id': 'team_schedule'})
            table_rows = table.find_all('tr')
            output = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text for tr in td]
                output.append(row)
            df = pd.DataFrame(output)
            df = df[[0, 4, 17]]
            df.columns = ['date', 'opponent', 'attendance']
            df.dropna(how='all', axis=0, inplace=True)
            df['year'] = int(year)
            df['home_team'] = team
            main_df = pd.concat([main_df, df], axis=0)
        except Exception as e:
            print(year)
            print(team)
            print(e)
            pass

main_df