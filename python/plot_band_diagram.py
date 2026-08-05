#!/usr/bin/env python3
"""
FILE:    python/requirements.txt equivalent — install with:
         pip install numpy pandas matplotlib

FILE:    python/plot_band_diagram.py
PURPOSE: After running SDevice, SVisual exports the band diagram
         data as a text file. This script reads it and makes a
         publication-quality band diagram figure for all 4 materials.

HOW TO RUN:
    python3 plot_band_diagram.py

INPUT:   results/Si_bands.csv, Ge_bands.csv, GaAs_bands.csv, SiC4H_bands.csv
         (These are exported from SVisual manually or via script)
         OR use the theoretical band diagram calculated here.

OUTPUT:  results/band_diagrams.png
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# Material properties at 300K for theoretical band diagram
# Source: Sze & Ng, Physics of Semiconductor Devices, 3rd Ed.
MATERIAL_PROPS = {
    "Silicon": {
        "Eg": 1.12,          # bandgap (eV)
        "ni": 1.5e10,        # intrinsic concentration (cm^-3)
        "chi": 4.05,         # electron affinity (eV)
        "eps_r": 11.7,       # relative permittivity
        "color": "#1f77b4",
        "type": "indirect",
    },
    "Germanium": {
        "Eg": 0.66,
        "ni": 2.4e13,
        "chi": 4.0,
        "eps_r": 16.2,
        "color": "#2ca02c",
        "type": "indirect",
    },
    "GaAs": {
        "Eg": 1.42,
        "ni": 2.1e6,
        "chi": 4.07,
        "eps_r": 12.9,
        "color": "#d62728",
        "type": "direct",
    },
    "4H-SiC": {
        "Eg": 3.26,
        "ni": 8.2e-9,
        "chi": 3.7,
        "eps_r": 9.7,
        "color": "#9467bd",
        "type": "indirect",
    },
}

# Common doping for all materials
Na = 1e17   # P-region (cm^-3)
Nd = 1e16   # N-region (cm^-3)
kT = 0.02585  # thermal voltage at 300K (eV)


def compute_fermi_levels(Eg, Na, Nd, ni):
    """
    Compute the Fermi level position in P and N regions.
    For non-degenerate semiconductors:
        P-side: Ef measured from Ev = kT * ln(Na/ni)
        N-side: Ef measured from Ec = -kT * ln(Nd/ni)
    Returns Vbi (built-in voltage).
    """
    # Fermi level from midgap in P-region
    Ef_p = -kT * np.log(Na / ni)   # below midgap (closer to Ev)

    # Fermi level from midgap in N-region
    Ef_n = kT * np.log(Nd / ni)    # above midgap (closer to Ec)

    # Built-in voltage = difference in Fermi levels
    Vbi = kT * np.log(Na * Nd / ni**2)

    return Vbi, Ef_p, Ef_n


def plot_theoretical_band_diagram(ax, material, props, y_range=(0, 1.0)):
    """
    Plot a simplified theoretical band diagram for a PN junction.
    Uses the depletion approximation for the band bending shape.
    """
    Eg = props["Eg"]
    ni = props["ni"]
    color = props["color"]

    Vbi, Ef_p, Ef_n = compute_fermi_levels(Eg, Na, Nd, ni)

    # Create y-axis (position across device)
    y = np.linspace(0, 1.0, 500)   # 0 = top (P-side anode), 1 = bottom (N-side cathode)

    # Compute depletion width using abrupt junction formula
    eps_r = props["eps_r"]
    eps_0 = 8.854e-14   # F/cm
    q = 1.602e-19       # C
    eps = eps_r * eps_0
    W = np.sqrt(2 * eps * Vbi * (Na + Nd) / (q * Na * Nd))  # in cm
    W_um = W * 1e4  # convert to µm

    # Junction position
    y_junc = 0.5
    xp = (Nd / (Na + Nd)) * W_um   # depletion width in P-side (µm)
    xn = (Na / (Na + Nd)) * W_um   # depletion width in N-side (µm)

    # Build the Ec profile
    Ec = np.zeros_like(y)

    # P-region (y < y_junc - xp/1): Ec is HIGH (above reference)
    # N-region (y > y_junc + xn/1): Ec is LOW (reference = 0)
    # Depletion region: quadratic band bending

    p_bulk_end = y_junc - xp
    n_bulk_start = y_junc + xn

    for i, yi in enumerate(y):
        if yi < p_bulk_end:
            Ec[i] = Vbi           # P-side bulk: Ec is Vbi above N-side
        elif yi > n_bulk_start:
            Ec[i] = 0.0           # N-side bulk: reference level
        else:
            # Depletion region: quadratic bending
            # Normalized position within depletion region (0 to 1)
            t = (yi - p_bulk_end) / (n_bulk_start - p_bulk_end + 1e-10)
            Ec[i] = Vbi * (1 - t)**2   # parabolic bending (approximate)

    Ev = Ec - Eg     # Ev = Ec - Eg everywhere

    # Fermi level (flat at equilibrium)
    # In N-side bulk: Ef is kT*ln(Nd/ni) above Ec midgap
    # Aligned so Ef = 0 in N-side for reference
    Ef_line = np.zeros_like(y) + 0.0 - (Eg/2 - kT * np.log(Nd/ni))

    # Plot
    ax.plot(y, Ec, color=color, linewidth=2.0, linestyle='-')
    ax.plot(y, Ev, color=color, linewidth=2.0, linestyle='-')
    ax.plot(y, Ef_line, color=color, linewidth=1.0, linestyle='--', alpha=0.7)

    # Label Vbi arrow
    ax.annotate('', xy=(0.55, 0), xytext=(0.55, Vbi),
                arrowprops=dict(arrowstyle='<->', color=color, lw=1.5))
    ax.text(0.57, Vbi/2, f'Vbi={Vbi:.2f}V',
           fontsize=7, color=color, va='center')

    return Vbi


def main():
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Theoretical Equilibrium Band Diagrams — PN Junction\n"
                "Na = 1×10¹⁷ cm⁻³  |  Nd = 1×10¹⁶ cm⁻³  |  T = 300 K",
                fontsize=13, fontweight='bold')

    materials = list(MATERIAL_PROPS.keys())
    axes_flat = axes.flatten()

    for i, (material, props) in enumerate(MATERIAL_PROPS.items()):
        ax = axes_flat[i]
        Vbi = plot_theoretical_band_diagram(ax, material, props)

        ax.set_title(f"{material}  |  Eg = {props['Eg']} eV  |  {props['type']} gap",
                    fontsize=11, fontweight='bold', color=props['color'])
        ax.set_xlabel("Position y (µm)", fontsize=10)
        ax.set_ylabel("Energy (eV)", fontsize=10)
        ax.axvline(x=0.5, color='gray', linestyle=':', alpha=0.5, linewidth=1)
        ax.text(0.5, ax.get_ylim()[1]*0.95 if i > 0 else props['Eg'] + Vbi + 0.1,
               'Junction', ha='center', fontsize=8, color='gray')
        ax.text(0.2, ax.get_ylim()[1]*0.1 if i > 0 else 0.1, 'P-type',
               ha='center', fontsize=9, style='italic')
        ax.text(0.8, ax.get_ylim()[1]*0.1 if i > 0 else 0.1, 'N-type',
               ha='center', fontsize=9, style='italic')

        # Legend
        ec_patch = mpatches.Patch(color=props['color'], label='Ec, Ev')
        ef_patch = mpatches.Patch(color=props['color'], alpha=0.5, label=f'Ef (Vbi={Vbi:.2f}V)')
        ax.legend(handles=[ec_patch, ef_patch], fontsize=8, loc='upper right')
        ax.grid(True, alpha=0.2)

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, "band_diagrams.png")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()

    print("Saved: results/band_diagrams.png")
    print("\nMaterial Properties Summary:")
    print(f"{'Material':<12} {'Eg (eV)':<10} {'ni (cm-3)':<15} {'Vbi (V)':<10} {'Gap Type'}")
    print("-" * 60)
    for mat, props in MATERIAL_PROPS.items():
        Vbi, _, _ = compute_fermi_levels(props['Eg'], Na, Nd, props['ni'])
        print(f"{mat:<12} {props['Eg']:<10} {props['ni']:<15.2e} {Vbi:<10.3f} {props['type']}")


if __name__ == "__main__":
    main()
