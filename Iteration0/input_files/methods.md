1. **Data Preprocessing and Feature Engineering**: 
   - Apply a `log1p` transformation to the `energy_above_hull` feature to mitigate right-skewness.
   - Perform one-hot encoding on the `spacegroup` categorical variable.
   - Create a binary feature `is_group_v` (1 if the transition metal is Nb or Ta, 0 otherwise) to explicitly account for known compositional drivers of high DOS.
   - Apply Z-score normalization (StandardScaler) to all continuous features (`volume`, transformed `energy_above_hull`, and `dos_at_fermi`).

2. **Multicollinearity and Model Selection**:
   - Calculate the Variance Inflation Factor (VIF) for all predictors (`volume`, `spacegroup` dummies, `energy_above_hull`, `is_group_v`) to ensure no severe multicollinearity exists.
   - Select a regularized regression model (Ridge or Lasso) to stabilize coefficients, ensuring the model remains robust even if minor correlations persist between structural features.

3. **Cross-Validated Residual Calculation**:
   - Implement a 5-fold cross-validation strategy to fit the regression model.
   - For each fold, calculate the residuals (actual `dos_at_fermi` minus predicted `dos_at_fermi`) for the held-out test set. This ensures that the "expected" DOS is derived from a model that has not seen the specific data point, preventing overfitting.

4. **Residual Normalization and Statistical Outlier Detection**:
   - Compute the Studentized residuals for all observations to account for potential heteroscedasticity.
   - Identify "statistically significant" electronic outliers by selecting materials where the Studentized residual exceeds a threshold (e.g., > 2.0 standard deviations).

5. **Filtering for Metallic Candidates**:
   - Filter the dataset to retain only materials where `band_gap == 0.0` eV.
   - Cross-reference these metallic candidates with the calculated Studentized residuals to isolate materials that are both metallic and exhibit statistically significant "Electronic Overperformance."

6. **Ranking and Prioritization**:
   - Rank the filtered metallic candidates in descending order based on the magnitude of their Studentized residuals.
   - Generate a final prioritized list of candidates that demonstrate the highest potential for enhanced electron-phonon coupling, effectively decoupling compositional excellence from structural geometry.

7. **Visualization of Results**:
   - Generate a parity plot comparing predicted vs. actual `dos_at_fermi`, explicitly highlighting the top 10 ranked candidates with distinct labels or colors.
   - Create a scatter plot of `energy_above_hull` vs. `dos_at_fermi`, color-coded by the magnitude of the Studentized residuals, to visualize the decoupling of structural stability from electronic performance.

8. **Final Synthesis**:
   - Compile the final prioritized list including `material_id`, `formula`, `spacegroup`, and Studentized residual value.
   - Document the findings by summarizing how the identified outliers deviate from the baseline trends established by the structural and compositional features, providing a physically grounded rationale for experimental validation.