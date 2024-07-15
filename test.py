import requests
import pprint
import pandas as pd

def champions_skins(name):
    url = f'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/champion/{name}.json'

    response = requests.get(url)

    if response.status_code == 200:
        
        data = response.json()
    
        skins_champions = data['data'][name]['skins']
        name_champions = data['data'][name]['name']
        
        print(name_champions)
        pprint.pprint(skins_champions)
    
        
    
    
    # skins = pd.DataFrame(skins_champions)
    # print(skins)
    
    # valor_name = []
    
    # for indice, valor in enumerate(s):
    #     valor_name.append(valor['name'])
        
    # df_stats = pd.DataFrame(valor_stats)
    # df_stats.insert(0, 'Name', valor_name)
    
    
    else:
        print(f"Erro na requisição: {response.status_code}")

name_champions = input('Nome do seu campeão: ')

champions_skins(f'{name_champions}')

