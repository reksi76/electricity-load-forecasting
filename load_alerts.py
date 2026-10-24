import pandas as pd 

def calculate_high_load_treshold(df, zones, split_idx, percentile=95):
    treshold = {}

    for zone in zones:
        train_consumption = df['zone'].iloc[:split_idx].dropna()

        treshold[zone] = train_consumption.quantile(
                percentile/100
                )

        return treshold

def detect_high_load(prediction, treshold):
    if predicition >= treshold:
        return {
                'Status' : 'HIGH LOAD',
                'Prediction' : prediction,
                'Treshold' : treshold,
                'Message' : 'Prediksi konsumsi mencapai atau melampaui ambang'
                }

    return {
            'Status' : 'Normal',
            'Prediction' : prediction,
            'Treshold' : treshold,
            'Message' : 'Prediksi konsumsi berada di bawah ambang'
            }
