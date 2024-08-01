# Comsumindo-Api-Projeto

### github

https://github.com/devCaiodias/Comsumindo-Api-Projeto

### O que eu ultilizei 

https://www.python.org/downloads/release/python-3118/ https://pypi.org/project/pip/ https://pandas.pydata.org/ https://pypi.org/project/requests/ https://pypi.org/project/mysql-connector-python/ https://pypi.org/project/dotenv/

### Apis utilizada

Url_champions = https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/championFull.json

Url_champions_skins = https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Aatrox_1.jpg

### Oque eu fiz

Extrair dados da Api do jogo, e coloquei em cada tabla do banco de dados (tabela: champion, tabela: champion_info, tabela: champion_stats, tabela: champions_skins) e também tranformei a tabela champions_skins em um arquivo excel.

### Pacote ultilizados

import requests
import pandas as pd
import openpyxl
import mysql.connector
import dotenv
import os

### Conceitos

Virtual Enviroment (venv)
para criar um ambient virtual
py -m venv venv

### para ativar o ambiente virtual

venv/scripts/activate