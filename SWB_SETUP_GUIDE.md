# ============================================================
# FILE:    SWB_SETUP_GUIDE.md
# PURPOSE: Step-by-step instructions for setting up the
#          Sentaurus Workbench (SWB) project on the college PC.
#
# The SWB project file (.swb) is a GUI-created binary —
# it cannot be written by hand. These instructions tell you
# exactly what to click and type in the SWB GUI.
#
# DO THIS FIRST THING WHEN YOU SIT AT THE COLLEGE PC.
# ============================================================

# Sentaurus Workbench (SWB) Setup Guide

## Step 0 — Pull the Latest Code

Open a terminal on the college PC and run:

```bash
# If you haven't cloned yet (first time):
git clone https://github.com/ananthakrishnan754/sentaurus-tcad-pn-diode.git

# If you already have it cloned:
cd sentaurus-tcad-pn-diode
git pull
```

---

## Step 1 — Open Sentaurus Workbench

Launch SWB from the application menu or by typing in terminal:
```bash
swb &
```

The SWB window shows a **spreadsheet-like grid**:
- **Columns** = simulation runs (one per material)
- **Rows** = tools in the pipeline (SDE → SMesh → SDevice → SVisual)

---

## Step 2 — Create a New Project

1. In SWB: **File → New Project**
2. Set the project directory to your cloned folder:
   `/path/to/sentaurus-tcad-pn-diode/`
3. Name the project: `MaterialDiode`
4. Click **OK**

---

## Step 3 — Add the Tool Nodes (Rows)

You need to add 4 tools to the flow. Each tool becomes one row.

### Add SDE Node (Row 1):
1. Right-click in the flow area → **Add → Sentaurus Device Editor**
2. A new row labelled "sde" appears
3. Right-click the SDE node → **Edit Input File**
4. Browse to: `sde/sde_dvs.cmd`
5. Click **OK**

### Add SMesh Node (Row 2):
1. Right-click below SDE → **Add → Sentaurus Mesh**
2. A "smesh" row appears below SDE (connected by an arrow)
3. Right-click the SMesh node → **Edit Input File**
4. Browse to: `smesh/smesh.cmd`
5. Click **OK**

### Add SDevice Node (Row 3):
1. Right-click below SMesh → **Add → Sentaurus Device**
2. A "sdevice" row appears
3. Right-click → **Edit Input File** → `sdevice/sdevice_des.cmd`
4. Click **OK**

### Add SVisual Node (Row 4):
1. Right-click below SDevice → **Add → Sentaurus Visual**
2. Right-click → **Edit Input File** → `svisual/plot_iv.tcl`
3. Click **OK**

The flow should now show: `SDE → SMesh → SDevice → SVisual`

---

## Step 4 — Define the Workbench Variable @mat@

This is the most important step. The `@mat@` variable tells SWB
which material to substitute in your scripts for each column.

1. In SWB menu: **Edit → Variables**
2. Click **New Variable**
3. Set Name: `mat`  (SWB automatically adds the @ signs)
4. Set Type: **String**
5. Click **OK**

Now you see a row labelled `mat` at the TOP of the spreadsheet.

---

## Step 5 — Add 4 Columns (One Per Material)

Each column = one simulation run for one material.

### Column 1 — Silicon:
1. The first column already exists by default
2. Click the cell in the `mat` row, Column 1
3. Type: `Silicon`  (exactly — case sensitive)
4. Press Enter

### Column 2 — Germanium:
1. Right-click Column 1 header → **Duplicate Column**
2. Click the `mat` cell in Column 2
3. Change it to: `Germanium`
4. Press Enter

### Column 3 — GaAs:
1. Duplicate Column 2
2. Change `mat` to: `GaAs`

### Column 4 — 4H-SiC:
1. Duplicate Column 3
2. Change `mat` to: `SiC4H`

**IMPORTANT:** The material names must EXACTLY match Sentaurus's
material database names:
- Silicon → `Silicon` ✅
- Germanium → `Germanium` ✅
- GaAs → `GaAs` ✅
- 4H-SiC → `SiC4H` ✅  (NOT "SiC" or "4HSiC" — will not be found)

---

## Step 6 — Verify the Project Before Running

Before running all 4 materials, verify just Silicon works:

1. Click Column 1 (Silicon) to select it
2. Right-click the SDE node in Column 1 → **Run**
3. Wait for SDE to finish (green checkmark = success)
4. Open the SDE output in the viewer to verify the geometry

**What you should see in the SDE viewer:**
- Two rectangular regions (P on top, N on bottom)
- Red line at top = Anode contact
- Blue line at bottom = Cathode contact
- Color gradient showing doping concentration

If the geometry looks correct, continue:
5. Right-click SMesh node → **Run**
6. Open the mesh viewer: you should see fine mesh near the junction

---

## Step 7 — Run the First Simulation (Silicon Only)

1. Right-click SDevice node in Column 1 → **Run**
2. A log window opens showing SDevice output in real time
3. Watch for convergence messages

