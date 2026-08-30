import os
import time
import subprocess
from PIL import Image

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
    print(f"\n[+] Capturing GUI desktop screenshot for {mat_code} -> {out_filename}...")
    
    # 1. Run in-guest launcher
    cmd_launch = [
        "VBoxManage", "guestcontrol", VM_NAME, "run",
        "--username", USERNAME, "--password", PASSWORD,
        "--exe", "/bin/bash", "--",
        "/media/sf_swb/launch_material_ui.sh", mat_code
    ]
    res = subprocess.run(cmd_launch, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"    Launcher output: {res.stdout.decode()[-150:].strip()}")
    
    # 2. Check output PNG or XWD file in shared folder
    png_path = os.path.join(SHARED_DIR, f"svisual_full_ui_{mat_code}.png")
    xwd_path = os.path.join(SHARED_DIR, f"svisual_full_ui_{mat_code}.xwd")
    dest_path = os.path.join(OUT_DIR, out_filename)
    
    if os.path.exists(png_path) and os.path.getsize(png_path) > 1000:
        img = Image.open(png_path)
        img.save(dest_path)
        print(f"    Saved PNG from shared folder: {dest_path} ({os.path.getsize(dest_path)/1024:.1f} KB, dimensions: {img.size})")
    elif os.path.exists(xwd_path):
        try:
            img = Image.open(xwd_path)
            img.save(dest_path)
            print(f"    Converted XWD to PNG: {dest_path} ({os.path.getsize(dest_path)/1024:.1f} KB, dimensions: {img.size})")
        except Exception as e:
            print(f"    Error converting XWD: {e}")
    else:
        print(f"    Warning: No output file found for {mat_code}")

print("\n[+] BATCH XWD GUI CAPTURE COMPLETE!")
