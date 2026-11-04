import argparse

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
from analyze_alert_errors import analyze_alert_errors

from methods import (
        persistence_method, 
        seasonal_persistence_method, 
        moving_average_method, 
        linear_regression_method
        )

from deviation_alerts import (
    get_predictions,
    calculate_deviation_thresholds,
    evaluate_deviation_alerts
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
    
    train_end = int(len(df) * 0.64)
    validation_end = int(len(df) * 0.8)
    train_start = validation_end

    thresholds = calculate_high_load_thresholds(
        df, zones, split_idx, percentile
    )

    return {
            'df' : df, 
            'zones' : zones, 
            'horizon' : horizon, 
            'daily_period' : daily_period, 
            'split_idx' : split_idx,
            'train end' : train_end,
            'validation end' : validation_end,
            'train start' : train_start,
            'percentile' : percentile, 
            'thresholds' : thresholds
            }


def run_forecasting(data):
    df = data['df']
    zones = data['zones']
    horizon = data['horizon']
    daily_period = data['daily_period']
    split_idx = data['split_idx']
    
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

def run_comparison(data, methods):
    comparison = method_comparison(
            methods,
            data['df'],
            data['zones'],
            data['horizon'],
            data['daily_period'],
            data['split_idx']
            )
    
    output_file = EVALUATIONS_DIR/'forecasting_comparison.csv'
    comparison.to_csv(
            output_file,
            index=False,
            sep=';'
            )
    print('\nForcasting comparison:')
    print(comparison.to_string(index=False))
    print(f'\nSaved to {output_file}')

def run_alert_evaluation(data, methods):
    all_results = []

    for model_name, method_result in methods.items():
        for result in method_result:
            item = result.copy()
            item['Model'] = model_name
            all_results.append(item)

    comparison = evaluate_high_load_alerts(
        all_results,
        data['thresholds']
    )

    output_file = EVALUATIONS_DIR / 'high_load_alert_evaluation.csv'

    comparison.to_csv(
        output_file,
        index=False,
        sep=';'
    )

    print('\nHigh-load alert evaluation:')
    print(comparison.to_string(index=False))
    print(f'\nSaved to: {output_file}')

def run_threshold_analysis(data):
    summary_df = plot_analyze_threshold(
        data['df'],
        data['zones'],
        data['split_idx'],
        data['thresholds']
    )

    print('\nThreshold analysis:')
    print(summary_df.to_string(index=False))

    plot_load_threshold_timeseries(
        data['df'],
        data['zones'],
        data['split_idx'],
        data['thresholds']
    )

def run_forecast_plots(data, methods):
    for method_name, method_result in methods.items():
        plot_load_thresholds(
            data['df'],
            method_result,
            data['zones'],
            data['thresholds'],
            data['horizon'],
            method_name,
            days=14
        )

def run_error_analysis(data, methods):
    all_results = []
    for model_name, method_results in methods.items():
        for result in method_results:
            item = result.copy()
            item['Model'] = model_name
            all_results.append(item)

    error_df = analyze_alert_errors(
            all_results, data['thresholds']
            )

    output_file = EVALUATIONS_DIR/'alert_evaluation_Analysis'

    error_df.to_csv(
            output_file,
            index=False,
            sep=';'
            )

    print('\nAlert error analysis')
    print(error_df.to_string(index=False))
    print(f'Saved to {output_file}')

def run_deviation_alerts(data):
    df = data['df']
    zones = data['zones']
    horizon = data['horizon']
    daily_period = data['daily period']
    train_end = data['train end']
    validation_end = data['validation end']
    test_start = data['test start']

    prediction = get_predictions(
            zones,
            horizon,
            daily_period,
            train_end,
            validation_end
            ) 

    thresholds = calculate_deviation_thresholds(
        predictions,
        train_end,
        validation_end,
        percentile=95
    )

    evaluation = evaluate_deviation_alerts(
        predictions,
        thresholds,
        test_start
    )

    output_file = (
        EVALUATIONS_DIR / "deviation_alert_evaluation.csv"
    )

    evaluation.to_csv(
        output_file,
        index=False,
        sep=";"
    )

    print("\nDeviation Alert Evaluation:")
    print(evaluation.to_string(index=False))
    print(f"\nSaved to: {output_file}")


def run_all(data, methods):
    run_comparison(data, methods)
    run_alert_evaluation(data, methods)
    run_threshold_analysis(data)
    run_forecast_plots(data, methods)
    run_error_analysis(data, methods)
    run_deviation_alerts(data)

def main():
    parser = argparse.ArgumentParser(
            description='Electricity Load Forecasting Pipeline'
            )

    parser.add_argument(
            '--stage',
            choices=[
                'all',
                'forecast',
                'comparison', 
                'alerts',
                'threshold',
                'plots',
                'errors',
                'deviation'
                ],
            default='all',
            help = 'Pipeline stage to run'
            )

    args = parser.parse_args()
    
    # Prepare dataset configuration
    data = prepare_data()

    # Forecasting is required for these stages
    if args.stage in [
        'all',
        'forecast',
        'comparison',
        'alerts',
        'plots',
        'errors',
        'deviation'
    ]:
        methods = run_forecasting(data)

    else:
        methods = None

    if args.stage == 'all':
        run_all(data, methods)

    elif args.stage == 'forecast':
        print('Forecasting completed')

    elif args.stage == 'comparison':
        comparison = run_comparison(data, methods)


    elif args.stage == 'alerts':
        run_alert_evaluation(data, methods)

    elif args.stage == 'threshold':
        run_threshold_analysis(data)

    elif args.stage == 'plots':
        run_forecast_plots(data, methods)

    elif args.stage == 'errors':
        run_error_analysis(data, methods)

    elif args.stage == 'errors':
        run_deviation_alerts(data)


if __name__=='__main__':
    main()

