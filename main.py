import sys 
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from data_audit import file_info
from compare_models import method_comparison
from load_alerts import calculate_high_load_thresholds, detect_high_load
from evaluate_alerts import evaluate_high_load_alerts
from methods import (
        persistence_method, 
        seasonal_persistence_method, 
        moving_average_method, 
        linear_regression_method
        )

import pandas as pd

df = file_info(verbose=False)
zones = [
        'Zone 1 Power Consumption',
        'Zone 2 Power Consumption',
        'Zone 3 Power Consumption'
        ]
horizon = 6
daily_period = 144
split_idx = int(len(df) * 0.8)
percentile = 95

methods = {
        'Persistence' : persistence_method(
            df, zones, horizon, split_idx
            ),
        'Seasonal Persistence' : seasonal_persistence_method(
            df, zones, horizon, split_idx, daily_period
            ),
        'Moving Average' : moving_average_method(
            df, zones, horizon, split_idx
            ),
        'Linear Regression' : linear_regression_method(
            df, zones, horizon, split_idx
            )
    }

results = method_comparison(
        methods, df, zones, horizon, 
        daily_period, split_idx,
        )
compare = pd.DataFrame(results)
print(compare.to_string(index=False))

print('\nAmbang konsumsi tinggi per zona:')
thresholds = calculate_high_load_thresholds(
        df, zones, split_idx, percentile
        )
for zone, threshold in thresholds.items():
    # print(f'{zone} : {threshold:.2f}')
    alert = detect_high_load(threshold)

    print('\nZona:', zone)
    print('Status:', alert['Status'])
    print(f'Prediksi: {alert['Prediction']:.2f}')
    print('Pesan:', alert['Message'])

evaluate_high_load_alerts(
    df,
    zones, 
    horizon,
    daily_period,
    split_idx,
    percentile
    )


        


