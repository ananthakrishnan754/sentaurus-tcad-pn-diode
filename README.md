# Material Engineered PN Diode — Synopsys Sentaurus TCAD

**M.Tech VLSI Project** | Synopsys Sentaurus TCAD

---

## Project Goal

Simulate a PN junction diode in 4 semiconductor materials and compare their electrical characteristics:

- Silicon (Si)
- Germanium (Ge)
- Gallium Arsenide (GaAs)
- 4H-Silicon Carbide (4H-SiC)

---

## Folder Structure

```
TCAD project/
├── sde/              # Sentaurus Device Editor scripts (geometry + doping)
├── smesh/            # Mesh control scripts
├── sdevice/          # SDevice physics simulation scripts
├── svisual/          # SVisual plotting scripts (Tcl)
├── python/           # Python post-processing and comparison scripts
└── results/          # Output plots and CSVs (not tracked by git)
```

---

## Tool Pipeline

```
SDE  →  SMesh  →  SDevice  →  SVisual  →  Python
(geometry)  (mesh)  (physics solve)  (plot)  (analysis)
```

---

## Device Specifications

| Parameter        | Value                  |
|-----------------|------------------------|
| Device type      | Vertical PN diode       |
| Width            | 1 µm                   |
| Total height     | 1 µm                   |
| P-region height  | 0.5 µm (top)           |
| N-region height  | 0.5 µm (bottom)        |
| P-doping (Na)    | 1×10¹⁷ cm⁻³ (Boron)   |
| N-doping (Nd)    | 1×10¹⁶ cm⁻³ (Phosphorus)|
| Temperature      | 300 K                  |

---

## How to Use on College PC

1. `git pull` the latest code
2. Open Sentaurus Workbench (SWB)
3. File → Open → point to this folder
4. Run the SWB project (all tools execute in order)
5. Results appear in the `n*_*/` folders that SWB auto-creates

---

## Workflow — Day by Day

**Day 1:** Silicon PN diode — geometry, mesh, equilibrium, I-V  
**Day 2:** Full physics (SRH, Auger, breakdown) + extend to all 4 materials  
**Day 3:** Visualization, Python comparison, final report figures  

---

## Author

Ananthakrishnan | M.Tech VLSI
