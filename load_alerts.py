import pandas as pd 

def calculate_high_load_thresholds(df, zones, split_idx, percentile):
    thresholds = {}

    for zone in zones:
        train_consumption = df[zone].iloc[:split_idx].dropna()

        thresholds[zone] = train_consumption.quantile(
                percentile/100
                )

    return thresholds

def detect_high_load(threshold):
    prediction = threshold * 1.02
    print(prediction)
    if prediction >= threshold:
        return {
                'Status' : 'HIGH LOAD',
                'Prediction' : prediction,
                'Treshold' : threshold,
                'Message' : 'Prediksi konsumsi mencapai atau melampaui ambang'
                }

    return {
            'Status' : 'Normal',
            'Prediction' : prediction,
            'Treshold' : threshold,
            'Message' : 'Prediksi konsumsi berada di bawah ambang'
            }
