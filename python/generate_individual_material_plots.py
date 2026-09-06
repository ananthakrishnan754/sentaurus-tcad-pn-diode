#!/usr/bin/env python3
"""
generate_individual_material_plots.py
================================================================================
Generates publication-quality, standalone 300 DPI figures for each material
simulated in the TCAD Material-Engineered PN Diode & Photodiode project:
  1. Silicon (Si)
  2. Germanium (Ge)
  3. Gallium Arsenide (GaAs) & GaAs LED
  4. 4H-Silicon Carbide (4H-SiC)

Outputs saved to: results/
================================================================================
"""

import os
import re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

def parse_df_ise(filepath):
    """Accurately parses Sentaurus DF-ISE .plt files into dictionary of datasets."""
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r') as f:
        content = f.read()

    ds_match = re.search(r'datasets\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not ds_match:
        return None

    headers = [h.strip('" ') for h in re.findall(r'"([^"]+)"', ds_match.group(1))]

    data_match = re.search(r'Data\s*\{(.*?)\}', content, re.DOTALL)
    if not data_match:
        return None

    raw_tokens = data_match.group(1).split()
    values = []
    for tok in raw_tokens:
        try:
            values.append(float(tok))
        except ValueError:
            pass

    num_cols = len(headers)
    if num_cols == 0:
        return None

    num_rows = len(values) // num_cols
    values = values[:num_rows * num_cols]
    arr = np.array(values).reshape(num_rows, num_cols)

    ds_dict = {}
    for idx, name in enumerate(headers):
        ds_dict[name.lower()] = arr[:, idx]

    v_key, i_key = None, None
    for k in ds_dict.keys():
        if 'anode' in k and 'outervoltage' in k:
            v_key = k
        elif 'anode' in k and 'totalcurrent' in k:
            i_key = k

    if not v_key:
        for k in ds_dict.keys():
            if 'voltage' in k and 'outer' in k:
                v_key = k
                break
    if not i_key:
        for k in ds_dict.keys():
            if 'totalcurrent' in k or 'current' in k:
                i_key = k
                break

    if v_key and i_key:
        return {'v': ds_dict[v_key], 'i': ds_dict[i_key]}
    return None

def generate_individual_plot(mat_name, plt_file, eg, vbi, von, i0, n_factor, color, out_name):
    path = os.path.join(RESULTS_DIR, plt_file)
    data = parse_df_ise(path)
    if not data:
        print(f"Warning: {path} not found.")
        return

    V = data['v']
    I = data['i']

    # Sort forward and reverse
    fwd_mask = V >= 0
    V_fwd, I_fwd = V[fwd_mask], np.abs(I[fwd_mask])
    s_f = np.argsort(V_fwd)
    V_fwd, I_fwd = V_fwd[s_f], I_fwd[s_f]
    _, u_f = np.unique(V_fwd, return_index=True)
    V_fwd, I_fwd = V_fwd[u_f], I_fwd[u_f]

    rev_mask = V <= 0
    V_rev, I_rev = V[rev_mask], np.abs(I[rev_mask])
    s_r = np.argsort(V_rev)
    V_rev, I_rev = V_rev[s_r], I_rev[s_r]

    # Create 2-panel figure: Left = Forward (Log + Linear inset/dual axis), Right = Reverse
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    fig.suptitle(f"{mat_name} PN Diode Detailed I-V Characteristics\n"
                 f"[Bandgap $E_g = {eg}$, $V_{{bi}} = {vbi}$, Junction Area $1.0\\,\\mu m^2$, $T=300\\text{{ K}}$]",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    # --- LEFT PANEL: Forward Bias (Log scale + Linear scale secondary) ---
    ax1.set_title("Forward Bias Characteristics", fontsize=11, fontweight='bold', pad=10)
    ax1.set_xlabel("Anode Forward Voltage $V_A$ (V)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Forward Current $|I_A|$ (A) [Log Scale]", fontsize=10, fontweight='bold', color=color)
    ax1.set_yscale('log')
    ax1.set_xlim(0, 1.0)
    ax1.set_ylim(1e-18, 1e-2)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)

    line1 = ax1.plot(V_fwd, I_fwd, color=color, linewidth=2.5, label=f'{mat_name} (Log $|I|$)')

    # Mark knee / turn-on voltage
    if von is not None and von > 0:
        ax1.axvline(x=von, color='#dc2626', linestyle=':', linewidth=1.5, label=f'$V_{{on}} = {von:.3f}\\,V$')
        ax1.scatter([von], [1e-6 if np.max(I_fwd)>=1e-6 else 1e-10], color='#dc2626', s=45, zorder=5)

    # Secondary linear axis
    ax1_lin = ax1.twinx()
    ax1_lin.set_ylabel("Forward Current $I_A$ (mA) [Linear Scale]", fontsize=10, fontweight='bold', color='#475569')
    ax1_lin.plot(V_fwd, I_fwd * 1e3, color='#64748b', linestyle='--', linewidth=1.8, label=f'{mat_name} (Linear mA)')
    ax1_lin.set_ylim(0, max(0.25, np.max(I_fwd)*1.15e3))
    ax1_lin.tick_params(axis='y', labelcolor='#475569')

    # Combine legends
    lines = line1 + [ax1.get_lines()[-1]] if len(ax1.get_lines())>1 else line1
    labels = [l.get_label() for l in lines] + [ax1_lin.get_lines()[0].get_label()]
    lines.append(ax1_lin.get_lines()[0])
    ax1.legend(lines, labels, loc='upper left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    # Annotate Ideality Factor
    box_props = dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#cbd5e1', alpha=0.9)
    ax1.text(0.55, 0.20, f"Ideality Factor $n = {n_factor:.2f}$\n$V_{{on}} (1\\,\\mu A) = {von if von else 'N/A'}\\,V$",
             transform=ax1.transAxes, fontsize=9.5, verticalalignment='bottom', bbox=box_props)

    # --- RIGHT PANEL: Reverse Bias (Log scale) ---
    ax2.set_title("Reverse Bias Leakage & Saturation", fontsize=11, fontweight='bold', pad=10)
    ax2.set_xlabel("Anode Reverse Voltage $V_A$ (V)", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Reverse Leakage Current $|I_A|$ (A)", fontsize=10, fontweight='bold')
    ax2.set_yscale('log')
    ax2.set_xlim(-20.0, 0.0)
    ax2.set_ylim(1e-20, 1e-6)
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)

    ax2.plot(V_rev, I_rev, color=color, linewidth=2.2, label=f'{mat_name} Reverse $I(V)$')

    # Annotate -1V leakage
    ax2.scatter([-1.0], [i0], color='#d97706', s=50, zorder=5)
    ax2.annotate(f"$I_0(-1V) = {i0:.2e}\\,A$",
                 xy=(-1.0, i0), xytext=(-12.0, i0 * 8 if i0 < 1e-12 else i0 * 3),
                 arrowprops=dict(facecolor='#d97706', shrink=0.08, width=1, headwidth=6),
                 fontsize=9.5, fontweight='bold', color='#92400e',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbeb', edgecolor='#fde68a'))

    ax2.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, out_name)
    plt.savefig(out_path)
    plt.close()
    print(f"Generated standalone plot: {out_path}")

def main():
    print("Generating comprehensive standalone 300 DPI plots for each material...")

    # 1. Silicon
    generate_individual_plot(
        mat_name="Silicon (Si)",
        plt_file="Silicon_des.plt",
        eg="1.12\\text{ eV}",
        vbi="0.753\\text{ V}",
        von=0.657,
        i0=1.41e-16,
        n_factor=1.16,
        color="#1f77b4",
        out_name="Silicon_IV_Detailed.png"
    )

    # 2. Germanium
    generate_individual_plot(
        mat_name="Germanium (Ge)",
        plt_file="Germanium_des.plt",
        eg="0.66\\text{ eV}",
        vbi="0.371\\text{ V}",
        von=0.246,
        i0=2.95e-10,
        n_factor=1.16,
        color="#2ca02c",
        out_name="Germanium_IV_Detailed.png"
    )

    # 3. Gallium Arsenide
    generate_individual_plot(
        mat_name="Gallium Arsenide (GaAs)",
        plt_file="GaAs_des.plt",
        eg="1.42\\text{ eV}",
        vbi="1.212\\text{ V}",
        von=0.805, # at 0.1 nA
        i0=6.76e-17,
        n_factor=1.56,
        color="#d62728",
        out_name="GaAs_IV_Detailed.png"
    )

    # 4. 4H-Silicon Carbide
    generate_individual_plot(
        mat_name="4H-Silicon Carbide (4H-SiC)",
        plt_file="SiC4H_des.plt",
        eg="3.26\\text{ eV}",
        vbi="2.927\\text{ V}",
        von=0.674,
        i0=8.97e-17,
        n_factor=1.17,
        color="#9467bd",
        out_name="SiC4H_IV_Detailed.png"
    )

    # 5. Photodiode Light vs Dark & LED Overlay
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)
    fig.suptitle("Optoelectronic Devices: PIN Photodiodes & GaAs LED\n"
                 "[Spectral Illumination $\\lambda = 0.55\\,\\mu m$, $P_{opt} = 10\\text{ mW/cm}^2$]",
                 fontsize=13, fontweight='bold', color='#0f172a', y=0.98)

    si_dark = parse_df_ise(os.path.join(RESULTS_DIR, "Si_dark_des.plt"))
    si_opt = parse_df_ise(os.path.join(RESULTS_DIR, "Si_opt_des.plt"))
    gaas_dark = parse_df_ise(os.path.join(RESULTS_DIR, "GaAs_dark_des.plt"))
    gaas_opt = parse_df_ise(os.path.join(RESULTS_DIR, "GaAs_opt_des.plt"))
    gaas_led = parse_df_ise(os.path.join(RESULTS_DIR, "GaAs_LED_des.plt"))

    # Photodiode Reverse Photoresponse
    ax1.set_title("Photodiode Photoresponse: Dark vs Illuminated", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Reverse Voltage $V_{bias}$ (V)", fontsize=10, fontweight='bold')
    ax1.set_ylabel("Current $|I|$ (A) [Log Scale]", fontsize=10, fontweight='bold')
    ax1.set_yscale('log')
    ax1.set_xlim(-3.0, 0.0)
    ax1.set_ylim(1e-17, 1e-13)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)

    if si_dark: ax1.plot(si_dark['v'], np.abs(si_dark['i']), '#1f77b4', linestyle='--', linewidth=2, label='Silicon (Dark)')
    if si_opt: ax1.plot(si_opt['v'], np.abs(si_opt['i']), '#1f77b4', linestyle='-', linewidth=2.2, label='Silicon ($10\\text{ mW/cm}^2$)')
    if gaas_dark: ax1.plot(gaas_dark['v'], np.abs(gaas_dark['i']), '#d62728', linestyle='--', linewidth=2, label='GaAs (Dark)')
    if gaas_opt: ax1.plot(gaas_opt['v'], np.abs(gaas_opt['i']), '#d62728', linestyle='-', linewidth=2.2, label='GaAs ($10\\text{ mW/cm}^2$)')
    ax1.legend(loc='lower left', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)

    # LED Forward Light Emitting Response
    ax2.set_title("GaAs Direct-Bandgap LED Electroluminescence I-V", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Anode Forward Voltage $V_A$ (V)", fontsize=10, fontweight='bold')
    ax2.set_ylabel("Forward Current $|I_A|$ (A)", fontsize=10, fontweight='bold')
    ax2.set_yscale('log')
    ax2.set_xlim(0.0, 1.6)
    ax2.set_ylim(1e-15, 1e-12)
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.6)

    if gaas_led:
        ax2.plot(gaas_led['v'], np.abs(gaas_led['i']), color='#e11d48', linewidth=2.5, label='GaAs LED Forward Recombination')
        ax2.annotate("Spontaneous Radiative\nEmission Regime ($> 1.0\\,V$)",
                     xy=(1.2, 3.5e-14), xytext=(0.4, 2e-13),
                     arrowprops=dict(facecolor='#e11d48', shrink=0.08, width=1, headwidth=5),
                     fontsize=9, fontweight='bold', color='#9f1239',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff1f2', edgecolor='#fecdd3'))
    ax2.legend(loc='lower right', frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9.5)

    plt.tight_layout()
    opt_out = os.path.join(RESULTS_DIR, "Optoelectronic_Photodiode_LED_Detailed.png")
    plt.savefig(opt_out)
    plt.close()
    print(f"Generated standalone plot: {opt_out}")

if __name__ == "__main__":
    main()
