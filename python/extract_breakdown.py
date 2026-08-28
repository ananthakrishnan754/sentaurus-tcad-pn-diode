#!/usr/bin/env python3
"""
FILE:    python/extract_breakdown.py
PURPOSE: Extract breakdown voltage from reverse I-V data by finding
         the knee point where current rises sharply.
         Also computes the depletion width from the C-V relationship.

HOW TO RUN:
    python3 extract_breakdown.py

INPUT:   results/Si_des.plt (and Ge, GaAs, SiC4H)
OUTPUT:  results/breakdown_analysis.png
"""

import numpy as np
import matplotlib.pyplot as plt
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

MATERIALS = {
    "Silicon":   "Si_des.plt",
    "Germanium": "Ge_des.plt",
    "GaAs":      "GaAs_des.plt",
    "4H-SiC":    "SiC4H_des.plt",
}

COLORS = {
    "Silicon":   "#1f77b4",
    "Germanium": "#2ca02c",
    "GaAs":      "#d62728",
    "4H-SiC":    "#9467bd",
}


def parse_plt_file(filepath):
    import re
    with open(filepath, "r") as f:
        content = f.read()
    m = re.search(r"datasets\s*=\s*\[(.*?)\]", content, re.DOTALL)
    if not m:
        raise ValueError(f"No datasets block in {filepath}")
    col_names = re.findall(r'"([^"]+)"', m.group(1))
    n_cols = len(col_names)
    dm = re.search(r"Data\s*\{(.*?)\}", content, re.DOTALL)
    if not dm:
        raise ValueError(f"No Data block in {filepath}")
    vals = np.array([float(v) for v in
                     re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?",
                                dm.group(1))])
    if len(vals) % n_cols != 0:
        raise ValueError(f"Data length {len(vals)} not divisible by {n_cols} cols in {filepath}")
    n_rows = len(vals) // n_cols
    import pandas as pd
    return pd.DataFrame(vals.reshape(n_rows, n_cols), columns=col_names)

def find_breakdown_voltage(V_rev, I_rev, threshold=1e-4):
    abs_I = np.abs(I_rev)
    above_threshold = np.where(abs_I > threshold)[0]
    if len(above_threshold) > 0:
        return V_rev[above_threshold[0]]
    return None


def compute_depletion_width(V_rev, Na, Nd, eps_r, material):
    """
    Theoretically compute the depletion width as a function
    of reverse voltage using the abrupt junction approximation:

        W(V) = sqrt(2 * eps * (Vbi - V) / q * (Na + Nd) / (Na * Nd))

    where:
        eps = eps_r * eps_0 (permittivity)
        Vbi = (kT/q) * ln(Na * Nd / ni^2) (built-in voltage)
        V = applied voltage (negative for reverse bias)

    This gives the theoretical depletion width — compare to
    what you see in the SVisual plots!
    """
    q = 1.602e-19        # C
    eps_0 = 8.854e-14    # F/cm
    kT_q = 0.02585       # V at 300K

    # Intrinsic carrier concentrations at 300K
    ni_values = {
        "Silicon":   1.5e10,   # cm^-3
        "Germanium": 2.4e13,   # cm^-3
        "GaAs":      2.1e6,    # cm^-3 (much smaller due to large bandgap)
        "4H-SiC":    8.2e-9,   # cm^-3 (extremely small due to very large bandgap)
    }

    ni = ni_values.get(material, 1.5e10)

    # Built-in voltage
    Vbi = kT_q * np.log(Na * Nd / ni**2)

    # Permittivity
    eps = eps_r * eps_0

    # Depletion width at each reverse voltage (V is negative)
    V_total = Vbi - V_rev   # total potential across junction
    V_total = np.maximum(V_total, 0)  # can't be negative

    W = np.sqrt(2 * eps * V_total * (Na + Nd) / (q * Na * Nd))
    W_um = W * 1e4  # convert cm to µm

    return Vbi, W_um