**Good signs in the log:**
```
Poisson: Converged. Iterations: 3
Coupled (Poisson Electron Hole): Converged. Iterations: 5
Quasistationary: Step 1, V=0.005V, Converged.
Quasistationary: Step 2, V=0.010V, Converged.
```

**Bad signs (errors):**
```
ERROR: Contact "Anode" not found  → name mismatch in Electrode{}
ERROR: Cannot open file "MaterialDiode_msh.tdr" → SMesh didn't run
Newton not converged after 30 iterations → reduce voltage step size
```

---

## Step 8 — View the Results in SVisual

1. Right-click SVisual node → **Run**
2. SVisual opens automatically and executes the Tcl plot script
3. It generates .png files in the simulation output folder

**To view the .tdr results interactively:**
1. File → Open → select `MaterialDiode_des.tdr`
2. Choose a quantity to display (e.g., "ElectricField")
3. A 2D color map appears — you can zoom into the junction region

---

## Step 9 — Run All 4 Materials

Once Silicon works perfectly:

1. Select ALL 4 columns (Ctrl+Click each column header)
2. Right-click → **Run Selected**
3. SWB runs all 4 simulations — Silicon first, then others in parallel
   (or sequentially depending on license availability)

Total expected run time: 15–30 minutes for all 4 materials.

---

## Step 10 — At College PC: Push the .plt Files to GitHub

After all 4 simulations finish, do this AT THE COLLEGE PC:

**1. Find the SWB output folders** (SWB creates these automatically):
```
sentaurus-tcad-pn-diode/
├── n1_Silicon/MaterialDiode_des.plt
├── n2_Germanium/MaterialDiode_des.plt
├── n3_GaAs/MaterialDiode_des.plt
└── n4_SiC4H/MaterialDiode_des.plt
```

**2. Copy .plt files into the results/ folder with clear names:**
```bash
cp n1_Silicon/MaterialDiode_des.plt results/Si_des.plt
cp n2_Germanium/MaterialDiode_des.plt results/Ge_des.plt
cp n3_GaAs/MaterialDiode_des.plt results/GaAs_des.plt
cp n4_SiC4H/MaterialDiode_des.plt results/SiC4H_des.plt
```

**3. Push to GitHub from college PC:**
```bash
git add results/
git commit -m "Day 2: Simulation .plt results for all 4 materials"
git push
```

That's ALL you do at the college PC for Step 10.
The Python analysis runs at HOME.

---

## Step 11 — At HOME PC: Pull and Run Python Analysis

After you get home, open your terminal:

**1. Pull the simulation results:**
```bash
cd "/home/ananthakrishnan/TCAD project"
git pull
```

**2. Verify the .plt files arrived:**
```bash
ls results/
# Should show: Si_des.plt  Ge_des.plt  GaAs_des.plt  SiC4H_des.plt
```

**3. Run the comparison analysis:**
```bash
venv/bin/python python/compare_materials.py
```
Output: `results/iv_overlay.png` + `results/comparison_table.csv`

**4. Run the breakdown analysis:**
```bash
venv/bin/python python/extract_breakdown.py
```
Output: `results/breakdown_analysis.png`

**5. Run the band diagram script (already tested, works without simulation):**
```bash
venv/bin/python python/plot_band_diagram.py
```
Output: `results/band_diagrams.png`

**6. Push the generated plots back to GitHub:**
```bash
git add results/
git commit -m "Day 2: Python analysis — comparison plots and table"
git push
```

Now all your figures are on GitHub and ready for the report.

---

## Common SWB Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Material not found in database` | Wrong `@mat@` value | Use exact names: Silicon, Germanium, GaAs, SiC4H |
| `Cannot open _msh.tdr` | SMesh didn't run or failed | Check SMesh log for errors, run SMesh first |
| `Contact X not found` | Name mismatch between SDE and SDevice | Check spelling/capitalization matches exactly |
| `Newton not converged` | Voltage step too large near knee | Reduce `MaxStep` in Quasistationary |
| `Negative carrier concentration` | Mesh too coarse at junction | Increase junction refinement in SDE |
| `License checkout failed` | Another tool using the license | Wait and retry, or reduce parallel runs |

---

## File Naming Convention in SWB

SWB uses the project name prefix everywhere.
Our project name is `MaterialDiode`.

So every file that flows between tools is named:
- `MaterialDiode_bnd.tdr` — from SDE (boundary)
- `MaterialDiode_dop.tdr` — from SDE (doping)
- `MaterialDiode_msh.tdr` — from SMesh (mesh)
- `MaterialDiode_des.tdr` — from SDevice (2D results)
- `MaterialDiode_des.plt` — from SDevice (I-V data)
- `MaterialDiode_equil_des.tdr` — equilibrium state (saved explicitly)

**The name `MaterialDiode` must be consistent** across all scripts:
- SDE: `(sde:save-model "MaterialDiode")`
- SMesh: `-boundary "MaterialDiode_bnd.tdr"`
- SDevice: `Grid = "MaterialDiode_msh.tdr"`

If any one of these doesn't match, the pipeline breaks at that step.
