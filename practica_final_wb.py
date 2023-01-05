import bs4 
import requests
import pandas as pd
from fpdf import FPDF
import re


def ratio_apostado():
    url = 'https://www.sportytrader.es/cuotas/baloncesto/usa/nba-306/'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    equipo = 'nuggets'
    try:
        equipos = soup.find_all('div', onclick=re.compile(equipo))
        ratio = equipos[0].find_all('span', class_='px-1 h-booklogosm font-bold bg-primary-yellow text-white leading-8 rounded-r-md w-14 md:w-18 flex justify-center items-center text-base')
        return float(ratio[0].text),float(ratio[1].text)
    except:
        return 0,0
def extract():
    url = 'https://api.sportsdata.io/v3/nba/scores/json/Standings/2023'
    url2 = 'https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStatsByTeam/2023/DEN'
    params = {'key': 'b32c222a51d443d3b0a6d1cda29a2c4b'}
    response = requests.get(url, params=params)
    response2 = requests.get(url2, params=params)
    return response , response2

def createpdf(response, response2):
    data = response.json()
    data2 = response2.json()
    standings = pd.DataFrame(data)
    players = pd.DataFrame(data2)
    
    standings = standings[['Name', 'Conference', 'Wins', 'Losses', 'Percentage',
    'Streak','GamesBack','ConferenceRank']]
    eastern = standings[standings['Conference'] == 'Eastern']  
    western = standings[standings['Conference'] == 'Western']
    
    players = players[['Name', 
       'Position',  'Games', 'Rebounds', 'Points',
        'AssistsPercentage', 'StealsPercentage','BlocksPercentage', 'PlusMinus']]
    # cambiar nombre de columnas
    players.columns = ['Name', 'Pos', 'Games', 'Rebs', 'Pts', 'Ast', 'Stls', 'Blcks', 'PlusMinus']
    players = players.head(12)
    players['Pts']= round(players['Pts']/players['Games'])
    players['Rebs']= round(players['Rebs']/players['Games'])
    players['Ast']= round(players['Ast']/5)
    eastern = eastern.set_index('ConferenceRank')
    eastern = eastern.sort_index()
    western = western.set_index('ConferenceRank')
    western = western.sort_index()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=35)
    pdf.cell(200, 50, txt="NBA API ", ln=1, align="C")
    pdf.image('nba.png', x=10, y=10, w=50)
    pdf.image('nba.png', x=158, y=10, w=50)
    pdf.cell(200,60, txt='', ln=1, align="C")
    pdf.cell(200,40, txt='Denver Nuggets', ln=1, align="C")
    pdf.set_font("Arial", size=12)
  
    
    pdf.image('denver.png', x=83, y=170, w=50)
    
    pdf.add_page()
    pdf.image('denver.png', x=17, y=10, w=30)
    pdf.image('denver.png', x=168, y=10, w=30)
    
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 30, txt="NBA STANDINGS", ln=1, align="C")
    pdf.cell(200, 30, txt="--Eastern Conference--", ln=1, align="C")
    
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(70, 10, "Name", 1, align="C")
    pdf.cell(22, 10, "Wins", 1, align="C")   
    pdf.cell(22, 10, "Losses", 1, align="C")
    pdf.cell(28, 10, "Percentage", 1, align="C")
    pdf.cell(30, 10, "GamesBack", 1, align="C")
    pdf.cell(22, 10, "Streak",1, align="C",ln=1)

    pdf.set_font("Arial", size=12)
    for index, row in eastern.iterrows():
        pdf.cell(70, 10, row['Name'], 1, align="C")
        pdf.cell(22, 10, str(row['Wins']), 1, align="C")
        pdf.cell(22, 10, str(row['Losses']), 1, align="C")
        pdf.cell(28, 10, str(row['Percentage']), 1, align="C")
        pdf.cell(30, 10, str(row['GamesBack']), 1, align="C")
        pdf.cell(22, 10, str(row['Streak']), 1, align="C",ln=1)

    
    pdf.add_page()
    pdf.image('denver.png', x=17, y=10, w=30)
    pdf.image('denver.png', x=168, y=10, w=30)

    pdf.set_font("Arial", size=24)
    pdf.cell(200, 30, txt="NBA STANDINGS", ln=1, align="C")
    pdf.cell(200, 30, txt="--Western Conference--", ln=1, align="C")
    
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(70, 10, "Name", 1, align="C")
    pdf.cell(22, 10, "Wins", 1, align="C")   
    pdf.cell(22, 10, "Losses", 1, align="C")
    pdf.cell(28, 10, "Percentage", 1, align="C")
    pdf.cell(30, 10, "GamesBack", 1, align="C")
    pdf.cell(22, 10, "Streak",1, align="C",ln=1)

    pdf.set_font("Arial", size=12)
    for index, row in western.iterrows():
        if row['Name'] == 'Nuggets':
            pdf.set_font("Arial", size=12, style="B")
        else:
            pdf.set_font("Arial", size=12)
        pdf.cell(70, 10, row['Name'], 1, align="C")
        pdf.cell(22, 10, str(row['Wins']), 1, align="C")
        pdf.cell(22, 10, str(row['Losses']), 1, align="C")
        pdf.cell(28, 10, str(row['Percentage']), 1, align="C")
        pdf.cell(30, 10, str(row['GamesBack']), 1, align="C")
        pdf.cell(22, 10, str(row['Streak']), 1, align="C",ln=1)
    
    pdf.add_page()
    pdf.image('denver.png', x=17, y=10, w=30)
    pdf.image('denver.png', x=168, y=10, w=30)

    pdf.set_font("Arial", size=24)
    pdf.cell(200, 30, txt="Team Stats", ln=1, align="C")
    pdf.cell(200, 30, txt="--Western Conference--", ln=1, align="C")

    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(46, 10, "Name", 1, align="C")
    pdf.cell(18, 10, "Pos", 1, align="C")
    pdf.cell(22, 10, "Games", 1, align="C")
    pdf.cell(22, 10, "Rebs",1, align="C")
    pdf.cell(18, 10, "PTS",1, align="C")
    pdf.cell(18, 10, "AST",1, align="C")
    pdf.cell(18, 10, "Stls",1, align="C")
    pdf.cell(18, 10, "Blcks",1, align="C")
    pdf.cell(16, 10, "+/-",1, align="C",ln=1)

    pdf.set_font("Arial", size=12)
    for index, row in players.iterrows():
        if row ['Name'] == 'Nikola Jokic':
            pdf.set_font("Arial", size=12, style="B")
        else:
            pdf.set_font("Arial", size=12)
        if row['Name'] == 'Kentavious Caldwell-Pope':
            pdf.cell(46, 10, 'Caldwell-Pope', 1, align="C")
        else:
            pdf.cell(46, 10, row['Name'], 1, align="C")
        pdf.cell(18, 10, str(row['Pos']), 1, align="C")
        pdf.cell(22, 10, str(row['Games']), 1, align="C")
        pdf.cell(22, 10, str(row['Rebs']), 1, align="C")
        pdf.cell(18, 10, str(row['Pts']), 1, align="C")
        pdf.cell(18, 10, str(row['Ast']), 1, align="C")
        pdf.cell(18, 10, str(row['Stls']), 1, align="C")
        pdf.cell(18, 10, str(row['Blcks']), 1, align="C")
        pdf.cell(16, 10, str(row['PlusMinus']), 1, align="C",ln=1)

    
    pdf.add_page()
    pdf.image('denver.png', x=17, y=10, w=30)
    pdf.image('denver.png', x=168, y=10, w=30)

    jokers = players[players['Name'] == 'Nikola Jokic']
    pdf.set_font("Arial", size=24)
    pdf.cell(200, 30, txt="NIKOLA JOKIC", ln=1, align="C")
    pdf.cell(200, 30, txt="THE JOKER", ln=1, align="C")
    pdf.cell(200,30,txt=" 2x MVP  ",ln=1,align="R")
    pdf.cell(200,30,txt="80+ Triple Doubles  ",ln=1,align="R")
    for index, row in jokers.iterrows():
        pdf.cell(200,30,str(row['Pts']) + ' PPG  ',ln=1,align="R")
        pdf.cell(200,30,str(row['Ast']) + ' APG  ',ln=1,align="R")
        pdf.cell(200,30,str(row['Rebs']) + ' RPG  ',ln=1,align="R")
    pdf.image('Jokic.png', x=20, y=80, w=100)

    cuota1,cuota2 = ratio_apostado()
    if cuota1 == cuota2:
        cuota1==cuota2==1
    pdf.set_font("Arial", size=17)
    pdf.cell(200,22,txt="Basandonos solamente en las cuotas de Sporty Trader:",ln=1,align="C")
    pdf.set_font("Arial", size=14)
    pdf.cell(200,25,txt="Si juega en casa "+str(round((cuota1/(cuota1+cuota2))*100))+" % de victoria",ln=1,align="C")
    pdf.cell(200,9,txt="Si juega fuera de casa "+str(round((cuota2/(cuota1+cuota2))*100))+" % de victoria",ln=1,align="C")
    

    pdf.output("nba.pdf")



    



if __name__ == '__main__':
    standings,players = extract()
    createpdf(standings,players)

    