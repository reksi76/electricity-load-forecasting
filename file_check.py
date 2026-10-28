import pandas as pd 

from config import DATA_PATH

df = pd.read_csv(DATA_PATH)

print(df.head())

print('Ukuran dataset: ', df.shape)

print('Nama kolom:')
print(df.columns.tolist())

print('Informasi dataset:', df.info())

df['DateTime'] = pd.to_datetime(
        df['DateTime'],
        format='%m/%d/%Y %H:%M',
        errors='coerce'
        )

df.columns = df.columns.str.strip().str.replace(r'\s+', ' ', regex=True)

df['Hour'] = df['DateTime'].dt.hour
df['Day'] = df['DateTime'].dt.day
df['Month'] = df['DateTime'].dt.month
df['DayOfWeek'] = df['DateTime'].dt.day_name()


print(df[['DateTime', 'Hour', 'Day', 'Month', 'DayOfWeek']].head(10))
print(df[['DateTime']].head())
print('Timestamp gagal dibaca:', df['DateTime'].isna().sum())
print('\n=== DATA SHAPE ===')
print(df.shape)
