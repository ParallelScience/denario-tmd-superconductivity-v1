# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

def main():
    mpl.rcParams['text.usetex'] = False
    data_dir = 'data'
    data_path = os.path.join(data_dir, 'processed_tmd_data.csv')
    candidates_path = os.path.join(data_dir, 'prioritized_candidates.csv')
    if not os.path.exists(data_path):
        print('Error: Processed dataset not found at ' + data_path)
        return
    df = pd.read_csv(data_path)
    if os.path.exists(candidates_path):
        top_candidates = pd.read_csv(candidates_path).head(10)
    else:
        print('Warning: Prioritized candidates not found. Extracting from main dataset.')
        top_candidates = df[df['band_gap'] == 0.0].sort_values('studentized_residual', ascending=False).head(10)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    ax1 = axes[0]
    ax1.scatter(df['predicted_dos_at_fermi'], df['dos_at_fermi'], alpha=0.6, edgecolors='w', linewidth=0.5)
    min_val = min(df['predicted_dos_at_fermi'].min(), df['dos_at_fermi'].min())
    max_val = max(df['predicted_dos_at_fermi'].max(), df['dos_at_fermi'].max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'k--', zorder=0, label='y = x')
    ax1.scatter(top_candidates['predicted_dos_at_fermi'], top_candidates['dos_at_fermi'], color='red', edgecolor='black', zorder=5, label='Top 10 Candidates')
    for _, row in top_candidates.iterrows():
        ax1.annotate(row['formula'], (row['predicted_dos_at_fermi'], row['dos_at_fermi']), textcoords='offset points', xytext=(5, 5), ha='left', fontsize=9, color='darkred')
    ax1.set_xlabel('Predicted DOS at Fermi Level (Scaled)')
    ax1.set_ylabel('Actual DOS at Fermi Level (Scaled)')
    ax1.set_title('Parity Plot: Predicted vs Actual DOS')
    ax1.legend()
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax2 = axes[1]
    sc = ax2.scatter(df['energy_above_hull'], df['dos_at_fermi'], c=df['studentized_residual'], cmap='viridis', alpha=0.8, edgecolor='w', linewidth=0.5)
    cbar = fig.colorbar(sc, ax=ax2)
    cbar.set_label('Studentized Residual')
    ax2.set_xlabel('Energy Above Hull (eV/atom)')
    ax2.set_ylabel('DOS at Fermi Level (Scaled)')
    ax2.set_title('Stability vs DOS Colored by Residual')
    ax2.grid(True, linestyle=':', alpha=0.7)
    fig.tight_layout()
    timestamp = int(time.time())
    plot_filename = 'results_visualization_1_' + str(timestamp) + '.png'
    plot_filepath = os.path.join(data_dir, plot_filename)
    fig.savefig(plot_filepath, dpi=300)
    print('--- Top 10 Candidates Highlighted in Parity Plot ---')
    for _, row in top_candidates.iterrows():
        print('Formula: ' + str(row['formula']) + ', Actual DOS (Scaled): ' + str(round(row['dos_at_fermi'], 4)) + ', Predicted DOS (Scaled): ' + str(round(row['predicted_dos_at_fermi'], 4)) + ', Studentized Residual: ' + str(round(row['studentized_residual'], 4)))
    print('----------------------------------------------------\n')
    print('--- Scatter Plot Summary ---')
    print('X-axis: Energy Above Hull (raw) range: [' + str(round(df['energy_above_hull'].min(), 4)) + ', ' + str(round(df['energy_above_hull'].max(), 4)) + '] eV/atom')
    print('Y-axis: DOS at Fermi Level (Scaled) range: [' + str(round(df['dos_at_fermi'].min(), 4)) + ', ' + str(round(df['dos_at_fermi'].max(), 4)) + ']')
    print('Color: Studentized Residual range: [' + str(round(df['studentized_residual'].min(), 4)) + ', ' + str(round(df['studentized_residual'].max(), 4)) + ']')
    print('----------------------------\n')
    print('Plot saved to ' + plot_filepath)

if __name__ == '__main__':
    main()