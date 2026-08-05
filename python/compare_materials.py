#!/usr/bin/env python3
"""
FILE:    python/compare_materials.py
PURPOSE: Read SDevice .plt output files for all 4 materials,
         extract key parameters, and generate a comparison
         table + overlay plots.

HOW TO RUN:
    python3 compare_materials.py

REQUIRED FILES (in ../results/ folder):
    Si_des.plt
    Ge_des.plt
    GaAs_des.plt
    SiC4H_des.plt

    These files are what SDevice writes when the Workbench
    runs the simulation for each material. Copy them from
    the SWB output folders (n1_Si, n2_Ge, etc.) into results/.

OUTPUTS:
    results/comparison_table.csv     → numbers for your report
    results/iv_overlay.png           → all 4 I-V curves on one plot
    results/leakage_comparison.png   → reverse leakage bar chart
    results/breakdown_comparison.png → breakdown voltage bar chart
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# Adjust these paths to match where SWB puts its output.
# SWB creates numbered folders like: n1_Si/, n2_Ge/ etc.
# ============================================================

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Map material name → expected .plt filename
# Adjust these filenames to match your SWB project naming
MATERIALS = {
    "Silicon":     "Si_des.plt",
    "Germanium":   "Ge_des.plt",
    "GaAs":        "GaAs_des.plt",
    "4H-SiC":      "SiC4H_des.plt",
}

# Colors for each material in overlay plots
COLORS = {
    "Silicon":     "#1f77b4",   # blue
    "Germanium":   "#2ca02c",   # green
    "GaAs":        "#d62728",   # red
    "4H-SiC":      "#9467bd",   # purple
}

# Line styles for print-friendly plots
LINESTYLES = {
    "Silicon":     "-",
    "Germanium":   "--",
    "GaAs":        "-.",
    "4H-SiC":      ":",
}


# ============================================================
# FUNCTION 1: PARSE A SENTAURUS .plt FILE
# The .plt file format is:
#   - Header lines starting with #
#   - A line defining column names
#   - Data rows (space-separated numbers)
# ============================================================

def parse_plt_file(filepath):
    """
    Parse a Sentaurus Device .plt output file.
    Returns a pandas DataFrame with columns named after
    the electrical quantities (voltage, currents, etc.)

    The .plt file has this structure:
    # Sentaurus Device output
    # ...
    # Version ...
    #---
    "Anode OuterVoltage"  "Anode TotalCurrent"  "Cathode TotalCurrent"
    0.0   1.23e-20   -1.23e-20
    0.01  1.45e-20   -1.45e-20
    ...
    """
    headers = []
    data_rows = []
    header_found = False

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Skip comment lines (start with #)
            if line.startswith('#'):
                continue

            # The first non-comment, non-empty line = column headers
            if not header_found:
                # Column names are quoted strings
                # e.g.: "Anode OuterVoltage" "Anode TotalCurrent"
                import re
                headers = re.findall(r'"([^"]+)"', line)
                if headers:
                    header_found = True
                continue

            # All subsequent lines = data
            try:
                values = [float(v) for v in line.split()]
                if len(values) == len(headers):
                    data_rows.append(values)
            except ValueError:
                continue

    if not headers or not data_rows:
        raise ValueError(f"Could not parse file: {filepath}")

    return pd.DataFrame(data_rows, columns=headers)


# ============================================================
# FUNCTION 2: EXTRACT KEY PARAMETERS FROM I-V DATA
# From the parsed DataFrame, extract the important numbers
# that go into the comparison table.
# ============================================================

def extract_parameters(df, material_name):
    """
    Extract key device parameters from the I-V data.

    Parameters extracted:
    - Turn-on voltage (Vt): voltage where current first exceeds 1 µA
    - Forward current at 0.5V, 0.7V, 1.0V
    - Reverse leakage current at -1V (saturation current I0)
    - Approximate breakdown voltage (where reverse current > 1 mA)
    - Ideality factor (from slope of log I vs V in forward region)
    """
    params = {"Material": material_name}

    # Find voltage and current columns
    # Column names in .plt are like "Anode OuterVoltage" and "Anode TotalCurrent"
    volt_col = [c for c in df.columns if "Voltage" in c][0]
    curr_col = [c for c in df.columns if "TotalCurrent" in c and "Anode" in c][0]

    V = df[volt_col].values
    I = df[curr_col].values

    # Split into forward and reverse datasets
    fwd_mask = V >= 0
    rev_mask = V <= 0

    V_fwd = V[fwd_mask]
    I_fwd = I[fwd_mask]
    V_rev = V[rev_mask]
    I_rev = I[rev_mask]

    # --- Turn-on voltage: where |I| first exceeds 1 µA ---
    threshold = 1e-6  # 1 µA
    turnon_idx = np.where(np.abs(I_fwd) > threshold)[0]
    if len(turnon_idx) > 0:
        params["Turn-on Voltage (V)"] = round(V_fwd[turnon_idx[0]], 3)
    else:
        params["Turn-on Voltage (V)"] = ">1.0"

    # --- Forward current at specific voltages ---
    for v_check in [0.5, 0.7, 1.0]:
        idx = np.argmin(np.abs(V_fwd - v_check))
        if abs(V_fwd[idx] - v_check) < 0.05:  # within 50mV
            params[f"I at {v_check}V (A)"] = f"{I_fwd[idx]:.3e}"
        else:
            params[f"I at {v_check}V (A)"] = "N/A"

    # --- Reverse saturation current I0 at -1V ---
    idx_1v = np.argmin(np.abs(V_rev - (-1.0)))
    if abs(V_rev[idx_1v] - (-1.0)) < 0.1:
        params["I0 at -1V (A)"] = f"{abs(I_rev[idx_1v]):.3e}"
    else:
        params["I0 at -1V (A)"] = "N/A"

    # --- Breakdown voltage: where |reverse current| > 1 mA ---
    breakdown_threshold = 1e-3  # 1 mA
    bv_idx = np.where(np.abs(I_rev) > breakdown_threshold)[0]
    if len(bv_idx) > 0:
        params["Breakdown Voltage (V)"] = round(V_rev[bv_idx[0]], 1)
    else:
        params["Breakdown Voltage (V)"] = f"< {V_rev.min():.0f}V (not reached)"

    # --- Ideality factor from slope of ln(I) vs V ---
    # In the exponential region (I between 1 nA and 1 µA for forward bias)
    q = 1.602e-19   # electron charge (C)
    kT = 0.02585    # thermal voltage at 300K (V) = kT/q

    mask_exp = (I_fwd > 1e-12) & (I_fwd < 1e-4) & (V_fwd > 0.1)
    if np.sum(mask_exp) > 5:
        V_exp = V_fwd[mask_exp]
        I_exp = I_fwd[mask_exp]
        # Linear fit to ln(I) vs V → slope = q/(n*kT) → n = q/(slope*kT)
        slope, _ = np.polyfit(V_exp, np.log(I_exp), 1)
        ideality = 1.0 / (slope * kT)
        params["Ideality Factor n"] = round(ideality, 2)
    else:
        params["Ideality Factor n"] = "N/A"

    return params


# ============================================================
# FUNCTION 3: PLOT ALL 4 I-V CURVES OVERLAID
# ============================================================

def plot_iv_overlay(all_data, output_dir):
    """
    Plot all 4 material I-V curves on one figure for direct comparison.
    Creates both linear and log-scale versions.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("I-V Characteristics — Material Comparison\nPN Diode: Na=1e17 cm⁻³, Nd=1e16 cm⁻³, T=300K",
                 fontsize=13, fontweight='bold')

    # --- Left plot: Forward bias log scale ---
    ax1 = axes[0]
    ax1.set_title("Forward Bias — Log Scale", fontsize=11)
    ax1.set_xlabel("Anode Voltage (V)")
    ax1.set_ylabel("|Current| (A)")
    ax1.set_yscale('log')
    ax1.set_xlim(0, 1.0)
    ax1.set_ylim(1e-18, 1e-1)
    ax1.grid(True, which='both', alpha=0.3)

    for mat, (V, I) in all_data.items():
        fwd = V >= 0
        ax1.plot(V[fwd], np.abs(I[fwd]),
                color=COLORS[mat],
                linestyle=LINESTYLES[mat],
                linewidth=2,
                label=mat)

    ax1.legend(fontsize=10, loc='upper left')

    # --- Right plot: Reverse bias log scale ---
    ax2 = axes[1]
    ax2.set_title("Reverse Bias — Log Scale", fontsize=11)
    ax2.set_xlabel("Anode Voltage (V)")
    ax2.set_ylabel("|Current| (A)")
    ax2.set_yscale('log')
    ax2.set_xlim(-20, 0)
    ax2.set_ylim(1e-20, 1e-2)
    ax2.grid(True, which='both', alpha=0.3)

    for mat, (V, I) in all_data.items():
        rev = V <= 0
        ax2.plot(V[rev], np.abs(I[rev]),
                color=COLORS[mat],
                linestyle=LINESTYLES[mat],
                linewidth=2,
                label=mat)

    ax2.legend(fontsize=10, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "iv_overlay.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: iv_overlay.png")


