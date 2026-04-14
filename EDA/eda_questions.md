# Data Clarification Report

Upon reviewing the initial dataset and the engineering outputs for the Transition-Metal Dichalcogenides (TMDs) project, several ambiguities regarding the data definitions and query scope have been identified. To ensure absolute scientific certainty in our downstream modeling and physical interpretations, the following points require clarification:

1. **Units of Density of States at the Fermi Level (`dos_at_fermi`)**:
   The physical units for the `dos_at_fermi` variable are currently unspecified in the source documentation. Are these values reported in states/eV per unit cell, or states/eV per atom? This distinction is critical for accurately comparing the superconducting potential across materials with varying unit cell sizes and atomic counts.

2. **API Query Scope (Polymorphs vs. Ground-State)**:
   Does the dataset retrieved from the Materials Project API include all available polymorphs for each MX2 compound, or is it restricted strictly to the thermodynamically stable ground-state configurations? The presence of materials with `energy_above_hull > 0` suggests that metastable polymorphs are included, but the exact query parameters and inclusion criteria must be explicitly defined to properly account for sampling distributions.

3. **Spacegroup Definition (Conventional vs. Primitive)**:
   The `spacegroup` variable defines the symmetry operations of the crystal, but it is unclear whether the reported space groups and their corresponding lattice parameters (`a`, `b`, `c`, `alpha`, `beta`, `gamma`) correspond to the conventional standard setting or the primitive unit cell representation. Clarifying this is essential for correctly mapping symmetry-driven phase transitions and interpreting structural stability.