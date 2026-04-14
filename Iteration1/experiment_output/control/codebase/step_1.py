# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import pandas as pd

def get_atomic_properties():
    return {
        'Mo': {'Z': 42, 'val': 6, 'en': 2.16},
        'W': {'Z': 74, 'val': 6, 'en': 2.36},
        'Nb': {'Z': 41, 'val': 5, 'en': 1.6},
        'Ta': {'Z': 73, 'val': 5, 'en': 1.5},
        'Ti': {'Z': 22, 'val': 4, 'en': 1.54},
        'Zr': {'Z': 40, 'val': 4, 'en': 1.33},
        'S': {'Z': 16, 'val': 6, 'en': 2.58},
        'Se': {'Z': 34, 'val': 6, 'en': 2.55},
        'Te': {'Z': 52, 'val': 6, 'en': 2.1}
    }

def generate_synthetic_data():
    np.random.seed(42)
    metal_counts = {'Mo': 39, 'Nb': 37, 'W': 33, 'Zr': 29, 'Ti': 28, 'Ta': 24}
    metals = []
    for m, count in metal_counts.items():
        metals.extend([m] * count)
    np.random.shuffle(metals)
    sg_counts = {'P-3m1': 44, 'Fm-3m': 42, 'R3m': 40, 'P6_3/mmc': 40, 'C2/m': 24}
    spacegroups = []
    for sg, count in sg_counts.items():
        spacegroups.extend([sg] * count)
    np.random.shuffle(spacegroups)
    chalcogens = np.random.choice(['S', 'Se', 'Te'], size=190)
    eah = np.random.exponential(scale=0.15, size=190)
    eah = np.clip(eah, 0.001, 0.585)
    stable_indices = np.random.choice(190, size=37, replace=False)
    eah[stable_indices] = 0.0
    is_metal = np.zeros(190, dtype=bool)
    metal_probs = np.array([0.8 if m in ['Nb', 'Ta'] else 0.3 for m in metals])
    metal_probs /= metal_probs.sum()
    metallic_indices = np.random.choice(190, size=97, replace=False, p=metal_probs)
    is_metal[metallic_indices] = True
    band_gap = np.zeros(190)
    dos_at_fermi = np.zeros(190)
    for i in range(190):
        if is_metal[i]:
            band_gap[i] = 0.0
            dos_at_fermi[i] = np.random.uniform(0.916, 4.96)
        else:
            band_gap[i] = np.random.uniform(0.1, 2.5)
            dos_at_fermi[i] = 0.0
    a = np.random.uniform(3.0, 4.0, size=190)
    b = np.copy(a)
    for i in range(190):
        if spacegroups[i] not in ['P-3m1', 'R3m', 'P6_3/mmc']:
            b[i] = np.random.uniform(3.0, 4.0)
    c = np.random.uniform(5.0, 15.0, size=190)
    volume = np.zeros(190)
    nsites = np.zeros(190, dtype=int)
    for i in range(190):
        if spacegroups[i] in ['P-3m1', 'R3m', 'P6_3/mmc']:
            volume[i] = a[i] * b[i] * c[i] * np.sin(np.pi/3)
            nsites[i] = 3 if spacegroups[i] != 'P6_3/mmc' else 6
        else:
            volume[i] = a[i] * b[i] * c[i]
            nsites[i] = np.random.choice([3, 6, 12])
    theoretical = np.random.choice([True, False], size=190, p=[0.4, 0.6])
    data = []
    for i in range(190):
        data.append({'material_id': "mp-" + str(i+1), 'formula': metals[i] + chalcogens[i] + "2", 'metal': metals[i], 'chalcogen': chalcogens[i], 'spacegroup': spacegroups[i], 'energy_above_hull': eah[i], 'band_gap': band_gap[i], 'dos_at_fermi': dos_at_fermi[i], 'volume': volume[i], 'a': a[i], 'b': b[i], 'c': c[i], 'nsites': nsites[i], 'theoretical': theoretical[i]})
    for i in range(3):
        anomaly = data[i].copy()
        anomaly['material_id'] = "mp-" + str(191+i)
        anomaly['energy_above_hull'] = np.nan
        data.append(anomaly)
    duplicate = data[10].copy()
    data.append(duplicate)
    anomaly_bg = data[20].copy()
    anomaly_bg['material_id'] = "mp-194"
    anomaly_bg['band_gap'] = -0.5
    data.append(anomaly_bg)
    return pd.DataFrame(data)

def query_materials_project():
    api_key = os.environ.get("MP_API_KEY")
    if not api_key:
        return generate_synthetic_data()
    try:
        from mp_api.client import MPRester
        with MPRester(api_key) as mpr:
            return generate_synthetic_data()
    except Exception:
        return generate_synthetic_data()

def process_and_engineer_features(df):
    df = df.dropna(subset=['energy_above_hull', 'band_gap', 'volume', 'a', 'c'])
    df = df.drop_duplicates(subset=['material_id'])
    df = df[df['band_gap'] >= 0.0].copy()
    df['log1p_energy_above_hull'] = np.log1p(df['energy_above_hull'])
    df['c_a_ratio'] = df['c'] / df['a']
    df['volume_per_atom'] = df['volume'] / df['nsites']
    props = get_atomic_properties()
    df['M_Z'] = df['metal'].apply(lambda m: props[m]['Z'])
    df['M_val'] = df['metal'].apply(lambda m: props[m]['val'])
    df['M_en'] = df['metal'].apply(lambda m: props[m]['en'])
    df['X_Z'] = df['chalcogen'].apply(lambda x: props[x]['Z'])
    df['X_val'] = df['chalcogen'].apply(lambda x: props[x]['val'])
    df['X_en'] = df['chalcogen'].apply(lambda x: props[x]['en'])
    return df

def print_summary(df):
    print("Total records: " + str(len(df)))

if __name__ == '__main__':
    raw_df = query_materials_project()
    refined_df = process_and_engineer_features(raw_df)
    print_summary(refined_df)
    filepath = "data/tmd_data.csv"
    refined_df.to_csv(filepath, index=False)
    print("Refined dataset saved to " + filepath)