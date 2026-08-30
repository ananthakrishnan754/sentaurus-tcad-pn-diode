import os
import time
import subprocess

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

OUT_DIR = "/home/ananthakrishnan/TCAD project/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)

for mat_code, out_filename in MATERIALS:
    print(f"\n[+] Processing full UI screenshot for {mat_code} ({out_filename})...")
    
    # 1. Launch SVisual GUI inside VM
    cmd_launch = [
        "VBoxManage", "guestcontrol", VM_NAME, "run",
        "--username", USERNAME, "--password", PASSWORD,
        "--exe", "/bin/bash", "--",
        "/media/sf_swb/launch_material_ui.sh", mat_code
    ]
    subprocess.run(cmd_launch, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 2. Wait for GUI window to render
    time.sleep(7)
    
    # 3. Capture VM Framebuffer UI screenshot
    out_path = os.path.join(OUT_DIR, out_filename)
    cmd_cap = [
        "VBoxManage", "controlvm", VM_NAME, "screenshotpng", out_path
    ]
    res = subprocess.run(cmd_cap, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if res.returncode == 0 and os.path.exists(out_path):
        size_kb = os.path.getsize(out_path) / 1024
        print(f"    Successfully captured: {out_filename} ({size_kb:.1f} KB)")
    else:
        print(f"    Failed to capture {out_filename}: {res.stderr.decode()}")

print("\n[+] ALL FULL UI SCREENSHOTS CAPTURED SUCCESSFULLY!")
