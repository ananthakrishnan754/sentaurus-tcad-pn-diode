# ============================================================
# FILE:    svisual/plot_fields.tcl
# TOOL:    Sentaurus Visual (SVisual)
# PURPOSE: Load SDevice 2D output (.tdr files) and generate:
#          - Electric field profile across the junction
#          - Band diagram (Ec, Ev, Efn, Efp vs position)
#          - Carrier concentration profile
#          - Potential profile
#          - Depletion region visualization
#
# INPUT:   MaterialDiode_equil_des.tdr  (equilibrium state)
#          MaterialDiode_fwd_des.tdr    (forward bias state)
#          MaterialDiode_rev_des.tdr    (reverse bias state)
# OUTPUT:  band_diagram.png, efield.png, carriers.png, potential.png
# ============================================================


# ============================================================
# SECTION 1: LOAD 2D DATASETS
# The .tdr files contain full 2D spatial data — every quantity
# (E-field, potential, carrier density) at every mesh node.
# We cut a 1D slice through the middle of the device (x = 0.5 µm)
# to get line plots that are easier to interpret.
# ============================================================

# Load equilibrium state (0 V, no current)
set equil_data [sv::open "MaterialDiode_equil_des.tdr"]

# Load forward bias state (at some mid-bias, e.g., 0.6 V)
# In SDevice we saved the fwd file at the end of the sweep
set fwd_data [sv::open "MaterialDiode_fwd_des.tdr"]

# Load reverse bias state (at some reverse voltage, e.g., -5 V)
set rev_data [sv::open "MaterialDiode_rev_des.tdr"]

# Define the 1D cutline: vertical slice at x = 0.5 µm
# This passes through the center of the device from top to bottom
# y goes from 0 (Anode/top) to 1.0 µm (Cathode/bottom)
set cutline_x 0.5


# ============================================================
# SECTION 2: BAND DIAGRAM
# This is one of the most important plots in device physics.
# It shows:
#   Ec = conduction band edge (eV) vs position
#   Ev = valence band edge (eV) vs position
#   Efn = electron quasi-Fermi level (eV) vs position
#   Efp = hole quasi-Fermi level (eV) vs position
#
# At equilibrium: Efn = Efp = single flat Fermi level
# Under bias: Efn and Efp split — the splitting = applied voltage
# ============================================================

sv::create_plot -name "BandDiagram"
sv::set_plot_title "Band Diagram — Silicon PN Diode (Equilibrium)"
sv::set_x_label "Depth y (µm)"
sv::set_y_label "Energy (eV)"

# Plot Ec vs y at x = 0.5 µm (equilibrium)
sv::add_curve_1d $equil_data \
    -quantity "ConductionBand" \
    -x $cutline_x \
    -color blue \
    -legend "Ec (Conduction Band)"

# Plot Ev vs y at x = 0.5 µm (equilibrium)
sv::add_curve_1d $equil_data \
    -quantity "ValenceBand" \
    -x $cutline_x \
    -color red \
    -legend "Ev (Valence Band)"

# Plot Fermi level (at equilibrium Efn = Efp = Ef)
sv::add_curve_1d $equil_data \
    -quantity "eQuasiFermi" \
    -x $cutline_x \
    -color black \
    -style dashed \
    -legend "Ef (Fermi Level)"

sv::export_image "band_diagram_equil.png" -format png -resolution 300

# WHAT YOU SHOULD SEE:
# In the P-region (y = 0 to 0.5 µm):
#   Ec and Ev are at higher energy (bands are "up")
# In the N-region (y = 0.5 to 1.0 µm):
#   Ec and Ev are at lower energy (bands are "down")
# The transition happens at the junction (y = 0.5 µm):
#   This curved region is the depletion region.
#   The slope of Ec/Ev in this region = -q × E-field
# The Fermi level (dashed black) is flat and horizontal.
#   A flat Fermi level = equilibrium, no net current flows.
# The built-in voltage Vbi = Ec(P-side) - Ec(N-side)
#   For Si with Na=1e17, Nd=1e16: Vbi ≈ 0.76 V


