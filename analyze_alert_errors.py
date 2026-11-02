import pandas as pd 


def analyze_alert_errors(method_results, thresholds):
    errors = []

    for item in method_results:
        zone = item['Zone']
        model = item.get('Model', 'Unknown')

        y_actual = item['Actual']
        y_prediction = item['Prediction']
        threshold = thresholds[zone]

        y_actual, y_prediction = y_actual.align(
                y_prediction,
                join='inner'
                )

        valid = y_actual.notna() & y_prediction.notna()

        y_actual = y_actual.loc[valid]
        y_prediction = y_prediction.loc[valid]

        # Classify high-load events
        actual_high = y_actual >= threshold
        predicted_high = y_prediction >= threshold

        # Identify high positives and false negatives
        false_positive = predicted_high & ~actual_high
        false_negative = actual_high & ~predicted_high

        for timestamp in y_actual.index[false_positive]:
            actual_value = y_actual.loc[timestamp]
            prediction_value = y_prediction.loc[timestamp]

            errors.append({
                'Zone': zone,
                'Model': model,
                'Target time': timestamp,
                'Actual': actual_value,
                'Forecast': prediction_value,
                'Threshold': threshold,
                'Error type': 'FP',
                'Forecast error': prediction_value - actual_value
            })

        for timestamp in y_actual.index[false_negative]:
            actual_value = y_actual.loc[timestamp]
            prediction_value = y_prediction.loc[timestamp]

            errors.append({
                'Zone': zone,
                'Model': model,
                'Target time': timestamp,
                'Actual': actual_value,
                'Forecast': prediction_value,
                'Threshold': threshold,
                'Error type': 'FN',
                'Forecast error': prediction_value - actual_value
            })

        return pd.DataFrame(errors)
             
