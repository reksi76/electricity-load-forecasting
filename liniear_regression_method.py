import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))



import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error 
from data_audit import file_info


# df = pd.read_csv('Tetuan City power consumption.csv')
df = file_info(verbose=False)

zones = [
        'Zone 1 Power Consumption',
        'Zone 2 Power Consumption',
        'Zone 3 Power Consumption'
        ]

horizon = 6
split_idx = int(len(df) * 0.8)

features = [
        'lag_0', 
        'lag_1',
        'lag_2',
        'Temperature',
        'Humidity',
        'Wind Speed'
        ]

results = []

for zone in zones:
    data = pd.DataFrame(index=df.index)
    data['lag_0'] = df[zone]
    data['lag_1'] = df[zone].shift(1)
    data['lag_2'] = df[zone].shift(2)

    data['Temperature'] = df['Temperature']
    data['Humidity'] = df['Humidity']
    data['Wind Speed'] = df['Wind Speed']

    data['target'] = df[zone].shift(-horizon)
    data = data.dropna()

    train = data.loc[data.index < split_idx - horizon]
    test = data.loc[data.index >= split_idx]
    
    x_train = train[features]
    y_train = train['target']

    x_test = test[features]
    y_test = test['target']

    model = LinearRegression()
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    mae = mean_absolute_error(y_test, y_pred)

    results.append({
        'Zone' : zone, 
        'MAE' : mae,
        'Jumlah pengujian' : len(y_test)
        })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
    