# Now add forward bias band diagram to compare
sv::create_plot -name "BandDiagram_Bias"
sv::set_plot_title "Band Diagram — Si PN Diode (Equil vs Forward 0.6V)"
sv::set_x_label "Depth y (µm)"
sv::set_y_label "Energy (eV)"

sv::add_curve_1d $equil_data \
    -quantity "ConductionBand" \
    -x $cutline_x \
    -color blue \
    -legend "Ec — Equilibrium"

sv::add_curve_1d $fwd_data \
    -quantity "ConductionBand" \
    -x $cutline_x \
    -color cyan \
    -legend "Ec — Forward Bias 0.6V"

sv::add_curve_1d $equil_data \
    -quantity "ValenceBand" \
    -x $cutline_x \
    -color red \
    -legend "Ev — Equilibrium"

sv::add_curve_1d $fwd_data \
    -quantity "ValenceBand" \
    -x $cutline_x \
    -color orange \
    -legend "Ev — Forward Bias 0.6V"

sv::export_image "band_diagram_compare.png" -format png -resolution 300

# WHAT YOU SHOULD SEE (FORWARD BIAS):
# The band bending at the junction REDUCES compared to equilibrium.
# The reduction = applied voltage (0.6 V reduces barrier by 0.6 V).
# Efn and Efp are no longer the same — they SPLIT by 0.6 V.
# This split drives minority carrier injection across the junction.


# ============================================================
# SECTION 3: ELECTRIC FIELD PROFILE
# The electric field peaks at the PN junction and decays
# on both sides. The area under the E-field curve = Vbi.
# Under reverse bias, the peak field increases.
# Breakdown occurs when E-field exceeds ~3e5 V/cm (for Si).
# ============================================================

sv::create_plot -name "ElectricField"
sv::set_plot_title "Electric Field Profile — Silicon PN Diode"
sv::set_x_label "Depth y (µm)"
sv::set_y_label "Electric Field (V/cm)"

# Y-component of E-field (vertical direction = junction direction)
sv::add_curve_1d $equil_data \
    -quantity "ElectricField-Y" \
    -x $cutline_x \
    -abs \
    -color navy \
    -legend "E-field — Equilibrium"

sv::add_curve_1d $rev_data \
    -quantity "ElectricField-Y" \
    -x $cutline_x \
    -abs \
    -color purple \
    -legend "E-field — Reverse Bias -5V"

sv::export_image "efield.png" -format png -resolution 300

# WHAT YOU SHOULD SEE:
# A triangular peak centered at y = 0.5 µm (the junction).
# At equilibrium: peak ~1e4 to 5e4 V/cm for Si at these doping levels.
# At -5 V reverse: peak is higher and the depletion region wider.
# The field is zero in the P and N bulk regions (flat bands).
# The width of the triangle = depletion width.
#   Depletion width W = sqrt(2 * eps * Vbi / q * (Na + Nd)/(Na * Nd))
#   For Si: W ≈ 0.3 to 0.4 µm at equilibrium


# ============================================================
# SECTION 4: CARRIER CONCENTRATION PROFILE
# Shows where electrons and holes are located in the device.
# Inside the depletion region: very few carriers (depleted).
# In the bulk P-region: many holes, few electrons.
# In the bulk N-region: many electrons, few holes.
# ============================================================

sv::create_plot -name "Carriers"
sv::set_plot_title "Carrier Concentration — Silicon PN Diode (Equilibrium)"
sv::set_x_label "Depth y (µm)"
sv::set_y_label "Carrier Concentration (cm⁻³) — Log Scale"

# Electron concentration
sv::add_curve_1d $equil_data \
    -quantity "eDensity" \
    -x $cutline_x \
    -log_y \
    -color blue \
    -legend "Electrons n (cm⁻³)"

# Hole concentration
sv::add_curve_1d $equil_data \
    -quantity "hDensity" \
    -x $cutline_x \
    -log_y \
    -color red \
    -legend "Holes p (cm⁻³)"

# Net doping for reference (to show where junction is)
sv::add_curve_1d $equil_data \
    -quantity "Doping" \
    -x $cutline_x \
    -abs \
    -log_y \
    -color gray \
    -style dashed \
    -legend "|Net Doping| (cm⁻³)"

