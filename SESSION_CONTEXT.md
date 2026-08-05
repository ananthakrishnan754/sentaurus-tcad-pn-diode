# SESSION CONTEXT — Sentaurus TCAD Mentor
## Saved: 2026-08-05 | Conversation ID: 1392b899-38f4-4c4b-a9e0-014fdf055875

---

## Who You Are
- M.Tech VLSI student, beginner in Sentaurus TCAD
- Home PC: Ubuntu, VS Code, Python, Git (no Sentaurus)
- College PC: Has licensed Sentaurus installed
- Deadline: 3 days to complete working project

---

## Project Title
**Material Engineered PN Diode using Synopsys Sentaurus TCAD**

Simulate the same PN diode in 4 materials and compare everything:
- Silicon (Si)
- Germanium (Ge)
- Gallium Arsenide (GaAs)
- 4H-Silicon Carbide (4H-SiC)

---

## GitHub Repository
**https://github.com/ananthakrishnan754/sentaurus-tcad-pn-diode**

This is where ALL project files live. On college PC: `git clone` this repo.

---

## Device Specifications (FIXED — never change these)
| Parameter | Value |
|---|---|
| Device type | Vertical PN diode (2D cross-section) |
| Width | 1 µm (x-direction) |
| Total height | 1 µm (y-direction) |
| P-region | Top 0.5 µm (y = 0 to 0.5) |
| N-region | Bottom 0.5 µm (y = 0.5 to 1.0) |
| P-doping Na | 1×10¹⁷ cm⁻³ (Boron) |
| N-doping Nd | 1×10¹⁶ cm⁻³ (Phosphorus) |
| Temperature | 300 K |
| Anode contact | Top edge (y = 0) |
| Cathode contact | Bottom edge (y = 1.0) |

---

## Tool Pipeline
```
SDE → SMesh → SDevice → SVisual → Python
```
All 4 tools are wired in SWB (Sentaurus Workbench).
`@mat@` Workbench variable switches material per column.

---

## What Has Been Completed (Day 1 — Home PC)

### ✅ Files Written and Pushed to GitHub

| File | Status | What it does |
|---|---|---|
| `sde/sde_dvs.cmd` | ✅ Done | Draws geometry, doping (Boron 1e17, Phosphorus 1e16), contacts (Anode top, Cathode bottom), mesh refinement windows |
| `smesh/smesh.cmd` | ✅ Done | Mesh quality (max-edge 100nm global, 5nm at junction interface), doping gradient refinement |
| `sdevice/sdevice_des.cmd` | ✅ Done | Physics (SRH, Auger, Radiative, Fermi, BGN, mobility), Equilibrium + Forward 0→+1V + Reverse 0→-20V sweeps |
| `svisual/plot_iv.tcl` | ✅ Done | Plots forward/reverse/log I-V curves from .plt file |
| `svisual/plot_fields.tcl` | ✅ Done | Plots band diagram, E-field, carrier concentration, potential, recombination rates |
| `python/compare_materials.py` | ✅ Done | Parses all 4 .plt files, extracts turn-on voltage/ideality/I0/breakdown, generates comparison table + overlay plots |
| `python/extract_breakdown.py` | ✅ Done | Finds breakdown voltage, computes theoretical depletion width W(V) |
| `python/plot_band_diagram.py` | ✅ Done | Theoretical band diagrams for all 4 materials (works WITHOUT TCAD, already tested and generates results/band_diagrams.png) |
| `SWB_SETUP_GUIDE.md` | ✅ Done | Step-by-step GUI instructions for SWB setup on college PC |
| `STUDY_NOTES.md` | ✅ Done | 12 Q&As covering all concepts learned (SDE, SMesh, SDevice) |
| `README.md` | ✅ Done | Project overview |
| `.gitignore` | ✅ Done | Excludes .tdr, .plt_old, venv/, n*/ simulation folders |

### ✅ Python Environment
```bash
cd "/home/ananthakrishnan/TCAD project"
venv/bin/python python/plot_band_diagram.py   # already tested and works
```
Output confirmed: `results/band_diagrams.png` generated with Vbi values:
- Silicon: 0.753 V
- Germanium: 0.371 V
- GaAs: 1.212 V
- 4H-SiC: 2.927 V

---

## What Needs to Happen Next (Day 2 — College PC)

### Priority Order at the College PC:

