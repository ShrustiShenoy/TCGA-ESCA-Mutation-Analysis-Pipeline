# TCGA-ESCA-Mutation-Analysis-Pipeline
This script performs a downstream analysis of somatic mutation data from TCGA Esophageal Carcinoma (ESCA) samples. It processes locally downloaded .maf files organized by AJCC stages, filters for coding variants, and produces:

A clean multi-sheet Excel file with mutations per stage.

A mutation frequency scatter plot for quick stage-wise comparison.

# Objectives
Parse .maf files from local TCGA-ESCA sample directories.

Extract and retain only coding mutations based on Variant_Classification.

Visualize mutation frequency distribution across stages.

Export a structured .xlsx output for downstream analysis.

# The pipeline:

Recursively scans downloaded data (./grade_generalised/<Stage>/<CaseID>/)

Extracts and filters mutation calls from .maf files

Summarizes and visualizes mutation frequency per stage

Exports per-stage sheets and combined Excel output

# Directory Structure

grade_generalised/
├── StageI/
│   ├── TCGA-XX-XXXX-01A/
│   │   └── <*.maf>
├── StageII/
│   ├── ...

# Dependencies
pip install pandas matplotlib numpy xlsxwriter
