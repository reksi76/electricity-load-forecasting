import pandas as pd 
import numpy as np 

from sklearn.linear_model import LinearRegression 
from sklearn.metrics import (
        mean_absolute_error, 
        confusion_matrix, 
        precision_score,
        recall_score,
        f1_score
        )

from data_audit import file_info
from load_alerts import calculate_high_load_thresholds

def evaluate_high_load_alerts(
        df,
        zones, 
        horizon,
        daily_period,
        split_idx,
        percentile
    ):

    selected_models = {
            zones[0] : 'Seasonal Persistence',
            zones[1] : 'Linear Regression',
            zones[2] : 'Seasonal Persistence',
            }

    thresholds = calculate_high_load_thresholds(
            df, zones, split_idx, percentile
            )

    # Alerts evaluation on test data 

    results = []

    for zone in zones:
        actual = df[zone].shift(-horizon)

        if selected_models[zone] == 'Seasonal Persistence':

            prediction = df[zone].shift(
                    daily_period - horizon
                    )
        else:
            data = pd.DataFrame(index=df.index)
            data['lag_0'] = df[zone]
            data['lag_1'] = df[zone].shift(1)
            data['lag_2'] = df[zone].shift(2)

            data['Temperature'] = df['Temperature']
            data['Humidity'] = df['Humidity']
            data['Wind Speed'] = df['Wind Speed']

            data['target'] = actual 
            data['position'] = np.arange(len(df))

            features = [
                    'lag_0',
                    'lag_1',
                    'lag_2',
                    'Temperature',
                    'Humidity',
                    'Wind Speed'
                    ]
                
            data = data.dropna()

            train = data[data['position'] < split_idx - horizon]
            test = data[data['position'] >= split_idx]

            model = LinearRegression()
            model.fit(
                    train[features], 
                    train['target']
                    )
            prediction = pd.Series(
                    model.predict(test[features]), 
                    index = test.index
                    )
        test_index = df.index[split_idx:]
        eval_index = test_index.intersection(prediction.index)
        y_actual = actual.loc[eval_index]
        y_prediction = prediction.loc[eval_index]

        valid = y_actual.notna() & y_prediction.notna()

        y_actual = y_actual.loc[valid]
        y_prediction = y_prediction.loc[valid]

        threshold = thresholds[zone]

        actual_high = y_actual  >= threshold
        predicted_high = y_prediction  >= threshold

        tn, fp, fn, tp = confusion_matrix(
                actual_high,
                predicted_high,
                labels=[False, True]
                ).ravel()

        results.append({
            'Zone' : zone,
            'Model' : selected_models[zone],
            'Jumlah test' : len(y_actual),
            'MAE' : mean_absolute_error(
                y_actual, y_prediction
                ),
            'Ambang' : threshold,
            'Kejadian aktual tinggi' : int(actual_high.sum()),
            'Peringatan' : int(predicted_high.sum()),
            'TP' : int(tp),
            'FP' : int(fp),
            'FN' : int(fn), 
            'TN' : int(tn),
            'Precision' : precision_score(
                actual_high, predicted_high,
                zero_division=0
                ),
            'Recall' : recall_score(
                actual_high, predicted_high, 
                zero_division=0
                ),
            'F1' : f1_score(
                actual_high, predicted_high,
                zero_division=0
                )
            })

    comparison = pd.DataFrame(results)
    return comparison




