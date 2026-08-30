import subprocess
import time
import os

PLOTS = [
    ("plot_01_silicon.tcl", "svisual_full_ui_Silicon_Photodiode.png"),
    ("plot_02_germanium.tcl", "svisual_full_ui_Germanium_Photodiode.png"),
    ("plot_03_gaas.tcl", "svisual_full_ui_GaAs_Photodiode.png"),
    ("plot_04_sic4h.tcl", "svisual_full_ui_SiC4H_Photodiode.png"),
    ("plot_05_gaas_led.tcl", "svisual_full_ui_GaAs_LED.png"),
    ("plot_06_combined.tcl", "svisual_full_ui_Combined_Overlay.png")
]

OUT_DIR = "/home/ananthakrishnan/TCAD project/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

def run_vbox_cmd(cmd_str):
    full_cmd = [
        "VBoxManage", "guestcontrol", "Sentaurus TCAD RHEL6", "run",
        "--username", "sentaurus", "--password", "123456",
        "--exe", "/bin/bash", "--", "-c", cmd_str
    ]
    res = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout, res.stderr

print("Starting sequential single-plot Sentaurus Visual GUI captures...")

for tcl_script, output_filename in PLOTS:
    print(f"\n---> Processing {tcl_script} -> {output_filename}...")
    
    # 1. Kill any existing svisual
    run_vbox_cmd("pkill -9 svisual 2>/dev/null || true")
    time.sleep(1)

    # 2. Launch SVisual interactive GUI for this specific TCL script
    launch_cmd = (
        "export STROOT=/home/eda/sentaurus-2017.09/sentaurus/N_2017.09; "
        "export PATH=$STROOT/bin:$PATH; export SNPS_HOME=/home/eda; export STDB=$HOME/STDB; "
        "export SNPSLMD_LICENSE_FILE=27000@localhost.localdomain; export LM_LICENSE_FILE=27000@localhost.localdomain; "
        "export DISPLAY=:0; export XAUTHORITY=/home/sentaurus/.Xauthority; "
        f"nohup svisual -e /media/sf_swb/{tcl_script} > /tmp/{tcl_script}.log 2>&1 &"
    )
    run_vbox_cmd(launch_cmd)
    
    # Wait for SVisual GUI to open and render plot window
    print("Waiting 5s for SVisual GUI window to render...")
    time.sleep(5)
    
    # 3. Capture full UI screenshot
    out_path_guest = f"/media/sf_swb/screenshots/{output_filename}"
    out_xwd_guest = f"/media/sf_swb/screenshots/{output_filename}.xwd"
    
    snap_cmd = (
        "export DISPLAY=:0; export XAUTHORITY=/home/sentaurus/.Xauthority; "
        f"xwd -root -out {out_xwd_guest} && convert {out_xwd_guest} {out_path_guest} && rm -f {out_xwd_guest}"
    )
    stdout, stderr = run_vbox_cmd(snap_cmd)
    print(f"Captured: {output_filename}")

    # Clean up svisual instance
    run_vbox_cmd("pkill -9 svisual 2>/dev/null || true")
    time.sleep(1)

print("\nALL 6 INDIVIDUAL & COMBINED FULL-UI PLOTS CAPTURED SUCCESSFULLY!")
