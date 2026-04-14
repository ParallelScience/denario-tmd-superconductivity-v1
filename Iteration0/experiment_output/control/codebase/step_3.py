# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd

def main():
    """
    Loads the processed TMD dataset, filters for metallic candidates (band_gap == 0.0),
    identifies outliers with Studentized residuals > 2.0, prints summary statistics
    and the full prioritized candidate table, and saves the results.
    """
    data_path = os.path.join('data', 'processed_tmd_data.csv')
    if not os.path.exists(data_path):
        print('Error: Processed dataset not found at ' + data_path)
        return
    
    print('Loading dataset from ' + data_path + '...')
    df = pd.read_csv(data_path)
    
    # Filter for metallic candidates
    metallic_df = df[df['band_gap'] == 0.0]
    print('Number of metallic candidates (band_gap == 0.0): ' + str(len(metallic_df)))
    
    print('\n--- Summary Statistics of Residuals for Metallic Candidates ---')
    if len(metallic_df) > 0:
        print('Count: ' + str(len(metallic_df)))
        print('Mean:  ' + str(metallic_df['studentized_residual'].mean()))
        print('Max:   ' + str(metallic_df['studentized_residual'].max()))
        print('Min:   ' + str(metallic_df['studentized_residual'].min()))
    else:
        print('No metallic candidates found.')
    print('---------------------------------------------------------------\n')
    
    # Identify outliers (Studentized residual > 2.0)
    outliers_df = metallic_df[metallic_df['studentized_residual'] > 2.0].copy()
    
    # Sort by studentized_residual descending to prioritize the highest overperformers
    outliers_df = outliers_df.sort_values(by='studentized_residual', ascending=False)
    
    print('--- Summary Statistics of Residuals for Prioritized Candidates (Outliers > 2.0) ---')
    if len(outliers_df) > 0:
        print('Count: ' + str(len(outliers_df)))
        print('Mean:  ' + str(outliers_df['studentized_residual'].mean()))
        print('Max:   ' + str(outliers_df['studentized_residual'].max()))
        print('Min:   ' + str(outliers_df['studentized_residual'].min()))
    else:
        print('No outliers found with studentized_residual > 2.0 among metallic candidates.')
    print('-----------------------------------------------------------------------------------\n')
    
    print('--- Full Prioritized Candidate Table ---')
    # Ensure pandas prints all columns and rows without truncation
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    
    if len(outliers_df) > 0:
        print(outliers_df.to_string(index=False))
    else:
        print('Empty table.')
    print('----------------------------------------\n')
    
    # Save the final prioritized list of candidates
    output_path = os.path.join('data', 'prioritized_candidates.csv')
    outliers_df.to_csv(output_path, index=False)
    print('Prioritized candidates saved to ' + output_path)

if __name__ == '__main__':
    main()