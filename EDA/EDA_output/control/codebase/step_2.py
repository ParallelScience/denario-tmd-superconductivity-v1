# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import os

def analyze_data():
    """
    Loads the TMD dataset and performs statistical characterization and diagnostic analysis.
    
    Units of quantities:
    - energy_above_hull: eV/atom
    - band_gap: eV
    - dos_at_fermi: states/eV (per unit cell or per atom)
    - volume: Å³
    - a, b, c: Å
    - alpha, beta, gamma: degrees
    """
    data_path = os.path.join('data', 'tmd_data.csv')
    df = pd.read_csv(data_path)
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_rows', None)
    
    print('--- Descriptive Statistics ---')
    numeric_df = df.select_dtypes(include=[np.number])
    desc_stats = numeric_df.describe()
    print(desc_stats)
    
    print('\n--- Correlation Matrix ---')
    corr_matrix = numeric_df.corr()
    print(corr_matrix)
    
    print('\n--- Counts of Specific Phases ---')
    stable_count = (df['energy_above_hull'] == 0.0).sum()
    metallic_count = (df['band_gap'] == 0.0).sum()
    print('Thermodynamically stable materials (energy_above_hull == 0): ' + str(stable_count))
    print('Metallic phases (band_gap == 0): ' + str(metallic_count))
    
    print('\n--- Skewness and Kurtosis ---')
    skew_dos = df['dos_at_fermi'].skew()
    kurt_dos = df['dos_at_fermi'].kurtosis()
    skew_energy = df['energy_above_hull'].skew()
    kurt_energy = df['energy_above_hull'].kurtosis()
    
    print('dos_at_fermi - Skewness: ' + str(skew_dos) + ', Kurtosis: ' + str(kurt_dos))
    print('energy_above_hull - Skewness: ' + str(skew_energy) + ', Kurtosis: ' + str(kurt_energy))
    
    print('\n--- Recommendations on Log-Scaling ---')
    if abs(skew_dos) > 1.0:
        print('Recommendation for dos_at_fermi: High skewness detected. Consider log-scaling (e.g., log1p) for downstream modeling.')
    else:
        print('Recommendation for dos_at_fermi: Skewness is moderate. Log-scaling may not be strictly necessary.')
        
    if abs(skew_energy) > 1.0:
        print('Recommendation for energy_above_hull: High skewness detected. Consider log-scaling (e.g., log1p) for downstream modeling.')
    else:
        print('Recommendation for energy_above_hull: Skewness is moderate. Log-scaling may not be strictly necessary.')

if __name__ == '__main__':
    analyze_data()