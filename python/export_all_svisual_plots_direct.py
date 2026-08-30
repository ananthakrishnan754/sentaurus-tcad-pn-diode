import os
import subprocess

VM_NAME = "Sentaurus TCAD RHEL6"
USERNAME = "sentaurus"
PASSWORD = "123456"

SHARED_DIR = "/home/ananthakrishnan/Documents/swb/screenshots"
OUT_DIR = "/home/ananthakrishnan/TCAD project/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

# Master TCL script to export crisp 1920x1080 SVisual plots directly
tcl_script = """
export STROOT=/home/eda/sentaurus-2017.09/sentaurus/N_2017.09
export PATH=$STROOT/bin:$PATH
export SNPS_HOME=/home/eda
export STDB=$HOME/STDB
export SNPSLMD_LICENSE_FILE=27000@localhost.localdomain
export LM_LICENSE_FILE=27000@localhost.localdomain
export DISPLAY=:0

cd /media/sf_swb/results

# 1. Silicon PIN Photodiode
set p1 [create_plot -1d]
select_plots $p1
set_plot_prop -plot $p1 -title "Sentaurus Visual - Silicon PIN Photodiode I-V Characteristics"
if {[file exists "Si_dark_des.plt"]} { set ds [load_file "Si_dark_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "Silicon Photodiode (Dark)" }
if {[file exists "Si_opt_des.plt"]} { set ds [load_file "Si_opt_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "Silicon Photodiode (Optical 1mW/cm2)" }
set_axis_prop -plot $p1 -axis y -type log
set_curve_prop -plot $p1 -all_curves -line_width 3
set_axis_prop -plot $p1 -axis x -title "Anode Voltage (V)" -title_font_size 16 -label_font_size 14
set_axis_prop -plot $p1 -axis y -title "Anode Current (A)" -title_font_size 16 -label_font_size 14
export_view "/media/sf_swb/screenshots/svisual_export_Si.png" -format png -width 1920 -height 1080 -resolution 300
remove_plots $p1

# 2. Germanium PIN Photodiode
set p2 [create_plot -1d]
select_plots $p2
set_plot_prop -plot $p2 -title "Sentaurus Visual - Germanium PIN Photodiode I-V Characteristics"
if {[file exists "Germanium_des.plt"]} { set ds [load_file "Germanium_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "Germanium Photodiode" }
set_axis_prop -plot $p2 -axis y -type log
set_curve_prop -plot $p2 -all_curves -line_width 3
set_axis_prop -plot $p2 -axis x -title "Anode Voltage (V)" -title_font_size 16 -label_font_size 14
set_axis_prop -plot $p2 -axis y -title "Anode Current (A)" -title_font_size 16 -label_font_size 14
export_view "/media/sf_swb/screenshots/svisual_export_Ge.png" -format png -width 1920 -height 1080 -resolution 300
remove_plots $p2

# 3. GaAs PIN Photodiode
set p3 [create_plot -1d]
select_plots $p3
set_plot_prop -plot $p3 -title "Sentaurus Visual - GaAs PIN Photodiode I-V Characteristics"
if {[file exists "GaAs_dark_des.plt"]} { set ds [load_file "GaAs_dark_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "GaAs Photodiode (Dark)" }
if {[file exists "GaAs_opt_des.plt"]} { set ds [load_file "GaAs_opt_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "GaAs Photodiode (Optical)" }
set_axis_prop -plot $p3 -axis y -type log
set_curve_prop -plot $p3 -all_curves -line_width 3
set_axis_prop -plot $p3 -axis x -title "Anode Voltage (V)" -title_font_size 16 -label_font_size 14
set_axis_prop -plot $p3 -axis y -title "Anode Current (A)" -title_font_size 16 -label_font_size 14
export_view "/media/sf_swb/screenshots/svisual_export_GaAs.png" -format png -width 1920 -height 1080 -resolution 300
remove_plots $p3

# 4. 4H-SiC PIN Photodiode
set p4 [create_plot -1d]
select_plots $p4
set_plot_prop -plot $p4 -title "Sentaurus Visual - 4H-SiC PIN Photodiode I-V Characteristics"
if {[file exists "SiC4H_dark_des.plt"]} { set ds [load_file "SiC4H_dark_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "4H-SiC Photodiode (Dark)" }
if {[file exists "SiC4H_opt_des.plt"]} { set ds [load_file "SiC4H_opt_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "4H-SiC Photodiode (Optical)" }
set_axis_prop -plot $p4 -axis y -type log
set_curve_prop -plot $p4 -all_curves -line_width 3
set_axis_prop -plot $p4 -axis x -title "Anode Voltage (V)" -title_font_size 16 -label_font_size 14
set_axis_prop -plot $p4 -axis y -title "Anode Current (A)" -title_font_size 16 -label_font_size 14
export_view "/media/sf_swb/screenshots/svisual_export_SiC4H.png" -format png -width 1920 -height 1080 -resolution 300
remove_plots $p4

# 5. GaAs LED Forward I-V
set p5 [create_plot -1d]
select_plots $p5
set_plot_prop -plot $p5 -title "Sentaurus Visual - GaAs LED Forward I-V Characteristics"
if {[file exists "GaAs_LED_des.plt"]} { set ds [load_file "GaAs_LED_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "GaAs LED Emission Current" }
set_axis_prop -plot $p5 -axis y -type linear
set_curve_prop -plot $p5 -all_curves -line_width 3
set_axis_prop -plot $p5 -axis x -title "Forward Voltage (V)" -title_font_size 16 -label_font_size 14
set_axis_prop -plot $p5 -axis y -title "Diode Current (A)" -title_font_size 16 -label_font_size 14
export_view "/media/sf_swb/screenshots/svisual_export_GaAs_LED.png" -format png -width 1920 -height 1080 -resolution 300
remove_plots $p5

# 6. Combined Comparative Overlay
set p6 [create_plot -1d]
select_plots $p6
set_plot_prop -plot $p6 -title "Sentaurus Visual - Comparative Photodiode Performance Overlay"
if {[file exists "Silicon_des.plt"]} { set ds [load_file "Silicon_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "Silicon (Eg = 1.12 eV)" }
if {[file exists "Germanium_des.plt"]} { set ds [load_file "Germanium_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "Germanium (Eg = 0.66 eV)" }
if {[file exists "GaAs_des.plt"]} { set ds [load_file "GaAs_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "GaAs (Eg = 1.42 eV)" }
if {[file exists "SiC4H_des.plt"]} { set ds [load_file "SiC4H_des.plt"]; add_to_plot -dataset $ds -x "anode OuterVoltage" -y "anode TotalCurrent" -curve_name "4H-SiC (Eg = 3.26 eV)" }
set_axis_prop -plot $p6 -axis y -type log
set_curve_prop -plot $p6 -all_curves -line_width 3
set_axis_prop -plot $p6 -axis x -title "Anode Voltage (V)" -title_font_size 16 -label_font_size 14
set_axis_prop -plot $p6 -axis y -title "Anode Current (A)" -title_font_size 16 -label_font_size 14
export_view "/media/sf_swb/screenshots/svisual_export_Combined.png" -format png -width 1920 -height 1080 -resolution 300
remove_plots $p6

exit
"""

