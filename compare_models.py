import pandas as pd 

def method_comparison(
        methods, df, zones, horizon, 
        daily_period, split_idx,
        ):
    results = []

    for method_name, method_result in methods.items():
        for result in method_result:
            results.append({
                    'Metode' : method_name,
                    'Zona' : result['Zone'],
                    'MAE' : result['MAE'],
                    'Jumlah Pengujian' : result['Jumlah pengujian']
                    })

    # comparison = pd.DataFrame(result)
    # print(comparison.to_string(index=False))
    return results


