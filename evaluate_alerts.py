import pandas as pd 
import numpy as np 

from sklearn.metrics import (
        mean_absolute_error, 
        confusion_matrix, 
        precision_score,
        recall_score,
        f1_score
        )


def evaluate_high_load_alerts(
        method_results, thresholds
        ):
    results = []

    for item in method_results:
        zone = item['Zone']
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

        if y_actual.empty:
            raise ValueError(
                f"Tidak ada data valid untuk {zone}"
            )

        actual_high = y_actual  >= threshold
        predicted_high = y_prediction  >= threshold

        tn, fp, fn, tp = confusion_matrix(
                actual_high,
                predicted_high,
                labels=[False, True]
                ).ravel()

        results.append({
            'Zone': zone,
            'Model': item.get('Model', 'Unknown'),
            'Jumlah pengujian': len(y_actual),
            'MAE': item.get('MAE'),
            'Ambang': threshold,
            'Kejadian aktual tinggi': int(actual_high.sum()),
            'Peringatan': int(predicted_high.sum()),
            'TP' : int(tp),
            'FP' : int(fp),
            'FN' : int(fn), 
            'TN' : int(tn),
            'Precision' : precision_score(
                actual_high, predicted_high,
                zero_division=0
                ),
            'Recall' : recall_score(
                actual_high, predicted_high, 
                zero_division=0
                ),
            'F1' : f1_score(
                actual_high, predicted_high,
                zero_division=0
                )
            })

    return pd.DataFrame(results)




