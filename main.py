import mysql.connector
import requests
import pandas as pd
import os
import dotenv

# Carregar variáveis de ambiente
dotenv.load_dotenv()

def criar_bd(name_bd: str):
    # Conexão inicial para criar o banco de dados
    initial_connection = mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD']
    )
    initial_cursor = initial_connection.cursor()

    # Criação do banco de dados
    initial_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name_bd}")
    initial_connection.commit()
    initial_cursor.close()
    initial_connection.close()

    print(f"Banco de dados '{name_bd}' criado com sucesso!")

criar_bd('riotgamescampeao')

# Conexão com o banco de dados específico
connection = mysql.connector.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database='riotgamescampeao'
)
cursor = connection.cursor()

def create_table_champion():
    # Criação da tabela champion
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS champion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        title VARCHAR(255),
        blurb TEXT,
        partype VARCHAR(255)
    )
    ''')
    connection.commit()

create_table_champion()

def create_table_champions_info():
    # Criação da tabela Champions_info
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Champions_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        attack INT,
        defense INT,
        magic INT,
        difficulty INT
    )
    ''')
    connection.commit()

create_table_champions_info()

def create_table_champions_stats():
    # Criação da tabela Champions_stats
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Champions_stats (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(255),
        hp INT,
        hpperlevel INT,
        mp INT,
        mpperlevel INT,
        movespeed INT,
        armor INT,
        armorperlevel FLOAT,
        spellblock INT,
        spellblockperlevel FLOAT,
        attackrange INT,
        hpregen FLOAT,
        hpregenperlevel FLOAT,
        mpregen FLOAT,
        mpregenperlevel FLOAT,
        crit INT,
        critperlevel INT,
        attackdamage INT,
        attackdamageperlevel FLOAT,
        attackspeedperlevel FLOAT,
        attackspeed FLOAT
    )
    ''')
    connection.commit()

create_table_champions_stats()

# URL da API
url = 'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/champion.json'

# Fazendo a requisição para a API
response = requests.get(url)

if response.status_code == 200:
    # Convertendo o JSON para um dicionário
    dados = response.json()
    data = dados['data']
    
    # Transformar dados em DataFrame
    champions = []
    for champ, details in data.items():
        champions.append({
            'name': details['name'],
            'title': details['title'],
            'blurb': details['blurb'],
            'partype': details['partype'],
        })
    
    df = pd.DataFrame(champions)
    
    def inserir_dados_champion(df):
        for _, champion in df.iterrows():
            cursor.execute('''
            INSERT INTO champion 
            (name, title, blurb, partype)
            VALUES (%s, %s, %s, %s)
            ''', (
                champion['name'],
                champion['title'],
                champion['blurb'],
                champion['partype'],
            ))
        connection.commit()
        print(cursor.rowcount, "registros inseridos com sucesso na tabela champion.")
        
    inserir_dados_champion(df)
    
    # Transformar dados em DataFrame para Champions_info
    champion_infoo = []
    
    for champ, details in data.items():
        champion_infoo.append({
            'name': details['name'],
            'info': details['info']
        })
    
    valor_info = []
    valor_name = []
    
    for indice, valor in enumerate(champion_infoo):
        valor_info.append(valor['info'])
        valor_name.append(valor['name'])
        
    df_info = pd.DataFrame(valor_info)
    df_info.insert(0, 'Name', valor_name)
    
    def inserir_dados_champions_info(df):
        for _, champion_info in df.iterrows():
            cursor.execute('''
            INSERT INTO Champions_info 
            (Name, attack, defense, magic, difficulty)
            VALUES (%s, %s, %s, %s, %s)
            ''', (
                champion_info['Name'],
                champion_info['attack'],
                champion_info['defense'],
                champion_info['magic'],
                champion_info['difficulty']
            ))
        connection.commit()
        print(cursor.rowcount, "registros inseridos com sucesso na tabela Champions_info.")

    inserir_dados_champions_info(df_info)
    
    # Transformar dados em DataFrame para Champions_stats
    champion_stats = []
    
    for champ, details in data.items():
        champion_stats.append({
            'name': details['name'],
            'stats': details['stats']
        })
    
    valor_stats = []
    valor_name = []
    
    for indice, valor in enumerate(champion_stats):
        valor_stats.append(valor['stats'])
        valor_name.append(valor['name'])
        
    df_stats = pd.DataFrame(valor_stats)
    df_stats.insert(0, 'Name', valor_name)
    
    def inserir_dados_champions_stats(df):
        for _, champion_statss in df.iterrows():
            cursor.execute('''
            INSERT INTO Champions_stats
            (Name, hp, hpperlevel, mp, mpperlevel, movespeed, armor, armorperlevel, spellblock, spellblockperlevel, attackrange, hpregen, hpregenperlevel, mpregen, mpregenperlevel, crit, critperlevel, attackdamage, attackdamageperlevel, attackspeedperlevel, attackspeed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                champion_statss['Name'],
                champion_statss['hp'],
                champion_statss['hpperlevel'],
                champion_statss['mp'],
                champion_statss['mpperlevel'],
                champion_statss['movespeed'],
                champion_statss['armor'],
                champion_statss['armorperlevel'],
                champion_statss['spellblock'],
                champion_statss['spellblockperlevel'],
                champion_statss['attackrange'],
                champion_statss['hpregen'],
                champion_statss['hpregenperlevel'],
                champion_statss['mpregen'],
                champion_statss['mpregenperlevel'],
                champion_statss['crit'],
                champion_statss['critperlevel'],
                champion_statss['attackdamage'],
                champion_statss['attackdamageperlevel'],
                champion_statss['attackspeedperlevel'],
                champion_statss['attackspeed']
            ))
        connection.commit()
        print(cursor.rowcount, "registros inseridos com sucesso na tabela Champions_stats.")

    inserir_dados_champions_stats(df_stats)
    
else:
    print(f"Erro na requisição: {response.status_code}")

# Fechar cursor e conexão
cursor.close()
connection.close()
