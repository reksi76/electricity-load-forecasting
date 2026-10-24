import sys 
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from data_audit import file_info
from compare_models import method_comparison
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


