import pandas as pd 
import numpy as np 

def get_predictions(
        df, 
        zones, 
        horizon, 
        daily_period, 
        train_end, 
        ):
    '''
    Generate validation and test prediction for each model
    and zone 
    The target time t is the consumption at t + horizon
    '''

    results = {}
    # test_start = validation_end

    for zone in zones:

        # Persistance Method
        actual = df[zone].shift(-horizon)
        prediction = df[zone]

        results[('Persistence', zone)] = {
                'Actual' : actual, 
                'Prediction' : prediction
                }

        # Seasonal Persistence Method
        prediction = df[zone].shift(daily_period-horizon)
        #print('iwashere')

        results[('Seasonal Persistence', zone)] = {
                'Actual' : actual,
                'Prediction' : prediction
                }

        # Moving Average Method
        prediction = df[zone].rolling(window=6).mean()
        results[('Moving Average', zone)] = {
                'Actual' : actual,
                'Prediction' : prediction
                }

        # Linear Regression Method
        data = pd.DataFrame(index=df.index)

        data['lag_0'] = df[zone]
        data['lag_1'] = df[zone].shift(1)
        data['lag_2'] = df[zone].shift(2)

        data['Temperature'] = df['Temperature']
        data['Humidity'] = df['Humidity']
        data['Wind Speed'] = df['Wind Speed']

        data['target'] = df[zone].shift(-horizon)
        data['position'] = np.arange(len(df))

        data = data.dropna()

        features = [
                'lag_0',
                'lag_1',
                'lag_2',
                'Temperature',
                'Humidity',
                'Wind Speed'
                ]
        
        train = data[data['position'] <  train_end - horizon]
        validation_and_test = data[
                data['position'] >=  train_end -        horizon
                ]

        if train.empty or validation_and_test.empty:
            continue

        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(train[features], train['target'])

        prediction = pd.Series(
                np.nan,
                index=df.index,
                dtype=float
                )

        prediction.loc[validation_and_test.index] = model.predict(
                validation_and_test[features]
                )
        
        results[('Linear Regression', zone)] = {
                'Actual' : actual,
                'Prediction' : prediction
                }

    return results

def calculate_deviation_thresholds(
        predictions,
        validation_start,
        validation_end,
        percentile=95
        ):

    thresholds = {}

    for key, result in predictions.items():

        actual = result['Actual']
        prediction = result['Prediction']

        validation_actual = actual.iloc[
                validation_start:validation_end
                ]

        validation_prediction = prediction.iloc[
                validation_start:validation_end
                ]

        valid = (
                validation_actual.notna() & 
                validation_prediction.notna()
                )

        residuals = (
                validation_actual[valid]
                - validation_prediction[valid]
                ).abs()

        if residuals.empty:
            continue

        threshold = residuals.quantile(percentile/100)
        thresholds[key] = threshold 

    return thresholds

def evaluate_deviation_alerts(
        predictions,
        thresholds,
        test_start
        ):

    results = []
    for key, result in predictions.items():

        model_name, zone = key

        if key not in thresholds:
            continue

        actual = result['Actual'].iloc[test_start:]
        prediction = result['Prediction'].iloc[test_start:]

        valid = actual.notna() & prediction.notna()

        actual = actual[valid]
        prediction = prediction[valid]

        residuals = (actual - prediction).abs()

        threshold = thresholds[key]

        alerts = residuals > threshold

        results.append({
            "Model": model_name,
            "Zone": zone,
            "Deviation Threshold": threshold,
            "Jumlah pengujian": len(residuals),
            "Jumlah deviation alert": int(alerts.sum()),
            "Persentase deviation alert": (
                alerts.mean() * 100
            ),
            "Mean Absolute Deviation": residuals.mean(),
            "Maximum Deviation": residuals.max()
        })

    return pd.DataFrame(results)


def extract_deviation_alerts(
        predictions,
        thresholds,
        timestamps,
        test_start,
        horizon,
        interval_minutes
        ):

    start = test_start - horizon

    events = []
    for key, result in predictions.items():

        model_name, zone = key

        if key not in thresholds:
            continue

        actual = result['Actual']
        prediction = result['Prediction']

        target_times = timestamps.iloc[start:]

        valid = (actual.notna() 
                 & prediction.notna()
                 & target_times.notna())

        actual = actual[valid]
        prediction = prediction[valid]

        residuals = (prediction - actual).abs()
        threshold = thresholds[key]

        alerts = residuals > threshold 

        if not alerts.any():
            continue

        alert_indeces  = alerts.index[alerts]

        alert_events = pd.DataFrame({
            'DateTime':(
                pd.to_datetime(target_times.loc[alert_indeces].values)
                + pd.Timedelta(
                    minutes=horizon * interval_minutes
                    )
                ),
            'Model' : model_name,
            'Zone' : zone,
            'Actual' : actual[alerts].values,
            'Prediction' : prediction[alerts].values,
            'Absolute Error' : residuals[alerts].values,
            'Threshold' : threshold

            })

        events.append(alert_events)

    if not events:
        return pd.DataFrame()

    return pd.concat(events, ignore_index=True).sort_values(
            ['Zone', 'DateTime']
            )

                      
