from config import DATA_PATH
import pandas as pd
import matplotlib.pyplot as plt

# Baca dataset
df = pd.read_csv(DATA_PATH)

df["DateTime"] = pd.to_datetime(
    df["DateTime"],
    format="%m/%d/%Y %H:%M",
    errors="coerce"
)

# Rapikan nama kolom
df.columns = df.columns.str.strip().str.replace(
    r"\s+", " ", regex=True
)

# Urutan hari seperti pada grafik paper
days = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

df["Weekday"] = df["DateTime"].dt.day_name()

zones = [
    "Zone 1 Power Consumption",
    "Zone 2 Power Consumption",
    "Zone 3 Power Consumption"
]

for zone in zones:
    print(f"\n{'=' * 60}")
    print(f"STATISTIK: {zone}")

    # Statistik untuk setiap hari
    stats = df.groupby("Weekday")[zone].agg(
        count="count",
        minimum="min",
        Q1=lambda x: x.quantile(0.25),
        median="median",
        Q3=lambda x: x.quantile(0.75),
        maximum="max"
    ).reindex(days)

    print(stats.round(2))

    # Buat boxplot
    data = [
        df.loc[df["Weekday"] == day, zone].dropna()
        for day in days
    ]

    plt.figure(figsize=(9, 5))
    plt.boxplot(data, tick_labels=day_labels)
    plt.xlabel("Weekdays")
    plt.ylabel("Reported consumption value")
    plt.title(f"Weekly Distribution - {zone}")
    plt.grid(axis="y", alpha=0.4)
    plt.tight_layout()
    plt.show()

