import requests
import pandas as pd
import banco_de_dados


connection = banco_de_dados.get_db_connection()
cursor = connection.cursor()

# Create tables
banco_de_dados.create_table_champion(cursor)
banco_de_dados.create_table_champions_info(cursor)
banco_de_dados.create_table_champions_stats(cursor)
connection.commit()

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
        
    # Inserindo dados na Tabela Champions
    banco_de_dados.inserir_dados_champion(cursor, df)
        
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
        
    # Inserindo dados na Tabela Champions Info
    banco_de_dados.inserir_dados_champions_info(cursor, df_info)
        
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
        
    # Inserindo dados na Tabela Champions stats
    banco_de_dados.inserir_dados_champions_stats(cursor, df_stats)
        
    connection.commit()
        
else:
    print(f"Erro na requisição: {response.status_code}")

# Fechar cursor e conexão
cursor.close()
connection.close()

