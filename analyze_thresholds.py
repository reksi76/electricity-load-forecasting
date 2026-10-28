import pandas as pd 
import matplotlib.pyplot as plt 

from config import FIGURES_DIR


def plot_analyze_threshold(
        df, zones, split_idx, thresholds
        ):
    summary = []
    for zone in zones:
        print(zone)
        train = df[zone].iloc[:split_idx].dropna()
        test = df[zone].iloc[split_idx:].dropna()
        threshold = thresholds[zone]

        test_high = test >= threshold

        summary.append({
            'Zone' : zone,
            'Training mean' : train.mean(),
            'Testing mean' : test.mean(),
            'Training P95' : train.quantile(0.95),
            'Testing P95' : test.quantile(0.95),
            'Threshold' : threshold,
            'Testing minimum' : test.min(),
            'Testing maximum' : test.max(),
            'Testing above threshold' : int(test_high.sum()),
            'Testing below threshold' : int((~test_high).sum()),
            'Testing exceedance (%)' : test_high.mean() * 100,
            })

    summary_df = pd.DataFrame(summary)

    print('\nAnalisis distribusi dan ambang tinggi:')
    print(summary_df.round(2).to_string(index=False))

    # Graphic Visualization
    fig, axes = plt.subplots(
            nrows = len(zones),
            ncols = 1,
            figsize=(10, 4*len(zones))
            )

    if len(zones) == 1:
        axes = [axes]

    for ax, zone in zip(axes, zones):
        train = df[zone].iloc[:split_idx].dropna()
        test = df[zone].iloc[split_idx:].dropna()
        threshold = thresholds[zone]

        ax.hist(
                train, 
                bins=40,
                alpha=0.5,
                density=True,
                label='Training'
                )

        ax.hist(
                test,
                bins=40,
                alpha=0.5,
                density=True,
                label='Testing'
                )

        ax.axvline(
                threshold,
                linestyle='--',
                linewidth=2,
                label=(f'Threshold P95 = {threshold:.2f}')
                )

        ax.set_title(zone)
        ax.set_xlabel('Power Consumption')
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(alpha=0.2)

    plt.tight_layout()
    plt.savefig(
            FIGURES_DIR
            /'threshold_distribution.png',
            dpi=150,
            bbox_inches='tight'
            )
    plt.show()

    return summary_df


def plot_load_threshold_timeseries(
        df, 
        zones, 
        split_idx,
        thresholds, 
        ):
    
    split_time = df['DateTime'].iloc[split_idx]

    fig, axes = plt.subplots(
            nrows=len(zones),
            ncols=1,
            figsize=(15, 12),
            sharex=True
            )

    for ax, zone in zip(axes, zones):
        threshold = thresholds[zone]

        ax.plot(
                df['DateTime'],
                df[zone],
                linewidth=0.7,
                label='Actual Consumption',
                )

        ax.axhline(
                threshold,
                linestyle='--',
                linewidth=1.5,
                label=f"Training P95 = {threshold:2f}",
                )

        ax.axvline(
                split_time,
                linestyle=':',
                linewidth=1.5,
                label='Training/testing split'
                )
        
        ax.set_title(zone)
        ax.set_ylabel('Power Consumption')
        ax.legend()
        ax.grid(alpha=0.2)

    axes[-1].set_xlabel('Date')

    fig.suptitle(
            'Actual Power Consumption and High-load Threshold'
            )
    fig.tight_layout()

    fig.savefig(
            FIGURES_DIR
            /'load_threshold_timeseries.png',
            dpi=150,
            bbox_inches='tight'
            )
    plt.show()

