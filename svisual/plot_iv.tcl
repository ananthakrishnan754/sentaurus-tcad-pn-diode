# ============================================================
# FILE:    svisual/plot_iv.tcl
# TOOL:    Sentaurus Visual (SVisual)
# PURPOSE: Load the SDevice output (.plt file) and generate
#          publication-quality I-V curve plots.
#
# HOW TO RUN:
#   In SWB: add SVisual node, point it to this script.
#   OR: open SVisual GUI → File → Execute Script → select this file
#
# INPUT:   MaterialDiode_des.plt  (from SDevice)
# OUTPUT:  iv_forward.png, iv_reverse.png, iv_log.png
# ============================================================


# ============================================================
# SECTION 1: LOAD THE SDEVICE OUTPUT DATA
# The .plt file is a text table: first column = voltage,
# remaining columns = currents at each electrode.
# SVisual reads it and stores it in a "dataset" object.
# ============================================================

# Load the current-voltage data file
set plt_file "MaterialDiode_des.plt"

# sv::open opens a file and returns a dataset handle
set dataset [sv::open $plt_file]

# WHAT IS IN THE .plt FILE?
# The file has columns named like:
#   "Anode OuterVoltage"      → voltage applied at Anode (V)
#   "Anode TotalCurrent"      → current at Anode (A)
#   "Cathode TotalCurrent"    → current at Cathode (A)
# These exact column names are what SVisual uses to extract data.


# ============================================================
# SECTION 2: EXTRACT DATA COLUMNS
# We pull out the voltage and current arrays from the dataset.
# ============================================================

# Extract voltage column (this is the x-axis for all plots)
set voltage [sv::get_data $dataset "Anode OuterVoltage"]

# Extract Anode current (positive = current INTO the diode)
set current [sv::get_data $dataset "Anode TotalCurrent"]

# NOTE ON SIGN CONVENTION:
# In SDevice, current is defined as flowing INTO the contact.
# So at forward bias, the Anode current is POSITIVE (current
# flowing in = diode conducting). At reverse bias, Anode
# current is NEGATIVE (very small leakage, flowing out).
# When you plot, take absolute value for log scale.


# ============================================================
# SECTION 3: FORWARD I-V CURVE (LINEAR SCALE)
# Plot current vs voltage for Vanode = 0 to +1.0 V
# ============================================================

# Create a new plot window
sv::create_plot -name "ForwardIV_Linear"

# Set the plot title and axis labels
sv::set_plot_title "Forward I-V Characteristic — Silicon PN Diode (Linear)"
sv::set_x_label "Anode Voltage (V)"
sv::set_y_label "Current (A)"

# Add the I-V curve to the plot
# x-axis = voltage, y-axis = current
sv::add_curve $dataset \
    -x "Anode OuterVoltage" \
    -y "Anode TotalCurrent" \
    -color red \
    -legend "Si PN Diode — Forward I-V"

# Set x-axis range to show only forward bias
sv::set_x_range 0.0 1.0

# Save the plot to file
sv::export_image "iv_forward.png" -format png -resolution 300

# WHAT YOU SHOULD SEE:
# A classic exponential I-V curve (J-shaped).
# Current is nearly zero for V < 0.5 V (below threshold).
# Current rises sharply above 0.5 V (turn-on voltage for Si).
# At V = 0.7 V, current is roughly in the mA range (for 1 µm² area).
# The exact turn-on voltage differs between materials:
#   Si  → ~0.6-0.7 V  (Eg = 1.12 eV)
#   Ge  → ~0.3-0.4 V  (Eg = 0.66 eV)
#   GaAs→ ~1.2-1.4 V  (Eg = 1.42 eV)
#   SiC → ~2.5-3.0 V  (Eg = 3.26 eV)


# ============================================================
# SECTION 4: FORWARD I-V CURVE (LOG SCALE)
# Plotting on a logarithmic current axis reveals the ideality
# factor (the slope in log scale tells you the quality of
# the diode — ideal diode has ideality factor = 1).
# ============================================================

sv::create_plot -name "ForwardIV_Log"
sv::set_plot_title "Forward I-V Characteristic — Silicon PN Diode (Log Scale)"
sv::set_x_label "Anode Voltage (V)"
sv::set_y_label "Current (A) — Log Scale"

sv::add_curve $dataset \
    -x "Anode OuterVoltage" \
    -y "Anode TotalCurrent" \
    -abs                    \
    -log_y                  \
    -color blue             \
    -legend "Si PN Diode — Log I-V"

# -abs: takes absolute value of current before log
# -log_y: makes the y-axis logarithmic

sv::set_x_range 0.0 1.0
sv::set_y_range 1e-18 1e-1   ; # from 10^-18 A to 100 mA

sv::export_image "iv_log.png" -format png -resolution 300

# WHAT YOU SHOULD SEE (LOG SCALE):
# A straight line in the exponential region (0.3 to 0.6 V).
# The slope of this line = q / (n * kT) where n = ideality factor.
# For an ideal diode: n = 1, slope = 40 V^-1 at 300K.
# For SRH-dominated recombination: n = 2 (shallower slope).
# You can extract n from: n = q / (kT * d(lnI)/dV)


# ============================================================
# SECTION 5: REVERSE I-V CURVE
# Plot current vs voltage for Vanode = 0 to -20 V
# ============================================================

sv::create_plot -name "ReverseIV"
sv::set_plot_title "Reverse I-V Characteristic — Silicon PN Diode"
sv::set_x_label "Anode Voltage (V)"
sv::set_y_label "|Current| (A) — Log Scale"

sv::add_curve $dataset \
    -x "Anode OuterVoltage" \
    -y "Anode TotalCurrent" \
    -abs                    \
    -log_y                  \
    -color darkgreen        \
    -legend "Si PN Diode — Reverse I-V"

sv::set_x_range -20.0 0.0
sv::set_y_range 1e-20 1e-3

sv::export_image "iv_reverse.png" -format png -resolution 300

# WHAT YOU SHOULD SEE (REVERSE SCALE):
# A nearly flat line (leakage current plateau) from 0 to ~-15 V.
# This is the reverse saturation current I0.
# Near the breakdown voltage, current shoots up suddenly.
# For Si at these doping levels, Vbr ≈ -30 to -50 V.
# We only swept to -20 V, so you may not see full breakdown.
# COMPARE ACROSS MATERIALS:
# Ge will have HIGHER I0 (more thermal generation, smaller Eg)
# GaAs will have LOWER I0 (larger Eg, less thermal generation)
# SiC will have the LOWEST I0 (largest Eg, Vbr > 100 V)

# ============================================================
# END OF PLOT_IV.TCL
# ============================================================
