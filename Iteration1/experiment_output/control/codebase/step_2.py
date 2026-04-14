# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_validate, KFold
import joblib

def main():
    data_path = "data/tmd_data.csv"
    df = pd.read_csv(data_path)
    sg_dummies = pd.get_dummies(df['spacegroup'], prefix='sg', dtype=float)
    continuous_features = ['log1p_energy_above_hull', 'c_a_ratio', 'volume_per_atom', 'M_Z', 'M_val', 'M_en', 'X_Z', 'X_val', 'X_en']
    scaler = StandardScaler()
    df_continuous_scaled = pd.DataFrame(scaler.fit_transform(df[continuous_features]), columns=continuous_features, index=df.index)
    X = pd.concat([df_continuous_scaled, sg_dummies], axis=1)
    y = df['dos_at_fermi']
    gbr = GradientBoostingRegressor(random_state=42)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_results = cross_validate(gbr, X, y, cv=kf, scoring=('r2', 'neg_root_mean_squared_error'), return_train_score=False)
    mean_r2 = np.mean(cv_results['test_r2'])
    mean_rmse = -np.mean(cv_results['test_neg_root_mean_squared_error'])
    print("Model Performance Metrics (5-fold CV):")
    print("Mean R-squared: " + str(mean_r2))
    print("Mean RMSE: " + str(mean_rmse))
    gbr.fit(X, y)
    model_path = "data/gb_model.joblib"
    joblib.dump(gbr, model_path)
    print("Fitted model saved to " + model_path)
    X_path = "data/X_features.csv"
    X.to_csv(X_path, index=False)
    print("Feature matrix saved to " + X_path)
    predictions = gbr.predict(X)
    residuals = y - predictions
    df['predicted_dos_at_fermi'] = predictions
    df['residual'] = residuals
    updated_data_path = "data/tmd_data_with_residuals.csv"
    df.to_csv(updated_data_path, index=False)
    print("Updated dataset with residuals saved to " + updated_data_path)

if __name__ == '__main__':
    main()