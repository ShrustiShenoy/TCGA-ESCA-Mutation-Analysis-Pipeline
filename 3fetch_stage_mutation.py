import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

# Base directory where mutation and CNV data is stored
BASE_FOLDER = "./grade_generalised"
stages = ["StageI", "StageII", "StageIII", "StageIV"]
samples_per_stage = 4  # Limit to 4 samples per stage

# Define coding variant classifications
CODING_VARIANTS = {
    "Missense_Mutation", "Nonsense_Mutation",
    "Frame_Shift_Ins", "Frame_Shift_Del", "Splice_Site",
    "Translation_Start_Site", "In_Frame_Del", "In_Frame_Ins"
}

def find_maf_files(directory):
    """Recursively find all .maf files in a given directory."""
    maf_files = []
    for root, _, files in os.walk(directory):
        maf_files.extend([os.path.join(root, f) for f in files if f.endswith(".maf")])
    return maf_files

def read_maf_file(maf_path):
    """Safely read a MAF file and filter only coding variants."""
    try:
        maf_df = pd.read_csv(maf_path, sep='\t', comment='#', encoding='utf-8', on_bad_lines='skip', low_memory=False)
        required_columns = {"Hugo_Symbol", "Variant_Classification"}
        
        if not required_columns.issubset(maf_df.columns):
            print(f"Skipping {maf_path}: Missing required columns {required_columns}")
            return None
        
        # Filter only coding variants
        maf_df = maf_df[maf_df["Variant_Classification"].isin(CODING_VARIANTS)]
        
        return maf_df if not maf_df.empty else None
    except Exception as e:
        print(f"Skipping {maf_path} due to error: {e}")
        return None

def get_sample_mutation_data(stage):
    """Retrieve mutation data for randomly selected cases in a given stage."""
    stage_dir = os.path.join(BASE_FOLDER, stage)
    if not os.path.exists(stage_dir):
        print(f"Warning: {stage_dir} does not exist.")
        return []
    
    case_folders = [f for f in os.listdir(stage_dir) if os.path.isdir(os.path.join(stage_dir, f))]
    
    if len(case_folders) < samples_per_stage:
        print(f"Warning: Only {len(case_folders)} samples found in {stage_dir}, but {samples_per_stage} required.")
    
    selected_cases = random.sample(case_folders, min(samples_per_stage, len(case_folders)))  # Randomly pick cases
    mutation_data = []
    
    for case in selected_cases:
        case_path = os.path.join(stage_dir, case)
        maf_files = find_maf_files(case_path)
        for maf_file in maf_files:
            maf_df = read_maf_file(maf_file)
            if maf_df is not None:
                maf_df['Case'] = case
                maf_df['Stage'] = stage
                mutation_data.append(maf_df)
    
    return mutation_data

def save_to_excel(df, output_file):
    """Saves the DataFrame to an Excel file with different sheets for each stage."""
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for stage, stage_df in df.groupby('Stage'):
            stage_df.to_excel(writer, sheet_name=stage, index=False)
            print(f"Saved {len(stage_df)} records to sheet: {stage}")

def visualize_mutation_cnv(df):
    """Generates visualizations for Mutation Frequency using Matplotlib."""
    if 'Variant_Classification' not in df.columns or 'Stage' not in df.columns:
        raise ValueError("The dataset must have 'Variant_Classification' and 'Stage' columns.")
    
    # Scatter plot for Mutation Frequency per Stage
    plt.figure(figsize=(12, 6))
    mutation_counts = df.groupby('Stage').size()
    plt.scatter(mutation_counts.index, mutation_counts.values, color='red', s=100)
    plt.plot(mutation_counts.index, mutation_counts.values, linestyle='--', color='black')
    plt.title("Mutation Frequency by Stage")
    plt.xlabel("Stage")
    plt.ylabel("Number of Mutations")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("mutation_frequency_scatter_filtered.png")
    plt.show()

def main():
    """Main function to collect mutation data, save it, and generate visualizations."""
    all_mutation_data = []
    
    for stage in stages:
        mutation_data = get_sample_mutation_data(stage)
        all_mutation_data.extend(mutation_data)
    
    if all_mutation_data:
        combined_df = pd.concat(all_mutation_data, ignore_index=True)
        save_to_excel(combined_df, "mutation_cnv_filtered.xlsx")
        visualize_mutation_cnv(combined_df)
    else:
        print("No coding mutation data collected! Ensure MAF files exist.")

if __name__ == "__main__":
    main()
