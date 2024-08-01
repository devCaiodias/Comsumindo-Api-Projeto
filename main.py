import requests
import pandas as pd
import banco_de_dados
import openpyxl
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
    champion_infoo: list = []
        
    for champ, details in data.items():
        champion_infoo.append({
            'key': details['key'],
            'info': details['info']
        })
        
    valor_info:list = []
    valor_key:list = []
        
    for indice, valor in enumerate(champion_infoo):
        valor_info.append(valor['info'])
        valor_key.append(valor['key'])
            
    df_info = pd.DataFrame(valor_info)
    df_info.insert(0, 'key', valor_key)
        
    # Inserindo dados na Tabela Champions Info
    banco_de_dados.inserir_dados_champions_info(cursor, df_info)
        
    # Transformar dados em DataFrame para Champions_stats
    champion_stats:list = []
        
    for champ, details in data.items():
        champion_stats.append({
            'key': details['key'],
            'stats': details['stats']
        })
        
    valor_stats:list = []
    valor_key:list = []
        
    for indice, valor in enumerate(champion_stats):
        valor_stats.append(valor['stats'])
        valor_key.append(valor['key'])
            
    df_stats = pd.DataFrame(valor_stats)
    df_stats.insert(0, 'key', valor_key)
        
    # Inserindo dados na Tabela Champions stats
    banco_de_dados.inserir_dados_champions_stats(cursor, df_stats)
    
    # Extrair informações dos campeões
    
    champions_skins:list = []
    
    for champ, details in data.items():
        champions_skins.append(details['name'])

    # Extrair skins e ids dos campeões
    skins_data:list = []
    name_champions:list = []
    for name in champions_skins:
        for champ, details in data.items():
            if details['name'] == name:
                skins_champions = details['skins']
                for skin in skins_champions:
                    name_champions.append(details['key'])
                    skins_data.append(skin)

    # Converter para DataFrame
    skins_df = pd.DataFrame(skins_data)
    skins_df.insert(0, 'Champion_id', name_champions)

    # Obter URLs das skins
    champion_skins:list = []
    for champ, details in data.items():
        champion_skins.append({
            'key': details['key'],
            'id': details['id'],
            'skins': details['skins']
        })

    urls_dict:list = []
    for champ in champion_skins:
        champ_id = champ['id']
        for skin in champ['skins']:
            skin_num = skin['num']
            url = f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ_id}_{skin_num}.jpg'
            urls_dict.append(url)
            
    # Converter para DataFrame
    df_urls = pd.DataFrame(urls_dict, columns=['urls'])
    skins_df = skins_df.join(df_urls)

    # Exibir o DataFrame
    pprint.pprint(skins_df)
    skins_df.to_excel('champions_skins_url.xlsx', index=False)
    

    banco_de_dados.inserir_dados_champions_skins(cursor, skins_df)
    connection.commit()

        
else:
    print(f"Erro na requisição: {response.status_code}")

# Fechar cursor e conexão
cursor.close()
connection.close()