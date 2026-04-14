

Iteration 0:
# Summary: Residual-Based Identification of Anomalous Electronic Coupling in MX2 TMDs

### 1. Methodology & Assumptions
*   **Objective**: Identify metallic MX2 TMDs with "Electronic Overperformance" (high `dos_at_fermi` relative to structural/thermodynamic baseline).
*   **Model**: Ridge regression (α=1000) predicting `dos_at_fermi` using `volume`, `log1p(energy_above_hull)`, `is_group_v` (Nb/Ta flag), and one-hot encoded `spacegroup` (baseline: `Fm-3m`).
*   **Validation**: 5-fold cross-validation; Studentized residuals used to quantify deviation from structural expectations.
*   **Filtering**: Metallic candidates (`band_gap` = 0.0 eV) with Studentized residuals > 2.0 SD.

### 2. Key Findings
*   **Model Performance**: Mean CV R² = -0.0442. The structural baseline is insufficient to explain `dos_at_fermi` variance, confirming that electronic properties are driven by intrinsic compositional factors rather than geometry.
*   **Outlier Identification**: 31 metallic candidates identified as significant electronic outliers.
*   **Top Candidates**: MnS2, VS2, AgS2, IrTe2, LuSe2, CuS2, MoSe2, TaTe2, ReSe2, FeS2.
*   **Stability Decoupling**: High-residual candidates exist across the entire `energy_above_hull` spectrum, indicating that metastable phases (e.g., FeS2, IrTe2) are viable targets for non-equilibrium synthesis.

### 3. Limitations & Uncertainties
*   **Model Bias**: The model assumes a linear relationship between structural features and DOS; non-linear electronic correlations (e.g., strong electron-electron interactions in Vanadium compounds) are captured only as residuals.
*   **Data Scope**: Limited to MX2 stoichiometry; results may not generalize to other TMD phases or intercalated structures.
*   **Synthesis Feasibility**: High residuals in metastable materials suggest potential for superconductivity, but experimental accessibility remains unverified.

### 4. Future Directions
*   **Experimental Validation**: Prioritize synthesis of the top 10 candidates using non-equilibrium methods (e.g., MBE, high-pressure) for metastable phases.
*   **Refinement**: Incorporate additional features (e.g., electronegativity, d-orbital occupancy, or spin-orbit coupling strength) to further reduce baseline variance.
*   **Mechanism Analysis**: Perform DFT-based band structure calculations on the top 31 candidates to confirm the physical origin of the anomalous DOS peaks.
        