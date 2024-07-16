import mysql.connector
import os
import dotenv

dotenv.load_dotenv()

# Criando banco de dados
def criar_bd(name_bd: str):
    try:
        initial_connection = mysql.connector.connect(
            host=os.environ['MYSQL_HOST'],
            user=os.environ['MYSQL_USER'],
            password=os.environ['MYSQL_PASSWORD']
        )
        initial_cursor = initial_connection.cursor()
        initial_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name_bd}")
        initial_connection.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao criar o banco de dados: {err}")
    finally:
        initial_cursor.close()
        initial_connection.close()

criar_bd('riotgamescampeao')

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ['MYSQL_HOST'],
        user=os.environ['MYSQL_USER'],
        password=os.environ['MYSQL_PASSWORD'],
        database='riotgamescampeao'
    )

def create_table_champion(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS champion (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        title VARCHAR(255),
        blurb TEXT,
        partype VARCHAR(255)
    )
    ''')

def create_table_champions_info(cursor):
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

def create_table_champions_stats(cursor):
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

def inserir_dados_champion(cursor, df):
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

def inserir_dados_champions_info(cursor, df):
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

def inserir_dados_champions_stats(cursor, df):
    for _, champion_stats in df.iterrows():
        cursor.execute('''
        INSERT INTO Champions_stats
        (Name, hp, hpperlevel, mp, mpperlevel, movespeed, armor, armorperlevel, spellblock, spellblockperlevel, attackrange, hpregen, hpregenperlevel, mpregen, mpregenperlevel, crit, critperlevel, attackdamage, attackdamageperlevel, attackspeedperlevel, attackspeed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            champion_stats['Name'],
            champion_stats['hp'],
            champion_stats['hpperlevel'],
            champion_stats['mp'],
            champion_stats['mpperlevel'],
            champion_stats['movespeed'],
            champion_stats['armor'],
            champion_stats['armorperlevel'],
            champion_stats['spellblock'],
            champion_stats['spellblockperlevel'],
            champion_stats['attackrange'],
            champion_stats['hpregen'],
            champion_stats['hpregenperlevel'],
            champion_stats['mpregen'],
            champion_stats['mpregenperlevel'],
            champion_stats['crit'],
            champion_stats['critperlevel'],
            champion_stats['attackdamage'],
            champion_stats['attackdamageperlevel'],
            champion_stats['attackspeedperlevel'],
            champion_stats['attackspeed']
        ))