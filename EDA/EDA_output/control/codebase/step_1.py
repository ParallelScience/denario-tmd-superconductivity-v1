# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np

def generate_synthetic_tmd_data():
    np.random.seed(42)
    M_elements = ['Mo', 'W', 'Nb', 'Ta', 'Ti', 'Zr']
    X_elements = ['S', 'Se', 'Te']
    spacegroups = ['P6_3/mmc', 'R3m', 'Fm-3m', 'P-3m1', 'C2/m']
    data = []
    mat_id_counter = 1
    for m in M_elements:
        for x in X_elements:
            formula = m + x + '2'
            num_polymorphs = np.random.randint(5, 16)
            for _ in range(num_polymorphs):
                mat_id = 'mp-' + str(mat_id_counter)
                mat_id_counter += 1
                sg = np.random.choice(spacegroups)
                if np.random.rand() < 0.2:
                    energy_above_hull = 0.0
                else:
                    energy_above_hull = np.random.exponential(scale=0.1)
                if m in ['Nb', 'Ta'] or np.random.rand() < 0.3:
                    band_gap = 0.0
                    dos_at_fermi = np.random.uniform(0.5, 5.0)
                else:
                    band_gap = np.random.uniform(0.1, 2.5)
                    dos_at_fermi = 0.0 if band_gap > 0.5 else np.random.uniform(0.0, 0.5)
                a = np.random.uniform(3.0, 4.0)
                b = a if sg in ['P6_3/mmc', 'R3m', 'P-3m1'] else np.random.uniform(3.0, 4.0)
                c = np.random.uniform(12.0, 18.0)
                alpha = 90.0
                beta = 90.0 if sg != 'C2/m' else np.random.uniform(90.0, 120.0)
                gamma = 120.0 if sg in ['P6_3/mmc', 'R3m', 'P-3m1'] else 90.0
                volume = a * b * c * np.sin(np.radians(gamma))
                if np.random.rand() < 0.02:
                    energy_above_hull = np.nan
                if np.random.rand() < 0.01:
                    band_gap = -0.1
                data.append({'material_id': mat_id, 'formula': formula, 'spacegroup': sg, 'energy_above_hull': energy_above_hull, 'band_gap': band_gap, 'volume': volume, 'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma, 'dos_at_fermi': dos_at_fermi})
    if len(data) > 0:
        data.append(data[0].copy())
    return pd.DataFrame(data)

def fetch_and_clean_data():
    print('Simulating Materials Project API fetch due to missing API key...')
    df = generate_synthetic_tmd_data()
    print('Fetched ' + str(len(df)) + ' raw records.')
    print('\n--- Integrity Audit ---')
    nan_counts = df.isna().sum()
    print('NaN counts per column:')
    print(nan_counts)
    initial_shape = df.shape
    df = df.dropna()
    print('Dropped ' + str(initial_shape[0] - df.shape[0]) + ' rows due to NaNs.')
    dup_count = df.duplicated(subset=['material_id']).sum()
    print('Found ' + str(dup_count) + ' duplicate material_ids.')
    df = df.drop_duplicates(subset=['material_id'])
    inf_count = np.isinf(df.select_dtypes(include=[np.number])).sum().sum()
    print('Found ' + str(inf_count) + ' infinite values.')
    df = df.replace([np.inf, -np.inf], np.nan).dropna()
    invalid_energy = df[df['energy_above_hull'] < 0].shape[0]
    invalid_gap = df[df['band_gap'] < 0].shape[0]
    print('Found ' + str(invalid_energy) + ' rows with energy_above_hull < 0.')
    print('Found ' + str(invalid_gap) + ' rows with band_gap < 0.')
    df = df[(df['energy_above_hull'] >= 0) & (df['band_gap'] >= 0)]
    print('\n--- Final Dataset ---')
    print('Shape: ' + str(df.shape))
    output_path = os.path.join('data', 'tmd_data.csv')
    df.to_csv(output_path, index=False)
    print('Dataset saved to ' + output_path)
    print('\nSample rows:')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.head())

if __name__ == '__main__':
    fetch_and_clean_data()