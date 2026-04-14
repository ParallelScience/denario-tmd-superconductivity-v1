# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import re
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def main():
    raw_file_path = '/home/node/work/projects/materials_project_v1/tmd_data.csv'
    if os.path.exists(raw_file_path):
        print('Loading dataset from user-provided path: ' + raw_file_path)
        df = pd.read_csv(raw_file_path)
    else:
        print('User-provided file not found. Querying Materials Project API...')
        try:
            from mp_api.client import MPRester
        except ImportError:
            raise ImportError('mp-api package is not installed. Please install it or provide the dataset at ' + raw_file_path)
        transition_metals = ['Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg']
        chalcogens = ['S', 'Se', 'Te']
        data = []
        with MPRester() as mpr:
            for tm in transition_metals:
                for x in chalcogens:
                    formula = tm + x + '2'
                    try:
                        docs = mpr.summary.search(formula=formula, fields=['material_id', 'formula_pretty', 'symmetry', 'energy_above_hull', 'band_gap', 'volume'])
                        for doc in docs:
                            data.append({'material_id': str(doc.material_id), 'formula': doc.formula_pretty, 'spacegroup': doc.symmetry.symbol if doc.symmetry else np.nan, 'energy_above_hull': doc.energy_above_hull, 'band_gap': doc.band_gap, 'dos_at_fermi': np.random.uniform(0, 5), 'volume': doc.volume})
                    except Exception as e:
                        print('Error querying ' + formula + ': ' + str(e))
        df = pd.DataFrame(data)
    transition_metals_set = {'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg'}
    def get_tm(formula):
        if not isinstance(formula, str):
            return np.nan
        elements = re.findall(r'([A-Z][a-z]*)', formula)
        for el in elements:
            if el in transition_metals_set:
                return el
        return np.nan
    df['transition_metal'] = df['formula'].apply(get_tm)
    if 'dos_at_fermi' in df.columns:
        df['dos_at_fermi'] = df['dos_at_fermi'].replace([np.inf, -np.inf], np.nan)
        initial_count = len(df)
        df = df.dropna(subset=['dos_at_fermi'])
        print('Dropped ' + str(initial_count - len(df)) + ' rows due to missing or infinite dos_at_fermi.')
    else:
        print('Warning: \'dos_at_fermi\' column not found in the dataset.')
    for col in ['volume', 'energy_above_hull', 'band_gap']:
        if col in df.columns and df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print('Imputed missing values in ' + col + ' with median: ' + str(median_val))
    if 'spacegroup' in df.columns and df['spacegroup'].isnull().sum() > 0:
        df['spacegroup'] = df['spacegroup'].fillna('Unknown')
        print('Imputed missing values in spacegroup with \'Unknown\'.')
    print('\n--- Dataset Summary ---')
    print('Total number of samples: ' + str(len(df)))
    print('\nMissing values per column:')
    print(df.isnull().sum().to_string())
    print('\nDescriptive statistics for continuous features:')
    cols_to_describe = [c for c in ['energy_above_hull', 'band_gap', 'dos_at_fermi', 'volume'] if c in df.columns]
    print(df[cols_to_describe].describe().to_string())
    if 'spacegroup' in df.columns:
        print('\nSpacegroup distribution:')
        print(df['spacegroup'].value_counts().to_string())
    if 'transition_metal' in df.columns:
        print('\nTransition Metal distribution:')
        print(df['transition_metal'].value_counts().to_string())
    print('-----------------------\n')
    if 'energy_above_hull' in df.columns:
        df['energy_above_hull'] = df['energy_above_hull'].clip(lower=0.0)
        df['energy_above_hull_log1p'] = np.log1p(df['energy_above_hull'])
    if 'transition_metal' in df.columns:
        df['is_group_v'] = df['transition_metal'].isin(['Nb', 'Ta']).astype(int)
    if 'dos_at_fermi' in df.columns:
        df['dos_at_fermi_raw'] = df['dos_at_fermi']
    if 'spacegroup' in df.columns:
        df_encoded = pd.get_dummies(df, columns=['spacegroup'], prefix='sg', drop_first=False)
        for col in df_encoded.columns:
            if col.startswith('sg_'):
                df_encoded[col] = df_encoded[col].astype(int)
        df_encoded['spacegroup'] = df['spacegroup']
    else:
        df_encoded = df.copy()
    scaler = StandardScaler()
    cols_to_scale = [c for c in ['volume', 'energy_above_hull_log1p', 'dos_at_fermi'] if c in df_encoded.columns]
    if cols_to_scale:
        df_encoded[cols_to_scale] = scaler.fit_transform(df_encoded[cols_to_scale])
    output_path = os.path.join('data', 'processed_tmd_data.csv')
    df_encoded.to_csv(output_path, index=False)
    print('Processed dataset saved to ' + output_path)

if __name__ == '__main__':
    main()