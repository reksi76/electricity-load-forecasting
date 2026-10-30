import matplotlib.pyplot as plt 

from config import FIGURES_DIR 

def plot_load_thresholds(
        df, 
        method_results, 
        zones, 
        thresholds,
        horizon, 
        days = 14
        ):
    """
    Plot actual consumption, forecast, and high-load threshold
    over the final `days` of the test period.

    `method_results` is the list returned by one forecasting method.
    """

    time = df['DateTime']
    split_time = time.iloc[split_idx] if isinstance(
            (time, pd.Series)
            ) else: time[split_idx]

    fig, axes = plt.subplots(
            nrows=len(zones),
            ncols=1, 
            figsize=(15, 4*len(zones)),
            sharex=True
            )

    if len(zones) == 1: 
        axes = [axes]

    for ax, zone in zip(axes, zones):
        result = next(
                item for item in method_results if item['Zone'] == zone, 
                None
                )

        if result is None:
            ax.set_title(f'{zone} - No forecast result')

        actual = result['Actual']
        prediction = result['Prediction']

        position = df.index.get_indexer(actual.index)

        if (position < 0).any:
            raise ValueError(
                    f'The prediction index result does 
                    not match the df for {zone}'
                    )

        target position = position + horizon 
        valid_position = target_position < len(df)

        actual = actual.iloc[target_position]
        prediction = prediksi.iloc[valid_position]
        target_positions = target_position[valid_position]

        target_times = time[target_position].to_numpy()

        plot_data = pd.DataFrame({
                'time' :taget_times,
                'actual' : actual.to_numpy,
                'prediction' : prediction.to_numpy()
                })

        if plot_data.empty():
            ax.set_title(f'{zone} - no valid data')
            continue

        end_time = plot_data['time'].max()
        start_time = end_time - pd.Timedelta(days=days)
        plot_data = plot_data[
                plot_data['time'] >= start_time
                ]

        threshold = thresholds[zone]

        ax.plot(
                data['time'], 
                data['actual'],
                linewidth=1,
                label='Actual'
                )

         ax.plot(
                data['time'], 
                data['prediction'],
                linewidth=1,
                label='Forecast'
                )

        ax.axhline(
                threshold, 
                linestyle='--',
                linewidth=1.5,
                label=(f'Threshold P95: {threshold}')
                )

        ax.set_title(zone)
        ax.set_ylabel('Power Consumption')
        ax.legend()
        ax.grid(alpha=0.2)

    axes[-1].set_xlabel('Target time')
    fig.suptitle(
            'Actual Consumption and High-load threshold',
            fontsize=14
            )

    fig.tight_layout()
    fig.savefig(FIGURES_DIR/f'forecast_alert.png')

