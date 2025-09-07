import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
import numpy as np

df2 = pd.DataFrame()

##### Gathering players that participated in combine
firstLast=[]
dfNames = pd.read_csv("NBACombine.csv")

names = dfNames["Player"]
for i in names:
    j=i.split()
    firstLast.append([j[0].lower(),j[1].lower()])
print(firstLast)
#####




for i in firstLast:
    cont=True #Temporary Variable
    url = 'https://www.sports-reference.com/cbb/players/'+i[0]+'-'+i[1]+'-1.html' 
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', id='players_per_game')

    # ChatGPT code: if table not found searches 
    if table is None:
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if 'id="players_per_game"' in comment:
                comment_soup = BeautifulSoup(comment, 'html.parser')
                table = comment_soup.find('table', id='players_per_game')
                if table:
                    break
    #Wouldn't run without this, even though above should fix it
    if table is None:
        cont = False
        
    #Data to DF
    if cont:
        df = pd.read_html(str(table))[0]

    #Drop empty rows
        df = df.dropna(how='all')
        
    #Add Names to single df and add onto the bottom
        df["Name"] = i[0].capitalize()+' '+i[1].capitalize()
        df2 = pd.concat([df2, df], ignore_index=True)
        
    #Lag for pro-sports-reference TOS
    lag = np.random.uniform(low=5, high=40)
    print(f'...waiting {round(lag, 1)} seconds')
    time.sleep(lag) #Becasue NBA doesn't like you scraping data

#Filter out irrelivant stats to quick clean. Also only career stats
df_new = df2[df2['Season'].str.contains("Career")] 
df_new = df_new.drop(columns=(["Season","Team","Conf","Class","Pos","Awards"]))


df_new.to_csv("CollegeStats.csv",index=False)
