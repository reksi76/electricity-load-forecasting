import pandas as pd 


def summarize_alert_errors(error_df, zones, models):
    all_combinations = pd.MultiIndex.from_product(
            [zones, models],
            names=['Zone', 'Model']
            )

    summary = (
            error_df
            .groupby(['Zone', 'Model', 'Error type'])
            .size()
            .unstack(fill_value=0)
            .reindex(all_combinations, fill_value=0)
            .reset_index()
            )

    for error_type in ['FP', 'FN']:
        if error_type not in summary.columns:
            summary[error_type] = 0

    summary['Total error'] = summary['FP'] + summary['FN']

    summary = summary[
            ['Zone', 'Model', 'FP', 'FN', 'Total error']
            ]

    return summary.sort_values(['Zone', 'Model', 'FP', 'FN']).reset_index(drop=True)

if __name__ == '__main__':
    zones = [
    "Zone 1 Power Consumption",
    "Zone 2 Power Consumption",
    "Zone 3 Power Consumption"
    ]

    models = [
        "Persistence",
        "Seasonal Persistence",
        "Moving Average",
        "Linear Regression"
    ]
        
    input_path = './outputs/evaluations/alert_evaluation_Analysis.csv'
    output_path= './outputs/evaluations/alert_error_summary.csv'

    error_df = pd.read_csv(input_path, sep=';')
    summary_df = summarize_alert_errors(error_df, zones, models)

    summary_df.to_csv(output_path, index=False, sep=';')

    print(summary_df.to_string(index=False))
    print('Number of Model-Zone combination:',len(summary_df))
    print('Total FN/FP occurencess:', summary_df['Total error'].sum())
    print('Saved to', output_path)