sv::set_y_range 1e5 1e18
sv::export_image "carriers.png" -format png -resolution 300

# WHAT YOU SHOULD SEE:
# In P-region (y = 0 to ~0.35 µm):
#   Holes p ≈ 1e17 cm^-3 (majority, matches Na)
#   Electrons n ≈ 1e3 cm^-3 (minority, from mass action law: n = ni²/p)
# In N-region (y = ~0.65 to 1.0 µm):
#   Electrons n ≈ 1e16 cm^-3 (majority, matches Nd)
#   Holes p ≈ 1e4 cm^-3 (minority: p = ni²/n)
# In the depletion region (y = 0.35 to 0.65 µm):
#   Both n and p drop dramatically (10 to 100x below ni)
#   This is the space charge region.
# The doping curve (gray dashed) flips sign at y = 0.5 µm (junction).


# ============================================================
# SECTION 5: ELECTROSTATIC POTENTIAL PROFILE
# The electrostatic potential φ(y) shows the built-in voltage
# across the junction and how it changes with applied bias.
# ============================================================

sv::create_plot -name "Potential"
sv::set_plot_title "Electrostatic Potential — Silicon PN Diode"
sv::set_x_label "Depth y (µm)"
sv::set_y_label "Potential φ (V)"

sv::add_curve_1d $equil_data \
    -quantity "ElectrostaticPotential" \
    -x $cutline_x \
    -color black \
    -legend "φ — Equilibrium"

sv::add_curve_1d $fwd_data \
    -quantity "ElectrostaticPotential" \
    -x $cutline_x \
    -color green \
    -legend "φ — Forward Bias 0.6V"

sv::add_curve_1d $rev_data \
    -quantity "ElectrostaticPotential" \
    -x $cutline_x \
    -color red \
    -legend "φ — Reverse Bias -5V"

sv::export_image "potential.png" -format png -resolution 300

# WHAT YOU SHOULD SEE:
# At equilibrium:
#   φ steps up from cathode side to anode side by Vbi (~0.76V for Si)
#   The step is centered at the junction (y = 0.5 µm)
#   In the depletion region: steep S-shaped transition
#   In the bulk: flat (no field = constant potential)
# At forward bias (+0.6V):
#   The step is SMALLER (barrier reduced by 0.6V)
# At reverse bias (-5V):
#   The step is LARGER (barrier increased by 5V)
#   And the step spans a WIDER region (wider depletion)


# ============================================================
# SECTION 6: RECOMBINATION RATES
# Shows where carriers recombine and by which mechanism.
# ============================================================

sv::create_plot -name "Recombination"
sv::set_plot_title "Recombination Rates — Silicon PN Diode (Forward 0.6V)"
sv::set_x_label "Depth y (µm)"
sv::set_y_label "Recombination Rate (cm⁻³ s⁻¹) — Log Scale"

sv::add_curve_1d $fwd_data \
    -quantity "SRHRecombination" \
    -x $cutline_x \
    -abs \
    -log_y \
    -color blue \
    -legend "SRH Recombination"

sv::add_curve_1d $fwd_data \
    -quantity "AugerRecombination" \
    -x $cutline_x \
    -abs \
    -log_y \
    -color red \
    -legend "Auger Recombination"

sv::add_curve_1d $fwd_data \
    -quantity "RadiativeRecombination" \
    -x $cutline_x \
    -abs \
    -log_y \
    -color green \
    -legend "Radiative Recombination"

sv::export_image "recombination.png" -format png -resolution 300

# WHAT YOU SHOULD SEE (for Silicon):
# SRH >> Auger >> Radiative everywhere in Si (indirect bandgap)
# SRH peaks inside the depletion region and near contacts
# Auger peaks in the heavily doped P-region (high carrier density)
# Radiative is nearly negligible for Si (indirect gap)
# FOR GaAs: Radiative will be much larger than SRH!
# FOR SiC: SRH will dominate but rates are very low (wide gap)

# ============================================================
# END OF PLOT_FIELDS.TCL
# ============================================================
