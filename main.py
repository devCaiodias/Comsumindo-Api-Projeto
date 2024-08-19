import requests
import pandas as pd
import pprint


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
    valor_key_champions = 'key'
    valor_title_champions = 'title'
    valor_blurb_champions = 'blurb'
    valor_partype_champions = 'partype'
    df_champions = pd.DataFrame()
        
    def champions4(list_champion, parametro1, parametro2, parametro3, parametro4):
        for champ, details in data.items():
            list_champion.append({
                parametro1: details[parametro1],
                parametro2: details[parametro2],
                parametro3: details[parametro3],
                parametro4: details[parametro4],
            })

        
    champions4(champions, valor_key_champions, valor_title_champions, valor_blurb_champions, valor_partype_champions)      
    df_champions = pd.DataFrame(champions)
        
    # Transformar dados em DataFrame para Champions_info
        
    champion_infoo: list = []
    valor_key_info = 'key'
    valor_info = 'info'
    list_info:list = []
    list_key_info:list = []
    df_info = pd.DataFrame()
    def champions2(list_champions, parametro1, parametro2, list_value, list_value1):
        for champ, details in data.items():
            list_champions.append({
                parametro1: details[parametro1],
                parametro2: details[parametro2]
            })
    
            
        for valor in list_champions:
            list_value.append(valor[parametro2])
            list_value1.append(valor[parametro1])


    champions2(champion_infoo, valor_key_info, valor_info, list_info, list_key_info)

    df_info = pd.DataFrame(list_info)
    df_info.insert(0, 'key', list_key_info)
    
        
    # Transformar dados em DataFrame para Champions_stats
    champion_stats:list = []
    valor_key_stats = 'key'
    valor_stats = 'stats'
    list_stats:list = []
    list_key_stats:list = []
    df_stats = pd.DataFrame()

    champions2(champion_stats, valor_key_stats, valor_stats, list_stats, list_key_stats)

    df_stats = pd.DataFrame(list_stats)
    df_stats.insert(0, 'key', list_key_stats)
    
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
    # skins_df.to_excel('champions_skins_url.xlsx', index=False)
        
else:
    print(f"Erro na requisição: {response.status_code}")
