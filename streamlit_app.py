import requests
import pandas as pd
import streamlit as st


# Configurazione
API_URL = 'https://api.football-data.org/v4/competitions/SA/matches?season=2024'
# API_URL = 'https://api.football-data.org/v4/competitions/SA/matches?dateFrom=2024-10-01&dateTo=2024-10-31'
API_KEY = ''

headers = {'X-Auth-Token': API_KEY}

# Richiesta API
response = requests.get(API_URL, headers=headers)
data = response.json()

# Convertire i dati in un DataFrame
matches = pd.json_normalize(data['matches'])

# Salva i dati per usi futuri
matches.to_csv('serie_a_matches.csv', index=False)



def get_match_result(row):
    if row['score.fullTime.home'] > row['score.fullTime.away']:
        return '1'
    elif row['score.fullTime.home'] == row['score.fullTime.away']:
        return 'x'
    else:
        return '2'

matches['matchResult'] = matches.apply(get_match_result, axis=1)

