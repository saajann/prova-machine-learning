import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import streamlit as st

# Load the CSV
df = pd.read_csv('serie_a_matches.csv')

# Data cleaning and preparation
# df.dropna()  # Uncomment this line if needed for cleaning

# Feature engineering
df['home_goals'] = df['score.fullTime.home']
df['away_goals'] = df['score.fullTime.away']

# Define features and target variables
X = df[['homeTeam.id', 'awayTeam.id', 'matchday']]
y_home = df['home_goals']
y_away = df['away_goals']

# Train the model for home team
model_home = RandomForestRegressor()
X_train_home, X_test_home, y_train_home, y_test_home = train_test_split(X, y_home, test_size=0.2, random_state=42)
model_home.fit(X_train_home, y_train_home)

# Train the model for away team
model_away = RandomForestRegressor()
X_train_away, X_test_away, y_train_away, y_test_away = train_test_split(X, y_away, test_size=0.2, random_state=42)
model_away.fit(X_train_away, y_train_away)

# Streamlit Dashboard
st.title("Serie A Matchday Predictor")

# Select matchday
specified_matchday = st.selectbox("Select Matchday", df['matchday'].unique())

# Predict expected goals for the selected matchday
matchday_df = df[df['matchday'] == specified_matchday]
expected_goals_home = model_home.predict(matchday_df[['homeTeam.id', 'awayTeam.id', 'matchday']])
expected_goals_away = model_away.predict(matchday_df[['homeTeam.id', 'awayTeam.id', 'matchday']])

# Add predictions to the DataFrame
matchday_df['expected_goals_home'] = expected_goals_home
matchday_df['expected_goals_away'] = expected_goals_away

# Determine predicted outcomes
def predict_outcome(row):
    if row['expected_goals_home'] > row['expected_goals_away']:
        return 1  # Home win
    elif row['expected_goals_home'] < row['expected_goals_away']:
        return 2  # Away win
    else:
        return 'x'  # Draw

matchday_df['predicted_outcome'] = matchday_df.apply(predict_outcome, axis=1)

# Display results
st.write(f"Predictions for Matchday {specified_matchday}")
st.dataframe(matchday_df[['homeTeam.name', 'awayTeam.name', 'expected_goals_home', 'expected_goals_away', 'predicted_outcome']])
