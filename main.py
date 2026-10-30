from config import EVALUATIONS_DIR
from data_audit import file_info
from compare_models import method_comparison
from load_alerts import calculate_high_load_thresholds, detect_high_load
from evaluate_alerts import evaluate_high_load_alerts
from analyze_thresholds import (
    plot_analyze_threshold,
    plot_load_threshold_timeseries
    )
from plot_forecast import plot_load_thresholds

from methods import (
        persistence_method, 
        seasonal_persistence_method, 
        moving_average_method, 
        linear_regression_method
        )

import pandas as pd

def prepare_data():
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
    thresholds = calculate_high_load_thresholds(
        df, zones, split_idx, percentile
    )

    return {
            'df' : df, 
            'zones' : zones, 
            'horizon' : horizon, 
            'daily_period' : daily_period, 
            'split_idx' : split_idx, 
            'percentile' : percentile, 
            'thresholds' : thresholds
            }


def run_forecasting(
        df, zones,  horizon, 
        daily_period, split_idx
        ):
    
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
    return methods

def main():
    # 1. Prepare data and experiment parameters
    data = prepare_data()

    df = data['df']
    zones = data['zones']
    horizon = data['horizon']
    daily_period = data['daily_period']
    split_idx = data['split_idx']
    thresholds = data['thresholds']

    # 2. Run forecasting methods
    methods = run_forecasting(
        df,
        zones,
        horizon,
        daily_period,
        split_idx
    )

    # 3. Compare forecasting performance
    results = method_comparison(
        methods,
        df,
        zones,
        horizon,
        daily_period,
        split_idx
        )
    # 4. Evaluate high-load alerts 
    all_results = []
    for model_name, method_result in results:
        for result in results:
            item = result.copy()
            item['Model'] = model_name
            all_results.append(item)

    comparison = evaluate_high_load_alerts(
            all_results, thresholds
            )
    #print('High load Alert Evaluation:')
    #print(comparison.to_string(index=False)

    comparison.to_csv(
            EVALUATIONS_DIR/'high_load_alert_evaluation.csv',
            index=False,
            sep=';'
            )

    # 5. Analyze threshold distribution
    summary_df = plot_analyze_threshold(
        df,
        zones,
        split_idx,
        thresholds,
    )

    print('\nThreshold Analysis:')
    print(summary_df.to_string(index=False))

    # 6. Plot actual consumption and thresholds
    plot_load_threshold_timeseries(
        df,
        zones,
        split_idx,
        thresholds,
    )

    # 7. Plot actual consumption, forecast, and high-load threshold
    plot_load_thresholds(
            df, 
            method_result, 
            zones, 
            thresholds,
            horizon,
            days=14
            )

if __name__=='__main':
    main()

