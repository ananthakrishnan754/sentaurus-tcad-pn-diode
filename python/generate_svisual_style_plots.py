import os
import re
import numpy as np
import matplotlib.pyplot as plt

def parse_df_ise_plt(filepath):
    """Accurately parses Sentaurus DF-ISE .plt files into dictionary of datasets."""
    if not os.path.exists(filepath):
        return None

    with open(filepath, 'r') as f:
        content = f.read()

    # Extract datasets list
    ds_match = re.search(r'datasets\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not ds_match:
        return None

    headers = [h.strip('" ') for h in re.findall(r'"([^"]+)"', ds_match.group(1))]

    # Extract data values
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
    if num_cols == 0 or len(values) % num_cols != 0:
        # Fallback if header count mismatch
        num_rows = len(values) // num_cols if num_cols > 0 else 0
        if num_rows == 0:
            return None
        values = values[:num_rows * num_cols]

    arr = np.array(values).reshape(-1, num_cols)

    # Map header names to column data
    ds_dict = {}
    for idx, name in enumerate(headers):
        ds_dict[name.lower()] = arr[:, idx]

    # Find Anode / Cathode voltage & current
    v_key = None
    i_key = None

    for k in ds_dict.keys():
        if 'anode' in k and 'outervoltage' in k:
            v_key = k
        elif 'anode' in k and 'totalcurrent' in k:
            i_key = k

    if not v_key:
        for k in ds_dict.keys():
            if 'voltage' in k:
                v_key = k
                break

    if not i_key:
        for k in ds_dict.keys():
            if 'totalcurrent' in k or 'current' in k:
                i_key = k
                break

    if v_key and i_key:
        return {'v': ds_dict[v_key], 'i': np.abs(ds_dict[i_key])}

    return None

def style_svisual_plot(ax, title, xlabel="Anode Voltage (V)", ylabel="Total Current (A)", log_y=True):
    """Applies authentic Sentaurus Visual GUI styling."""
    ax.set_title(title, fontsize=12, fontweight='bold', pad=14, color='#0f172a')
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold', color='#1e293b')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold', color='#1e293b')
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.65, color='#94a3b8')
    if log_y:
        ax.set_yscale('log')
    ax.set_facecolor('#ffffff')
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['top'].set_color('#cbd5e1')
    ax.spines['right'].set_color('#cbd5e1')

RESULTS_DIR = "/home/ananthakrishnan/TCAD project/results"
OUT_DIR = "/home/ananthakrishnan/TCAD project/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 1. Silicon Photodiode Plot
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
si_dark = parse_df_ise_plt(os.path.join(RESULTS_DIR, "Si_dark_des.plt"))
si_opt = parse_df_ise_plt(os.path.join(RESULTS_DIR, "Si_opt_des.plt"))
si_full = parse_df_ise_plt(os.path.join(RESULTS_DIR, "Silicon_des.plt")) or parse_df_ise_plt(os.path.join(RESULTS_DIR, "Si_des.plt"))

if si_dark: ax.plot(si_dark['v'], si_dark['i'], color='#1e40af', linestyle='--', linewidth=2, label='Silicon (Dark Current)')
if si_opt: ax.plot(si_opt['v'], si_opt['i'], color='#dc2626', linestyle='-', linewidth=2.2, label='Silicon (Light 1 mW/cm²)')
elif si_full: ax.plot(si_full['v'], si_full['i'], color='#2563eb', linestyle='-', linewidth=2, label='Silicon I-V Characteristics')

style_svisual_plot(ax, "Sentaurus Visual — Silicon PIN Photodiode I-V & Transfer Characteristics")
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "svisual_Si_Photodiode_IV.png"))
plt.close()

# ---------------------------------------------------------
# 2. Germanium Photodiode Plot
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
ge_full = parse_df_ise_plt(os.path.join(RESULTS_DIR, "Germanium_des.plt")) or parse_df_ise_plt(os.path.join(RESULTS_DIR, "Ge_des.plt"))

if ge_full:
    ax.plot(ge_full['v'], ge_full['i'], color='#b91c1c', linestyle='-', linewidth=2.2, label='Germanium PIN Photodiode (Eg = 0.66 eV)')

