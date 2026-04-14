# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_plots():
    data_path = os.path.join('data', 'tmd_data.csv')
    df = pd.read_csv(data_path)
    df['metal'] = df['formula'].str.extract(r'^([A-Z][a-z]?)')[0]
    top_spacegroups = df['spacegroup'].value_counts().nlargest(5).index.tolist()
    df_top_sg = df[df['spacegroup'].isin(top_spacegroups)]
    print('--- Included Space Groups and Counts ---')
    sg_counts = df_top_sg['spacegroup'].value_counts()
    for sg, count in sg_counts.items():
        print('Space Group ' + str(sg) + ': ' + str(count) + ' materials')
    print('\n--- Included Transition Metals and Counts ---')
    metal_counts = df['metal'].value_counts()
    for m, count in metal_counts.items():
        print('Transition Metal ' + str(m) + ': ' + str(count) + ' materials')
    plt.rcParams['text.usetex'] = False
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    sns.violinplot(data=df_top_sg, x='spacegroup', y='dos_at_fermi', ax=axes[0, 0], inner='quartile')
    axes[0, 0].set_title('Distribution of DOS at Fermi Level by Space Group')
    axes[0, 0].set_xlabel('Space Group')
    axes[0, 0].set_ylabel('DOS at Fermi Level (states/eV)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    sns.scatterplot(data=df, x='band_gap', y='energy_above_hull', ax=axes[0, 1], alpha=0.7)
    axes[0, 1].set_title('Thermodynamic Stability vs. Band Gap')
    axes[0, 1].set_xlabel('Band Gap (eV)')
    axes[0, 1].set_ylabel('Energy Above Hull (eV/atom)')
    sns.boxplot(data=df, x='metal', y='dos_at_fermi', ax=axes[1, 0])
    axes[1, 0].set_title('DOS at Fermi Level by Transition Metal')
    axes[1, 0].set_xlabel('Transition Metal')
    axes[1, 0].set_ylabel('DOS at Fermi Level (states/eV)')
    pivot_df = df_top_sg.pivot_table(values='dos_at_fermi', index='metal', columns='spacegroup', aggfunc='mean')
    sns.heatmap(pivot_df, annot=True, cmap='viridis', ax=axes[1, 1], fmt='.2f', cbar_kws={'label': 'Mean DOS (states/eV)'})
    axes[1, 1].set_title('Mean DOS at Fermi Level: Metal vs. Space Group')
    axes[1, 1].set_xlabel('Space Group')
    axes[1, 1].set_ylabel('Transition Metal')
    axes[1, 1].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    timestamp = int(time.time())
    plot_filename = 'tmd_analysis_plots_' + str(timestamp) + '.png'
    plot_filepath = os.path.join('data', plot_filename)
    fig.savefig(plot_filepath, dpi=300)
    plt.close(fig)
    print('\nPlot saved to ' + plot_filepath)

if __name__ == '__main__':
    generate_plots()