# ============================================================
# FUNCTION 4: PLOT LEAKAGE CURRENT BAR CHART
# ============================================================

def plot_leakage_comparison(comparison_table, output_dir):
    """
    Bar chart comparing reverse saturation current I0 at -1V
    across all 4 materials. Uses log scale because values
    differ by many orders of magnitude.
    """
    materials = comparison_table["Material"].tolist()
    leakage_values = []

    for _, row in comparison_table.iterrows():
        val_str = row["I0 at -1V (A)"]
        try:
            leakage_values.append(float(val_str))
        except:
            leakage_values.append(np.nan)

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = [COLORS[m] for m in materials]
    bars = ax.bar(materials, leakage_values, color=colors, edgecolor='black', linewidth=1.2)
    ax.set_yscale('log')
    ax.set_title("Reverse Leakage Current (I₀) at -1V\nMaterial Comparison", fontsize=13, fontweight='bold')
    ax.set_xlabel("Semiconductor Material", fontsize=12)
    ax.set_ylabel("Leakage Current |I₀| (A) — Log Scale", fontsize=12)
    ax.grid(True, axis='y', alpha=0.4)

    # Add value labels on top of bars
    for bar, val in zip(bars, leakage_values):
        if not np.isnan(val):
            ax.text(bar.get_x() + bar.get_width()/2, val * 2,
                   f"{val:.2e}", ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "leakage_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved: leakage_comparison.png")