# Save TCL script inside VM shared directory
with open("/home/ananthakrishnan/Documents/swb/export_all_direct.tcl", "w") as f:
    f.write(tcl_script)

print("[+] Executing Sentaurus Visual in guest VM...")
cmd_exec = [
    "VBoxManage", "guestcontrol", VM_NAME, "run",
    "--username", USERNAME, "--password", PASSWORD,
    "--exe", "/bin/bash", "--",
    "-c", "export STROOT=/home/eda/sentaurus-2017.09/sentaurus/N_2017.09; export PATH=$STROOT/bin:$PATH; export SNPS_HOME=/home/eda; export STDB=$HOME/STDB; export SNPSLMD_LICENSE_FILE=27000@localhost.localdomain; export LM_LICENSE_FILE=27000@localhost.localdomain; export DISPLAY=:0; svisual -b /media/sf_swb/export_all_direct.tcl"
]

res = subprocess.run(cmd_exec, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("SVisual execution returned:", res.returncode)

# Check exported files
mapping = [
    ("svisual_export_Si.png", "svisual_Si_Photodiode_IV.png"),
    ("svisual_export_Ge.png", "svisual_Ge_Photodiode_IV.png"),
    ("svisual_export_GaAs.png", "svisual_GaAs_Photodiode_IV.png"),
    ("svisual_export_SiC4H.png", "svisual_SiC4H_Photodiode_IV.png"),
    ("svisual_export_GaAs_LED.png", "svisual_GaAs_LED_IV.png"),
    ("svisual_export_Combined.png", "svisual_Photodiode_Combined_IV_Overlay.png")
]

for src_name, dest_name in mapping:
    src_path = os.path.join(SHARED_DIR, src_name)
    dest_path = os.path.join(OUT_DIR, dest_name)
    if os.path.exists(src_path):
        import shutil
        shutil.copy(src_path, dest_path)
        size_kb = os.path.getsize(dest_path) / 1024
        print(f"    [SUCCESS] Exported {dest_name} ({size_kb:.1f} KB)")
    else:
        print(f"    [WARNING] Missing {src_path}")

print("\n[+] SVISUAL DIRECT HD PLOT EXPORT COMPLETE!")
