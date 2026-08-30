import os
import time
import subprocess
import shutil

VM_NAME = "Sentaurus TCAD RHEL6"
USERNAME = "sentaurus"
PASSWORD = "123456"

MATERIALS = [
    ("Si", "svisual_full_ui_Si_Photodiode.png"),
    ("Ge", "svisual_full_ui_Ge_Photodiode.png"),
    ("GaAs", "svisual_full_ui_GaAs_Photodiode.png"),
    ("SiC4H", "svisual_full_ui_SiC4H_Photodiode.png"),
    ("GaAs_LED", "svisual_full_ui_GaAs_LED.png"),
    ("Combined", "svisual_full_ui_Combined_Overlay.png")
]

SHARED_DIR = "/home/ananthakrishnan/Documents/swb/screenshots"
OUT_DIR = "/home/ananthakrishnan/TCAD project/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

for mat_code, out_filename in MATERIALS:
    print(f"\n[+] Launching SVisual and capturing in-guest UI screenshot for {mat_code}...")
    
    cmd_launch = [
        "VBoxManage", "guestcontrol", VM_NAME, "run",
        "--username", USERNAME, "--password", PASSWORD,
        "--exe", "/bin/bash", "--",
        "/media/sf_swb/launch_material_ui.sh", mat_code
    ]
    res = subprocess.run(cmd_launch, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for SVisual GUI rendering and xwd conversion inside VM
    time.sleep(8)
    
    src_png = os.path.join(SHARED_DIR, f"svisual_full_ui_{mat_code}.png")
    dest_png = os.path.join(OUT_DIR, out_filename)
    
    if os.path.exists(src_png):
        shutil.copy(src_png, dest_png)
        size_kb = os.path.getsize(dest_png) / 1024
        print(f"    SUCCESS: Captured & saved {out_filename} ({size_kb:.1f} KB)")
    else:
        print(f"    WARNING: Could not find {src_png}")

print("\n[+] ALL 6 MATERIAL FULL UI SCREENSHOTS SUCCESSFULLY CAPTURED!")
