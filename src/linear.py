# Imports
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pandas as pd
import numpy as np
import json

# Parameters
data_path ="/Users/mdebosz/Documents/Prywatne/Python-Scripts/GSTFI/src/data/data.csv"
future_days = 30

def get_linear_predictions(data_path = data_path, future_days = future_days):
    # Załaduj dane
    df = pd.read_csv(data_path, index_col='Data', parse_dates=True)

    # Usuń zbędną kolumne
    df.drop(['Unnamed: 0'],axis=1, inplace=True)

    output = {}


    for column in df.columns:
        # Dodaj kolumnę z liczbą dni (potrzebna do regresji)
        df['Day'] = np.arange(len(df))

        # Ustal zmienne zależne / niezależne
        X = df[~df[column].isna()]['Day'].values.reshape(-1,1)
        #y = df[column].values.reshape(-1,1)
        y = df[~df[column].isna()][column].values.reshape(-1,1)

        # Podziel dane na zestawy treningowe / testowe
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Trenuj model regresji liniowej
        regressor = LinearRegression()  
        regressor.fit(X_train, y_train)

        # Przewidywanie cen na przyszłość
        
        future_price = regressor.predict([[len(df) + future_days]])

        output[column] = future_price[0][0]

    """with open('src/data/linear.json', 'w') as f:
        json.dump(output, f, indent=4, sort_keys=True)
        print("Saved")"""
    return output


