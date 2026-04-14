# filename: codebase/step_4.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    plt.rcParams['text.usetex'] = False
    data_dir = "data/"
    df = pd.read_csv(os.path.join(data_dir, "tmd_data_with_residuals.csv"))
    filtered_df = df[(df['band_gap'] < 0.01) & (df['energy_above_hull'] < 0.1)].copy()
    primary_df = filtered_df[filtered_df['theoretical'] == False].sort_values(by='residual', ascending=False)
    secondary_df = filtered_df[filtered_df['theoretical'] == True].sort_values(by='residual', ascending=False)
    print("=== Candidate Filtering ===")
    print("Primary candidates (theoretical == False) count: " + str(len(primary_df)))
    if len(primary_df) > 0:
        print("Top 10 Primary Candidates:")
        print(primary_df[['material_id', 'formula', 'spacegroup', 'residual', 'dos_at_fermi', 'energy_above_hull']].head(10).to_string(index=False))
    print("\nSecondary candidates (theoretical == True) count: " + str(len(secondary_df)))
    if len(secondary_df) > 0:
        print("Top 10 Secondary Candidates:")
        print(secondary_df[['material_id', 'formula', 'spacegroup', 'residual', 'dos_at_fermi', 'energy_above_hull']].head(10).to_string(index=False))
    all_pos_res_df = df[df['residual'] > 0].copy()
    if len(all_pos_res_df) > 1:
        corr_c_a = all_pos_res_df['residual'].corr(all_pos_res_df['c_a_ratio'])
        corr_vol = all_pos_res_df['residual'].corr(all_pos_res_df['volume_per_atom'])
    else:
        corr_c_a = 0.0
        corr_vol = 0.0
    print("\n=== Sensitivity Analysis ===")
    print("Pearson correlations between positive residuals and structural motifs (across all positive residuals):")
    print("Correlation with c/a ratio: " + str(corr_c_a))
    print("Correlation with volume per atom: " + str(corr_vol))
    median_c_a = all_pos_res_df['c_a_ratio'].median()
    median_vol = all_pos_res_df['volume_per_atom'].median()
    def classify_candidate(row):
        struct_score = 0
        if abs(corr_c_a) > 0.3:
            if corr_c_a > 0 and row['c_a_ratio'] > median_c_a:
                struct_score += 1
            elif corr_c_a < 0 and row['c_a_ratio'] < median_c_a:
                struct_score += 1
        if abs(corr_vol) > 0.3:
            if corr_vol > 0 and row['volume_per_atom'] > median_vol:
                struct_score += 1
            elif corr_vol < 0 and row['volume_per_atom'] < median_vol:
                struct_score += 1
        return "structurally-driven" if struct_score > 0 else "compositionally-driven"
    filtered_df['classification'] = filtered_df.apply(classify_candidate, axis=1)
    print("\n=== Candidate Classification ===")
    print("Classification counts for filtered candidates:")
    print(filtered_df['classification'].value_counts().to_string())
    plt.figure(figsize=(9, 7))
    vmax = np.abs(df['residual']).max()
    scatter = plt.scatter(df['energy_above_hull'], df['dos_at_fermi'], c=df['residual'], cmap='coolwarm', s=60, edgecolor='k', alpha=0.8, vmin=-vmax, vmax=vmax)
    plt.colorbar(scatter, label='Residual Magnitude (states/eV)')
    plt.xlabel('Energy Above Hull (eV/atom)')
    plt.ylabel('DOS at Fermi Level (states/eV)')
    plt.title('Energy Above Hull vs DOS at Fermi Level\nColor-coded by Residual Magnitude')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    timestamp = int(time.time())
    plot_filename = "scatter_eah_vs_dos_" + str(timestamp) + ".png"
    plot_filepath = os.path.join(data_dir, plot_filename)
    plt.savefig(plot_filepath, dpi=300)
    plt.close()
    print("\nScatter plot saved to " + plot_filepath)
    final_list = filtered_df.sort_values(by='residual', ascending=False)
    final_filepath = os.path.join(data_dir, "prioritized_candidates.csv")
    final_list.to_csv(final_filepath, index=False)
    print("Final prioritized list of candidates saved to " + final_filepath)

if __name__ == '__main__':
    main()