def main():
    print("Breakdown Voltage & Depletion Width Analysis")
    print("="*50)

    # Material-specific parameters for depletion width calculation
    material_params = {
        "Silicon":   {"Na": 1e17, "Nd": 1e16, "eps_r": 11.7},
        "Germanium": {"Na": 1e17, "Nd": 1e16, "eps_r": 16.2},
        "GaAs":      {"Na": 1e17, "Nd": 1e16, "eps_r": 12.9},
        "4H-SiC":    {"Na": 1e17, "Nd": 1e16, "eps_r": 9.7},
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Breakdown & Depletion Analysis — Material Comparison",
                fontsize=13, fontweight='bold')

    ax1 = axes[0]
    ax1.set_title("Reverse I-V — Breakdown Region")
    ax1.set_xlabel("Reverse Voltage (V)")
    ax1.set_ylabel("|Current| (A) — Log Scale")
    ax1.set_yscale('log')
    ax1.grid(True, which='both', alpha=0.3)

    ax2 = axes[1]
    ax2.set_title("Theoretical Depletion Width vs Reverse Voltage")
    ax2.set_xlabel("Reverse Voltage (V)")
    ax2.set_ylabel("Depletion Width W (µm)")
    ax2.grid(True, alpha=0.3)

    V_sweep = np.linspace(0, -20, 200)  # voltage range for W calculation

    results = []

    for material, plt_filename in MATERIALS.items():
        plt_path = os.path.join(RESULTS_DIR, plt_filename)
        color = COLORS[material]
        params = material_params[material]

        # Plot theoretical depletion width (always, even without .plt data)
        Vbi, W_theory = compute_depletion_width(
            V_sweep,
            params["Na"], params["Nd"], params["eps_r"], material
        )
        ax2.plot(-V_sweep, W_theory, color=color, linewidth=2, label=f"{material} (Vbi={Vbi:.2f}V)")

        print(f"\n{material}:")
        print(f"  Built-in voltage Vbi = {Vbi:.3f} V")
        print(f"  Depletion width at 0V = {W_theory[0]:.3f} µm")
        print(f"  Depletion width at -5V = {W_theory[np.argmin(np.abs(V_sweep+5))]:.3f} µm")

        # Load and plot actual simulation data if available
        if not os.path.exists(plt_path):
            print(f"  WARNING: {plt_filename} not found in results/")
            continue

        try:
            df = parse_plt_file(plt_path)
            volt_col = [c for c in df.columns if "OuterVoltage" in c and "Anode" in c][0]
            curr_col = [c for c in df.columns if "TotalCurrent" in c and "Anode" in c][0]
            V = df[volt_col].values
            I = df[curr_col].values

            # Only reverse bias
            rev_mask = V <= 0
            V_rev = V[rev_mask]
            I_rev = I[rev_mask]

            ax1.plot(V_rev, np.abs(I_rev), color=color, linewidth=2, label=material)

            # Find breakdown
            bv = find_breakdown_voltage(V_rev, I_rev)
            if bv is not None:
                print(f"  Breakdown voltage ≈ {bv:.1f} V")
                results.append({"Material": material, "Vbr (V)": bv, "Vbi (V)": round(Vbi, 3)})
                ax1.axvline(x=bv, color=color, linestyle=':', alpha=0.7)
            else:
                print(f"  Breakdown not reached in sweep range")
                results.append({"Material": material, "Vbr (V)": "Not reached", "Vbi (V)": round(Vbi, 3)})

        except Exception as e:
            print(f"  Error reading {plt_filename}: {e}")

    ax1.legend(fontsize=10)
    ax2.legend(fontsize=10)

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, "breakdown_analysis.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: breakdown_analysis.png")

    if results:
        print("\nBreakdown Summary:")
        for r in results:
            print(f"  {r['Material']}: Vbi={r['Vbi (V)']}V, Vbr={r['Vbr (V)']}V")


if __name__ == "__main__":
    main()
