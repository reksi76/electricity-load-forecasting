import pandas as pd 

from config import DATA_PATH

def file_info(verbose=True):
    df = pd.read_csv(DATA_PATH)
    df['DateTime'] = pd.to_datetime(
            df['DateTime'],
            format = '%m/%d/%Y %H:%M',
            errors='coerce'

            )
    if verbose:
        # Check for missing values
        print('== Missing Values ===')
        print(df.isna().sum())

        # Check for duplicates
        print('\n === DUPLICATE ROWS ===')
        print('Duplikat seluruh baris:', df.duplicated().sum())
        print('Duplikat timestamp:', df['DateTime'].duplicated().sum())

        # Time Range
        print('\n=== TIME RANGE ===')
        print('Awal', df['DateTime'].min())
        print('Akhir', df['DateTime'].max())
        print('Jumlah rentang waktu:', df['DateTime'].nunique())

        # Time Interval
        df = df.sort_values('DateTime').reset_index(drop=True)
        interval = df['DateTime'].diff().dropna()

        print('\n=== TIME INTERVAL ===')
        print(interval.value_counts().head(10))
    
        # Check minimum and maximum values
        numeric_cols = df.select_dtypes(include='number').columns

        print('\n=== NUMERIC RANGES ===')
        print(df[numeric_cols].agg(['min', 'max']).T)

    return df
