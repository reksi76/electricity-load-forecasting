import sys 
import os 

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from data_audit import file_info
from methods import (
        persistence_method, 
        seasonal_persistence_method, 
        moving_average_method, 
        linear_regression_method
        )

df = file_info(verbose=False)
zones = [
        'Zone 1 Power Consumption',
        'Zone 2 Power Consumption',
        'Zone 3 Power Consumption'
        ]
horizon = 6
split_idx = int(len(df) * 0.8)
