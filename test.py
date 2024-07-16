import requests
import pprint
import pandas as pd
import main
import mysql.connector
import os


main.criar_bd('riotgamescampeao')

# Conexão com o banco de dados específico
connection = mysql.connector.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database='riotgamescampeao'
)
cursor = connection.cursor()

def create_table_champion_skin(name_champio: str):
    # Criação da tabela Champions skins
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {name_champio} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Champion_Id INT,
        Id_Skins INT,
        Num INT,
        Name_Skins TEXT,
        Chromas INT
    )
    ''')
    connection.commit()

create_table_champion_skin('Champions_Skins')




url_champions_skins = f'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/champion/Katarina.json'

url_champions = 'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/champion.json'

response = requests.get(url_champions_skins)
response1 = requests.get(url_champions)

if response.status_code == 200:
        
    data = response.json()
    data1 = response1.json()
    # Initialize list for champions
    champions = []
    
    for champ, details in data1['data'].items():
        champions.append(details['name'])
        # print(champ)
    
    for cont, name in enumerate(champions):
        url_champions_skins = f'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/champion/{name}.json'
        
        data = response.json()
        
        response1 = requests.get(url_champions_skins)
        skins_champions = data['data'][name]['skins']
        # print(skins_champions)
    name_champions = data['data']['Katarina']['key']
        
    # print(name_champions)
    # pprint.pprint(skins_champions)

    skins = pd.DataFrame(skins_champions)
    
    skins.insert(0, 'Champion_id', name_champions)
    print(skins)
    
        
    # print(champions[0])
    
else:
    print(f"Erro na requisição: {response.status_code}")



