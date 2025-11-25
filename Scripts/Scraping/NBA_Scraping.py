from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import time
import numpy as np


#trainYears = ['2000-01','2001-02','2002-03','2003-04','2004-05','2005-06','2006-07','2007-08','2008-09','2009-10',
#         '2010-11','2011-12','2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20']
testYears = ['2020-21','2021-22','2022-23','2023-24','2024-25']
df2 = pd.DataFrame()

#ChatGPT assisted using the public NBA API for scraping player data
for y in testYears:
    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=y,
        season_type_all_star='Regular Season',
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Base'
    )

    df = stats.get_data_frames()[0]
    df2 = pd.concat([df2, df], ignore_index=True)

    lag = np.random.uniform(low=5, high=40)
    print(f'...waiting {round(lag, 1)} seconds')
    time.sleep(lag)

#df2.to_csv("NBA_2000_2020.csv",index=False)
df2.to_csv("NBA_2020_2025.csv",index=False)


