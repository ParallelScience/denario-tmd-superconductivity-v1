# denario-tmd-superconductivity-v1

**Scientist:** denario-6
**Date:** 2026-04-13

# Data Description: Transition-Metal Dichalcogenides (TMDs) and Superconductivity

## Overview
This project analyzes structural and electronic properties of Transition-Metal Dichalcogenides (TMDs) sourced from the Materials Project. The goal is to identify patterns between crystal symmetry (space groups) and indicators of superconducting potential (such as density of states at the Fermi level and structural stability).

## Data Source
- **API**: Materials Project API (MPRester)
- **Target Materials**: Compounds with the formula MX2, where M = Transition Metal (e.g., Mo, W, Nb, Ta, Ti, Zr) and X = Chalcogen (S, Se, Te).

## File Inventory (to be generated via API)
The pipeline will generate the following files in the project directory:
- `/home/node/work/projects/materials_project_v1/tmd_data.csv`: A dataset containing:
    - `material_id`: Unique MP ID.
    - `formula`: Chemical formula.
    - `spacegroup`: Crystal space group.
    - `energy_above_hull`: Stability indicator (eV/atom).
    - `band_gap`: Electronic band gap (eV).
    - `dos_at_fermi`: Density of states at the Fermi level.
    - `volume`: Unit cell volume.
    - `lattice_parameters`: a, b, c, alpha, beta, gamma.

## Variable Meanings
- `energy_above_hull`: A value of 0 indicates a thermodynamically stable material.
- `dos_at_fermi`: High DOS at the Fermi level is often a prerequisite for superconductivity according to BCS theory.
- `spacegroup`: Defines the symmetry operations of the crystal, critical for identifying phase transitions.

## Suggested Analyses
1. **Symmetry Mapping**: Compare the distribution of `dos_at_fermi` across different space groups.
2. **Stability vs. Gap**: Analyze the relationship between thermodynamic stability and band gap to identify potential metallic phases.
3. **Compositional Trends**: Check if specific transition metals consistently produce high DOS in specific symmetries.
