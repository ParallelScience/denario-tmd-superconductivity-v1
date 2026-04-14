# filename: codebase/step_3.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import time
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

def compute_and_plot_shap():
    plt.rcParams['text.usetex'] = False
    data_dir = 'data'
    X_path = os.path.join(data_dir, 'X_features.csv')
    model_path = os.path.join(data_dir, 'gb_model.joblib')
    X = pd.read_csv(X_path)
    model = joblib.load(model_path)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    feature_importance = pd.DataFrame({'feature': X.columns, 'mean_abs_shap': mean_abs_shap}).sort_values(by='mean_abs_shap', ascending=False)
    top_n = 10
    print('Top ' + str(top_n) + ' most important features by mean absolute SHAP value:')
    for index, row in feature_importance.head(top_n).iterrows():
        print(row['feature'] + ': ' + str(row['mean_abs_shap']))
    plt.figure()
    shap.summary_plot(shap_values, X, show=False)
    timestamp = int(time.time())
    plot_filename = 'shap_summary_' + str(timestamp) + '.png'
    plot_filepath = os.path.join(data_dir, plot_filename)
    plt.savefig(plot_filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print('SHAP summary plot saved to ' + plot_filepath)

if __name__ == '__main__':
    compute_and_plot_shap()