# ============================================================
# FUNCTION 5: SAVE COMPARISON TABLE TO CSV
# ============================================================

def save_comparison_table(comparison_table, output_dir):
    """
    Save the full comparison table as a CSV file.
    You can open this in Excel/LibreOffice for your report.
    """
    csv_path = os.path.join(output_dir, "comparison_table.csv")
    comparison_table.to_csv(csv_path, index=False)
    print(f"Saved: comparison_table.csv")
    print("\n" + "="*60)
    print("MATERIAL COMPARISON TABLE")
    print("="*60)
    print(comparison_table.to_string(index=False))
    print("="*60)


# ============================================================
# MAIN: RUN ALL ANALYSIS
# ============================================================

def main():
    print("Sentaurus TCAD — Material Comparison Analysis")
    print("="*50)

    all_params = []
    all_data = {}

    for material, plt_filename in MATERIALS.items():
        plt_path = os.path.join(RESULTS_DIR, plt_filename)

        if not os.path.exists(plt_path):
            print(f"WARNING: File not found — {plt_path}")
            print(f"  Copy {plt_filename} from SWB output to results/ folder")
            continue

        print(f"Processing: {material}...")

        try:
            df = parse_plt_file(plt_path)
            params = extract_parameters(df, material)
            all_params.append(params)

            # Store V, I arrays for overlay plot
            volt_col = [c for c in df.columns if "Voltage" in c][0]
            curr_col = [c for c in df.columns if "TotalCurrent" in c and "Anode" in c][0]
            all_data[material] = (df[volt_col].values, df[curr_col].values)

            print(f"  Turn-on voltage: {params.get('Turn-on Voltage (V)', 'N/A')} V")
            print(f"  Ideality factor: {params.get('Ideality Factor n', 'N/A')}")

        except Exception as e:
            print(f"ERROR processing {material}: {e}")

    if not all_params:
        print("\nNo data files found in results/ folder.")
        print("Run the SWB simulation first, then copy the .plt files here.")
        return

    # Build comparison table
    comparison_table = pd.DataFrame(all_params)

    # Generate all outputs
    save_comparison_table(comparison_table, RESULTS_DIR)

    if len(all_data) > 0:
        plot_iv_overlay(all_data, RESULTS_DIR)

    if len(comparison_table) > 0:
        plot_leakage_comparison(comparison_table, RESULTS_DIR)

    print("\nDone! All output files saved to: results/")
    print("Open results/iv_overlay.png for the material comparison plot.")


if __name__ == "__main__":
    main()
