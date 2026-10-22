import numpy as np 
from sklearn.metrics import mean_absolute_error 
from sklearn.linear_model import LinearRegression
import pandas as pd 


def persistence_method(df, zones, horizon, split_idx, daily_period):
    results = []

    for zone in zones:
        actual = df[zone].shift(-horizon)
        prediction = df[zone]
    
        y_test = actual.iloc[split_idx:]
        y_pred = prediction.iloc[split_idx:]


        valid = y_test.notna() & y_pred.notna()

        mae = mean_absolute_error(
                y_test[valid],
                y_pred[valid]
                )

        results.append({
            'Zone' : zone,
            'MAE' : mae, 
            'Jumlah pengujian' : int(valid.sum())
            })


    baseline_results = pd.DataFrame(results)
    # print(baseline_results.to_string(index=False))
    return results

def seasonal_persistence_method(df, zones, horizon, split_idx):
    results = []

    for zone in zones:
        actual = df[zone].shift(-horizon)
        prediction = df[zone].shift(daily_period - horizon)

        y_test = actual.iloc[split_idx:]
        x_pred = prediction.iloc[split_idx:]

        valid = y_test.notna() & x_pred.notna()

        mae = mean_absolute_error(
                y_test[valid],
                x_pred[valid]
                )

        results.append({
            'Zone' : zone,
            'MAE' : mae,
            'Jumlah pengujian' : int(valid.sum())
            })

    seasonal_result = pd.DataFrame(results)
    print(seasonal_result.to_string(index=False))
    return results


def moving_average_method(df, zones, horizon, split_idx):
    window = 6
    results = []

    for zone in zones:
        actual = df[zone].shift(-horizon)
        prediction = df[zone].rolling(window=window).mean()

        y_test = actual.iloc[split_idx:]
        y_pred = prediction.iloc[split_idx:]

        valid = y_test.notna() & y_pred.notna()

        mae = mean_absolute_error(
                y_test[valid],
                y_pred[valid]
                )

        results.append({
            'Zone': zone, 
            'MAE' : mae,
            'Jumlah pengujian' : int(valid.sum())
            })

    moving_average_results = pd.DataFrame(results)
    print(moving_average_results.to_string(index=False))
    return results



def linear_regression_method(df, zones, horizon, split_idx):
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

        data['position'] = np.arange(len(df))
        data = data.dropna()

        train = data[
            data['position'] < split_idx - horizon
        ]
        test = data[
            data['position'] >= split_idx
        ]

        if train.empty or test.empty:
            continue

        x_train = train[features]
        y_train = train['target']

        x_test = test[features]
        y_test = test['target']

        model = LinearRegression()
        model.fit(x_train, y_train)

        y_pred = model.predict(x_test)

        mae = mean_absolute_error(y_test, y_pred)

        results.append({
            'Zone': zone,
            'MAE': mae,
            'Jumlah pengujian': len(y_test)
        })

    return results    


