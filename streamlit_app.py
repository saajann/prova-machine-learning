import requests
import pandas as pd
import streamlit as st


# Configurazione
API_URL = 'https://api.football-data.org/v2/competitions/SA/matches?dateFrom=2024-01-01&dateTo=2024-01-31'
API_KEY = '618e7151180f445f8dc99cdbb440f4ef'

headers = {'X-Auth-Token': API_KEY}

# Richiesta API
response = requests.get(API_URL, headers=headers)
data = response.json()

# Convertire i dati in un DataFrame
matches = pd.json_normalize(data['matches'])

# Salva i dati per usi futuri
matches.to_csv('serie_a_matches.csv', index=False)


st.title('Serie A predictor')

st.write('Hello world!')

st.dataframe(matches)