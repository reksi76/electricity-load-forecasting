from main import prepare_data, run_forecasting
from plot_forecast import plot_load_thresholds

data = prepare_data()
methods = run_forecasting(
        data['df'],
        data['zones'],
        data['horizon'],
        data['daily_period'],
        data['split_idx'],
        )
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
