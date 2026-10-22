import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

import pandas as pd 
from sklearn.metrics import mean_absolute_error 
from data_audit import file_info

df = file_info(verbose=False)

zones = [
        'Zone 1 Power Consumption',
        'Zone 2 Power Consumption',
        'Zone 3 Power Consumption'
        ]

horizon = 6
daily_period = 144
split_idx = int(len(df) * 0.8)

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
