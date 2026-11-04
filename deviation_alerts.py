import pandas as pd 
import numpy as np 

def get_predicition(
        df, 
        zones, 
        horizon, 
        daily_period, 
        train_end, 
        validation_end
        ):
    '''
    Generate validation and test prediction for each model
    and zone 
    The target time t is the consumption at t + horizon
    '''

    results = {}
    test_start = validation_end

    for zone in zones:

        # Persistance Method
        actual = df[zone].shift(-horizon)
        prediction = df[zone]

        results[('Persistance', zone)] = {
                'Actual' : actual, 
                'Prediction' : prediction
                }

        # Seasonal Persistance Method
        prediction = df[zone].shift(daily_period-horizon)

        results[('Seasonal Persistance'), zone] = {
                'Actual' : actual,
                'Prediction' : prediction
                }

        # Moving Average Method
        prediction = df[zone].rolling(window=6).mean()
        results[('Moving Average'), zone] = {
                'Actual' : actual,
                'Prediction' : prediction
                }

        # Linear Regression Method
        data = pd.DtaFrame(index=df.index)

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
        
        train = data[data[position]] <  train_end - horizon
        validation_and_test = data[
                data[position] >=  train_end - horizon
                ]

        if train.empty or validation_and_test.empty:
            continue

        from sk.learn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(train[features], train['target'])

        prediction = pd.Series(
                model.predict(validation_and_test[features]),
                index=validation_and_test.index
                )
        
        results[('Linear Regression', zone)] = {
                'Actual' = actual,
                'Prediction' = prediction
                }

        return results

    def calculate_deviation_threshold(
            prediction,
            validation_start,
            validation_end,
            percentile=95
            ):

        thresholds = {}

        for key, result in prediction.items():

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
                    validation_prediction.notna.()
                    )

            residuals = (
                    validation_actual[valid]
                    - validation_prediction[valid]
                    ).abs()

            if residuals.empty:
                continue

            thresholds = residuals.quartile(percentile/100)
            thresholds[key] = threshold 

        return thresholds

    def evaluate_deviation_alerts(
            prediction,
            thresholds,
            test_start
            ):

        resulta = []
        for key, result in prediction.items():

            model_name, zone = key

            in key not in thresholds:
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



        