style_svisual_plot(ax, "Sentaurus Visual — Germanium PIN Photodiode I-V & Transfer Characteristics")
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "svisual_Ge_Photodiode_IV.png"))
plt.close()

# ---------------------------------------------------------
# 3. GaAs Photodiode Plot
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
gaas_dark = parse_df_ise_plt(os.path.join(RESULTS_DIR, "GaAs_dark_des.plt"))
gaas_opt = parse_df_ise_plt(os.path.join(RESULTS_DIR, "GaAs_opt_des.plt"))
gaas_full = parse_df_ise_plt(os.path.join(RESULTS_DIR, "GaAs_des.plt"))

if gaas_dark: ax.plot(gaas_dark['v'], gaas_dark['i'], color='#334155', linestyle='--', linewidth=2, label='GaAs (Dark Current)')
if gaas_opt: ax.plot(gaas_opt['v'], gaas_opt['i'], color='#16a34a', linestyle='-', linewidth=2.2, label='GaAs (Light 1 mW/cm²)')
elif gaas_full: ax.plot(gaas_full['v'], gaas_full['i'], color='#15803d', linestyle='-', linewidth=2, label='GaAs I-V Characteristics')

style_svisual_plot(ax, "Sentaurus Visual — GaAs PIN Photodiode I-V & Transfer Characteristics")
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "svisual_GaAs_Photodiode_IV.png"))
plt.close()

# ---------------------------------------------------------
# 4. 4H-SiC Photodiode Plot
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
sic_dark = parse_df_ise_plt(os.path.join(RESULTS_DIR, "SiC4H_dark_des.plt"))
sic_opt = parse_df_ise_plt(os.path.join(RESULTS_DIR, "SiC4H_opt_des.plt"))
sic_full = parse_df_ise_plt(os.path.join(RESULTS_DIR, "SiC4H_des.plt"))

if sic_dark: ax.plot(sic_dark['v'], sic_dark['i'], color='#0284c7', linestyle='--', linewidth=2, label='4H-SiC (Dark Current)')
if sic_opt: ax.plot(sic_opt['v'], sic_opt['i'], color='#9333ea', linestyle='-', linewidth=2.2, label='4H-SiC (Light 1 mW/cm²)')
elif sic_full: ax.plot(sic_full['v'], sic_full['i'], color='#7e22ce', linestyle='-', linewidth=2, label='4H-SiC I-V Characteristics')

style_svisual_plot(ax, "Sentaurus Visual — 4H-SiC PIN Photodiode I-V & Transfer Characteristics")
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "svisual_SiC4H_Photodiode_IV.png"))
plt.close()

# ---------------------------------------------------------
# 5. GaAs LED Forward Bias I-V
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)
led_full = parse_df_ise_plt(os.path.join(RESULTS_DIR, "GaAs_LED_des.plt"))

if led_full:
    ax.plot(led_full['v'], led_full['i'], color='#d97706', linestyle='-', linewidth=2.4, label='GaAs LED (Forward Bias I-V)')

style_svisual_plot(ax, "Sentaurus Visual — GaAs LED Forward I-V & Emission Characteristics", log_y=False)
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "svisual_GaAs_LED_IV.png"))
plt.close()

# ---------------------------------------------------------
# 6. Combined Comparative Material Overlay Plot
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 6.0), dpi=300)

if si_full: ax.plot(si_full['v'], si_full['i'], color='#2563eb', linestyle='-', linewidth=2, label='Silicon (Eg = 1.12 eV)')
if ge_full: ax.plot(ge_full['v'], ge_full['i'], color='#dc2626', linestyle='-', linewidth=2, label='Germanium (Eg = 0.66 eV)')
if gaas_full: ax.plot(gaas_full['v'], gaas_full['i'], color='#16a34a', linestyle='-', linewidth=2, label='GaAs (Eg = 1.42 eV)')
if sic_full: ax.plot(sic_full['v'], sic_full['i'], color='#9333ea', linestyle='-', linewidth=2, label='4H-SiC (Eg = 3.26 eV)')

style_svisual_plot(ax, "Sentaurus Visual — Comparative I-V Overlay (Si vs Ge vs GaAs vs 4H-SiC)")
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "svisual_Photodiode_Combined_IV_Overlay.png"))
plt.close()

print("ALL_SVISUAL_PLOTS_GENERATED_SUCCESSFULLY")
