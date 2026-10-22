import os 
import sys 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pandas as pd 
from sklearn.metrics import mean_absolute_error 
from data_audit import file_info 

df = file_info(verbose=False)

zones = (
        'Zone 1 Power Consumption',
        'Zone 2 Power Consumption',
        'Zone 3 Power Consumption'
        )

horizon = 6
window = 6
split_idx = int(len(df) * 0.8)

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