**Step 1 — Clone and setup SWB**
```bash
git clone https://github.com/ananthakrishnan754/sentaurus-tcad-pn-diode.git
```
Then follow `SWB_SETUP_GUIDE.md` exactly.

**Step 2 — Run Silicon ONLY first**
- Run SDE → verify geometry (P-region top, N-region bottom, contacts visible)
- Run SMesh → verify mesh (fine near y=0.5, coarse in bulk)
- Run SDevice → watch log for convergence
- Run SVisual → check I-V curve shape

**Step 3 — Verify Silicon results against expected values**

Expected Silicon results (at Na=1e17, Nd=1e16, 300K):
| Parameter | Expected Value |
|---|---|
| Built-in voltage Vbi | ~0.75 V |
| Turn-on voltage (I > 1µA) | ~0.55–0.65 V |
| Depletion width at 0V | ~0.30–0.40 µm |
| Reverse leakage I0 at -1V | ~10⁻¹⁵ to 10⁻¹⁴ A |
| Breakdown voltage | ~-30 to -50 V |
| Ideality factor | ~1.5 to 2.0 (SRH regime) |

**Step 4 — Debug if anything is wrong (common issues listed below)**

**Step 5 — Extend to all 4 materials**
Once Silicon is perfect: right-click → Duplicate column × 3, change @mat@ to Germanium, GaAs, SiC4H.

**Step 6 — Collect .plt files and run Python**
```bash
cp n1_Silicon/MaterialDiode_des.plt results/Si_des.plt
cp n2_Germanium/MaterialDiode_des.plt results/Ge_des.plt
cp n3_GaAs/MaterialDiode_des.plt results/GaAs_des.plt
cp n4_SiC4H/MaterialDiode_des.plt results/SiC4H_des.plt
venv/bin/python python/compare_materials.py
venv/bin/python python/extract_breakdown.py
```

**Step 7 — Commit results**
```bash
git add results/
git commit -m "Day 2: Simulation results for all 4 materials"
git push
```

---

## Day 3 Plan (After Simulations Are Done)

1. Add optical generation model (AM1.5 spectrum) to SDevice
2. Add internal quantum efficiency (IQE) calculation
3. Generate all final report figures via SVisual
4. Write the comparison table in LaTeX/Word
5. Polish Python plots for report quality

---

## Common Errors and Fixes (Quick Reference)

| Error | Cause | Fix |
|---|---|---|
| `Material not found` | Wrong @mat@ name | Use: Silicon, Germanium, GaAs, SiC4H |
| `Cannot open _msh.tdr` | SMesh didn't run | Run SMesh first |
| `Contact X not found` | Name mismatch | "Anode"/"Cathode" must match exactly between SDE and SDevice |
| `Newton not converged` | Voltage step too large | Reduce MaxStep in Quasistationary |
| `Negative carrier concentration` | Mesh too coarse | Increase junction refinement |
| SDE runs but geometry wrong | Coordinate error | Remember: Y increases DOWNWARD in SDE |
| `License checkout failed` | License busy | Wait and retry |

---

## Key Concepts Learned (Summary)

- SWB @mat@ variable = run same script for 4 materials automatically
- SDE comment syntax = semicolon `;`
- SDevice comment syntax = asterisk `*` (NOT semicolon — syntax error if wrong)
- Mesh is finest at PN junction (2-5 nm), coarser in bulk (50-80 nm)
- SDevice always solves Poisson first, then coupled (Poisson+Electron+Hole)
- Adaptive stepping: Increment=1.5× on easy steps, Decrement=3× on failures
- Always load equilibrium state before starting reverse sweep
- SRH dominates in Si/Ge (indirect gap), Radiative dominates in GaAs (direct gap)
- Ideality factor n: extracted from slope of log(I) vs V in forward region
- File naming: EVERYTHING uses prefix "MaterialDiode" — must be consistent across SDE/SMesh/SDevice

---

## Study Notes File
All 12 Q&As are in `STUDY_NOTES.md` — read before sitting at college PC.

---

## How to Continue This Conversation

When you come back, tell the AI:
> "I'm continuing my Sentaurus TCAD project. Conversation ID: 1392b899-38f4-4c4b-a9e0-014fdf055875. Here is what happened at the college PC today: [describe results or errors]"

The AI will read this file from the repo and pick up exactly where we left off.
