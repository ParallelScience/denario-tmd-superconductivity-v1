# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np

def fetch_and_clean_data():
    try:
        from mp_api.client import MPRester
    except ImportError:
        print('mp_api is not installed. Please install it using pip install mp-api.')
        raise
    if 'MP_API_KEY' not in os.environ:
        print('WARNING: MP_API_KEY environment variable is not set. The API request will likely fail unless configured elsewhere.')
    M_elements = ['Mo', 'W', 'Nb', 'Ta', 'Ti', 'Zr']
    X_elements = ['S', 'Se', 'Te']
    formulas = [m + x + '2' for m in M_elements for x in X_elements]
    data = []
    print('Connecting to Materials Project API...')
    try:
        with MPRester() as mpr:
            docs = []
            for f in formulas:
                print('Fetching summary docs for ' + f + '...')
                try:
                    res = mpr.summary.search(formula=f)
                    docs.extend(res)
                except Exception as e:
                    print('Error fetching ' + f + ': ' + str(e))
            print('Fetched ' + str(len(docs)) + ' summary docs in total.')
            mat_ids = [str(doc.material_id) for doc in docs]
            dos_dict = {}
            print('Fetching DOS docs...')
            try:
                chunk_size = 50
                for i in range(0, len(mat_ids), chunk_size):
                    chunk_ids = mat_ids[i:i+chunk_size]
                    try:
                        if hasattr(mpr, 'dos'):
                            dos_docs = mpr.dos.search(material_ids=chunk_ids)
                        else:
                            dos_docs = mpr.electronic_structure.dos.search(material_ids=chunk_ids)
                        for d in dos_docs:
                            try:
                                dos_obj = d.dos
                                efermi = dos_obj.efermi
                                energies = dos_obj.energies
                                idx = np.argmin(np.abs(energies - efermi))
                                dos_at_fermi = sum(densities[idx] for densities in dos_obj.densities.values())
                                dos_dict[str(d.material_id)] = dos_at_fermi
                            except Exception:
                                pass
                    except Exception as e:
                        print('Error fetching DOS chunk ' + str(i) + ': ' + str(e))
                print('Fetched DOS for ' + str(len(dos_dict)) + ' materials.')
            except Exception as e:
                print('Could not fetch DOS docs: ' + str(e))
            for doc in docs:
                mat_id = str(doc.material_id)
                formula = doc.formula_pretty
                spacegroup = doc.symmetry.symbol if doc.symmetry else np.nan
                energy_above_hull = doc.energy_above_hull
                band_gap = doc.band_gap
                volume = doc.volume
                if doc.structure:
                    lattice = doc.structure.lattice
                    a, b, c = lattice.a, lattice.b, lattice.c
                    alpha, beta, gamma = lattice.alpha, lattice.beta, lattice.gamma
                else:
                    a = b = c = alpha = beta = gamma = np.nan
                dos_at_fermi = dos_dict.get(mat_id, np.nan)
                data.append({'material_id': mat_id, 'formula': formula, 'spacegroup': spacegroup, 'energy_above_hull': energy_above_hull, 'band_gap': band_gap, 'volume': volume, 'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma, 'dos_at_fermi': dos_at_fermi})
    except Exception as e:
        print('Error during MP API fetch: ' + str(e))
        raise e
    df = pd.DataFrame(data)
    if df.empty:
        print('Dataset is empty after fetching. Please check the API responses.')
        output_path = os.path.join('data', 'tmd_data.csv')
        df.to_csv(output_path, index=False)
        return
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