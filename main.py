import requests
import pandas as pd
import banco_de_dados
import pprint


connection = banco_de_dados.get_db_connection()
cursor = connection.cursor()

# Create tables
banco_de_dados.create_table_champion(cursor)
banco_de_dados.create_table_champions_info(cursor)
banco_de_dados.create_table_champions_stats(cursor)
banco_de_dados.create_table_champion_skin(cursor)
connection.commit()

# URL da API
url = 'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/championFull.json'

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
            'key': details['key'],
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
            'key': details['key'],
            'info': details['info']
        })
        
    valor_info = []
    valor_key = []
        
    for indice, valor in enumerate(champion_infoo):
        valor_info.append(valor['info'])
        valor_key.append(valor['key'])
            
    df_info = pd.DataFrame(valor_info)
    df_info.insert(0, 'key', valor_key)
        
    # Inserindo dados na Tabela Champions Info
    banco_de_dados.inserir_dados_champions_info(cursor, df_info)
        
    # Transformar dados em DataFrame para Champions_stats
    champion_stats = []
        
    for champ, details in data.items():
        champion_stats.append({
            'key': details['key'],
            'stats': details['stats']
        })
        
    valor_stats = []
    valor_key = []
        
    for indice, valor in enumerate(champion_stats):
        valor_stats.append(valor['stats'])
        valor_key.append(valor['key'])
            
    df_stats = pd.DataFrame(valor_stats)
    df_stats.insert(0, 'key', valor_key)
        
    # Inserindo dados na Tabela Champions stats
    banco_de_dados.inserir_dados_champions_stats(cursor, df_stats)
    
    champion_infoo = []

    for champ, details in dados['data'].items():
        champion_infoo.append({
            'key': details['key'],
            'skins': details['skins']
        })

    valor_skins = []
    valor_key = []

    for indice, valor in enumerate(champion_infoo):
        skins_names = [skin['name'] for skin in valor['skins']]
        valor_skins.append(skins_names)
        valor_key.append(valor['key'])

    # Criar um DataFrame com 21 colunas para comportar até 20 skins
    columns = ['key', 'skinum', 'skindois', 'skintres', 'skinquatro', 'skincinco', 'skinseis', 'skinsete', 'skinoito', 'skinnove', 'skindez', 'skinonze', 'skindoze', 'skintreze', 'skincatoze', 'skinquinze', 'skindeceseis', 'skindecesete', 'skindezoito', 'skindezenove', 'skinvinte', 'skinvinteum']
    df_skins = pd.DataFrame(columns=columns)
    
    for idx, (key, skins) in enumerate(zip(valor_key, valor_skins)):
        row = [key] + skins + [''] * (21 - len(skins))
        row = row[:22]  # Garantir que a linha tenha exatamente 22 elementos (1 para 'key', 1 para 'skins', e 20 para skins adicionais)
        df_skins.loc[idx] = row
    
    # Preencher valores nulos com 'default'
    df_skins.fillna('default', inplace=True)

    # Inserir dados preenchidos no banco de dados
    banco_de_dados.inserir_dados_champions_skins(cursor, df_skins)
        
    connection.commit()
        
else:
    print(f"Erro na requisição: {response.status_code}")

# Fechar cursor e conexão
cursor.close()
connection.close()

