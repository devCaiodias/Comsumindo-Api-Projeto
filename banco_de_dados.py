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
        ids INT,
        title VARCHAR(255),
        blurb TEXT,
        partype VARCHAR(255)
    )
    ''')

def create_table_champions_info(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Champions_info (
        id INT AUTO_INCREMENT PRIMARY KEY,
        ids INT,
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
        ids INT,
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
    
def create_table_champion_skin(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS champions_skin (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Champion_id INT,
        id_skins INT,
        num INT,
        name VARCHAR(255),
        chromas BOOLEAN, 
        urls TEXT
    );
    ''')

def inserir_dados_champion(cursor, df):
    for _, champion in df.iterrows():
        cursor.execute('''
        INSERT INTO champion 
        (ids, title, blurb, partype)
        VALUES (%s, %s, %s, %s)
        ''', (
            champion['key'],
            champion['title'],
            champion['blurb'],
            champion['partype'],
        ))

def inserir_dados_champions_info(cursor, df):
    for _, champion_info in df.iterrows():
        cursor.execute('''
        INSERT INTO Champions_info 
        (ids, attack, defense, magic, difficulty)
        VALUES (%s, %s, %s, %s, %s)
        ''', (
            champion_info['key'],
            champion_info['attack'],
            champion_info['defense'],
            champion_info['magic'],
            champion_info['difficulty']
        ))

def inserir_dados_champions_stats(cursor, df):
    for _, champion_stats in df.iterrows():
        cursor.execute('''
        INSERT INTO Champions_stats
        (ids, hp, hpperlevel, mp, mpperlevel, movespeed, armor, armorperlevel, spellblock, spellblockperlevel, attackrange, hpregen, hpregenperlevel, mpregen, mpregenperlevel, crit, critperlevel, attackdamage, attackdamageperlevel, attackspeedperlevel, attackspeed)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            champion_stats['key'],
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
        
def inserir_dados_champions_skins(cursor, df):
    for _, champions_skins in df.iterrows():
        cursor.execute('''
        INSERT INTO champions_skin
        (Champion_id, id_skins, num, name, chromas, urls)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            champions_skins['Champion_id'],
            champions_skins['id'],  # Make sure 'id' exists in the DataFrame
            champions_skins['num'],
            champions_skins['name'],
            champions_skins['chromas'],
            champions_skins['urls']
        ))
