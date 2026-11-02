from main import prepare_data, run_forecasting
from plot_forecast import plot_load_thresholds
from compare_models import method_comparison
from evaluate_alerts import evaluate_high_load_alerts

PLOT_LOAD_THRESHOLD= False

data = prepare_data()
methods = run_forecasting(
        data['df'],
        data['zones'],
        data['horizon'],
        data['daily_period'],
        data['split_idx'],
        )
results = method_comparison(
    methods,
    data['df'],
    data['zones'],
    data['horizon'],
    data['daily_period'],
    data['split_idx'],
    )
#print(results)
all_results = []
for model_name, method_result in methods.items():
    for result in method_result:
        #item = method_result.copy()
        item = result.copy()
        item['Model'] = model_name
        all_results.append(item)

if PLOT_LOAD_THRESHOLD:
    for method_name, method in methods.items():
        method_result = methods[method_name]


        plot_load_thresholds(
            data['df'],
            method_result,
            data['zones'],
            data['split_idx'],
            data['thresholds'],
            data['horizon'],
            method_name,
            days=14,
            )
comparison = evaluate_high_load_alerts(
        all_results, data['thresholds']
        )

summary = comparison[
        [
        'Zone',
        'Model',
        'MAE',
        'Kejadian aktual tinggi',
        'Peringatan',
        'TP',
        'FP',
        'FN',
        'Precision',
        'Recall',
        'F1',
            ]
        ].sort_values(
                ['Zone', 'F1'],
                ascending=[True, False]
                )
print('\nAlert performance ranking:')
print(summary.to_string(index=False))
