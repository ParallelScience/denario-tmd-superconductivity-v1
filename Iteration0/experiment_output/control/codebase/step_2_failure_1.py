# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import pandas as pd
import numpy as np
import warnings
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant
from sklearn.linear_model import RidgeCV, Ridge
from sklearn.model_selection import cross_val_score, cross_val_predict, KFold

def main():
    warnings.filterwarnings('ignore')
    data_path = os.path.join('data', 'processed_tmd_data.csv')
    if not os.path.exists(data_path):
        print('Error: Processed dataset not found at ' + data_path)
        return
    print('Loading dataset from ' + data_path + '...')
    df = pd.read_csv(data_path)
    base_predictors = ['volume', 'energy_above_hull_log1p', 'is_group_v']
    sg_predictors = [c for c in df.columns if c.startswith('sg_')]
    predictors = [p for p in base_predictors + sg_predictors if p in df.columns]
    X = df[predictors].copy()
    y = df['dos_at_fermi']
    def get_vifs(X_df):
        X_vif = add_constant(X_df)
        vifs = []
        for i in range(X_vif.shape[1]):
            try:
                vif = variance_inflation_factor(X_vif.values, i)
            except Exception:
                vif = np.inf
            vifs.append(vif)
        vif_df = pd.DataFrame({'feature': X_vif.columns, 'VIF': vifs})
        vif_df['VIF'] = vif_df['VIF'].fillna(np.inf)
        return vif_df[vif_df['feature'] != 'const'].sort_values(by='VIF', ascending=False)
    initial_vif_df = get_vifs(X)
    print('\n--- Top 10 Highest-VIF Predictors (Initial) ---')
    print(initial_vif_df.head(10).to_string(index=False))
    print('-----------------------------------------------\n')
    while True:
        if X.shape[1] == 0:
            print('Warning: All predictors dropped due to high VIF.')
            break
        vif_df = get_vifs(X)
        max_vif = vif_df.iloc[0]['VIF']
        max_feature = vif_df.iloc[0]['feature']
        if max_vif > 10:
            print('Dropping feature ' + max_feature + ' with VIF = ' + str(max_vif))
            X = X.drop(columns=[max_feature])
        else:
            break
    print('\nPredictors retained after VIF filtering:')
    print(X.columns.tolist())
    print('\n')
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    alphas = np.logspace(-3, 3, 100)
    print('Fitting 5-fold cross-validated Ridge regression model...')
    ridge_cv = RidgeCV(alphas=alphas, cv=kf)
    ridge_cv.fit(X, y)
    optimal_alpha = ridge_cv.alpha_
    ridge = Ridge(alpha=optimal_alpha)
    cv_scores = cross_val_score(ridge, X, y, cv=kf, scoring='r2')
    print('--- Ridge Regression Model Performance ---')
    print('Optimal Ridge alpha: ' + str(optimal_alpha))
    print('Cross-validation R-squared scores: ' + str(cv_scores))
    print('Mean CV R-squared: ' + str(np.mean(cv_scores)))
    print('------------------------------------------\n')
    y_pred_cv = cross_val_predict(ridge, X, y, cv=kf)
    residuals = y - y_pred_cv
    X_design = np.hstack([np.ones((X.shape[0], 1)), X.values])
    penalty = np.eye(X_design.shape[1]) * optimal_alpha
    penalty[0, 0] = 0
    inv_mat = np.linalg.inv(X_design.T @ X_design + penalty)
    leverage = np.sum(X_design * (X_design @ inv_mat), axis=1)
    leverage = np.clip(leverage, 0, 0.99)
    sigma = np.std(residuals, ddof=1)
    studentized_residuals = residuals / (sigma * np.sqrt(1 - leverage))
    print('--- Residuals Summary ---')
    print('Mean of Studentized residuals: ' + str(np.mean(studentized_residuals)))
    print('Std of Studentized residuals: ' + str(np.std(studentized_residuals)))
    print('Min of Studentized residuals: ' + str(np.min(studentized_residuals)))
    print('Max of Studentized residuals: ' + str(np.max(studentized_residuals)))
    print('-------------------------\n')
    df['predicted_dos_at_fermi'] = y_pred_cv
    df['residual'] = residuals
    df['studentized_residual'] = studentized_residuals
    df.to_csv(data_path, index=False)
    print('Studentized residuals computed and saved to ' + data_path)

if __name__ == '__main__':
    main()