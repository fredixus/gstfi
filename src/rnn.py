# Imports
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
import matplotlib.pyplot as plt
from keras.layers import Dense, LSTM
import numpy as np

import json

# Parameters
data_path ="/Users/mdebosz/Documents/Prywatne/Python-Scripts/GSTFI/src/data/data.csv"

def get_rnn(data_path = data_path):
    # Załaduj dane
    df = pd.read_csv(data_path, index_col='Data', parse_dates=True)

    # Usuń zbędną kolumne
    df.drop(['Unnamed: 0'],axis=1, inplace=True)

    output = {}


    for column in df.columns:
        # Przygotowanie danych
        data = df.filter([column])
        dataset = data.values
        training_data_len = int(np.ceil( len(dataset) * .95 ))

        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(dataset)

        train_data = scaled_data[0:int(training_data_len), :]
        x_train = []
        y_train = []

        for i in range(60, len(train_data)):
            x_train.append(train_data[i-60:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Budowanie modelu LSTM
        model = Sequential()
        model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
        model.add(LSTM(64, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')

        model.fit(x_train, y_train, batch_size=1, epochs=1)

        # Tworzenie testowego zestawu danych
        test_data = scaled_data[training_data_len - 60: , :]

        x_test = []
        y_test = dataset[training_data_len:, :]

        for i in range(60, len(test_data)):
            x_test.append(test_data[i-60:i, 0])
            
        x_test = np.array(x_test)

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

        # Przewidzenia cen na próbce testowej
        predictions = model.predict(x_test)
        predictions = scaler.inverse_transform(predictions)

        # Wizualizacja przewidywań
        train = data[:training_data_len]
        valid = data[training_data_len:]
        valid['Predictions'] = predictions
        
        output[column] = valid

    return output


