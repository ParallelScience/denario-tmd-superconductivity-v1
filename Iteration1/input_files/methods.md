1. **Data Refinement and Feature Engineering**
   - Apply `log1p` transformation to `energy_above_hull` and one-hot encode `spacegroup`.
   - Engineer structural features: calculate the `c/a` lattice ratio and unit cell volume per atom to capture structural density and anisotropy.
   - Incorporate compositional descriptors: add atomic number, valence electron count, and electronegativity for both the metal and chalcogen atoms to provide the model with physical context.
   - Apply Z-score normalization to all continuous predictors to ensure consistency across features.

2. **Non-Linear Modeling with Gradient Boosting**
   - Implement a Gradient Boosting Regressor to model `dos_at_fermi` as a function of structural and compositional features.
   - Set a fixed `random_state` for both the 5-fold cross-validation splits and the regressor to ensure reproducibility.
   - Generate cross-validated predictions and calculate the residuals (actual `dos_at_fermi` minus predicted `dos_at_fermi`) for the entire dataset.

3. **Interpretability via SHAP Analysis**
   - Apply SHAP (SHapley Additive exPlanations) to the model to quantify the contribution of each feature (structural, compositional, and symmetry-based) to the predicted `dos_at_fermi`.
   - Analyze whether the model's predictions are driven by expected structural trends or if the residuals capture unexplained variance linked to specific chemical properties like valence electron count.

4. **Synthesizability and Stability Filtering**
   - Apply a dual-filter: prioritize materials with `theoretical == False` (existing in ICSD) and `energy_above_hull < 0.1 eV/atom`.
   - Treat materials with `theoretical == True` as secondary candidates, requiring stricter scrutiny of their stability metrics.
   - Exclude high-residual candidates that are exclusively driven by high `energy_above_hull` values to avoid metastable artifacts.

5. **Validation of Metallic Ground States**
   - Utilize the `is_metal` property provided by the Materials Project API as the primary filter for metallic behavior.
   - For candidates where `is_metal` is ambiguous, apply a conservative threshold of `band_gap < 0.01 eV` to account for DFT numerical precision, labeling these as "Candidate Metallic Phases."

6. **Sensitivity Analysis of Residuals**
   - Perform correlation analysis between the residuals and structural motifs not explicitly in the model, such as M-X bond lengths or octahedral distortion parameters.
   - Re-classify candidates as "structurally-driven" if high residuals correlate strongly with these motifs, ensuring the final list focuses on "compositionally-driven" overperformers.

7. **Ranking and Prioritization**
   - Rank the filtered, metallic, and synthesizable candidates by the magnitude of their positive residuals.
   - Compile a final prioritized list of "Electronic Overperformers" that demonstrate high DOS despite structural and thermodynamic constraints.

8. **Visualization and Reporting**
   - Generate a SHAP summary plot to visualize global feature importance and a scatter plot of `energy_above_hull` vs. `dos_at_fermi`, color-coded by residual magnitude.
   - Document the top candidates and provide a physical rationale for their selection based on the decoupling of structural vs. compositional contributions.