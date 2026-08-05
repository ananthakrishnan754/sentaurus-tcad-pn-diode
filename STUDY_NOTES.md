# TCAD Study Notes — M.Tech VLSI
## Material Engineered PN Diode | Synopsys Sentaurus

> This file grows every session. One concept, one Q&A, fully explained.
> Re-read this before sitting at the college PC.

---

## Session 1 — SDE (Sentaurus Device Editor)

### Q1: Why does `@mat@` appear in the SDE script instead of writing "Silicon" directly?

**Answer:**
`@mat@` is a **Sentaurus Workbench variable**. When SWB runs the project, it substitutes `@mat@` with the actual material name from a table you define in SWB (e.g., Silicon, Germanium, GaAs, SiC4H). This means you write ONE SDE script and SWB runs it FOUR times, once for each material. Without `@mat@`, you would need to write and maintain 4 separate SDE files — if you change the geometry, you'd have to change it 4 times. With `@mat@`, you change it once and all 4 simulations update automatically.

---

### Q2: Why is the mesh finer near the junction (y ≈ 0.5 µm) than in the bulk?

**Answer:**
The PN junction is where all the interesting physics happens — the depletion region, the peak electric field, the built-in potential gradient. The semiconductor equations (Poisson + continuity) involve computing spatial gradients (how fast the potential or carrier concentration changes with position). Near the junction, these gradients are very steep. If the mesh is coarse there, the numerical gradient is inaccurate, giving wrong results for electric field, depletion width, and current. In the bulk, the potential is nearly flat (no steep gradient), so a coarse mesh gives perfectly accurate results there and saves simulation time.

---

### Q3: What are the two output files from SDE and what does each one contain?

**Answer:**
- `MaterialDiode_bnd.tdr` — the **boundary file**. Contains the geometric shape of the device: where each region starts and ends, the positions of contacts, and the mesh refinement window instructions. Think of it as the "blueprint" of the device.
- `MaterialDiode_dop.tdr` — the **doping file**. Contains the doping concentration at every point in the device. SMesh reads this to know where to apply fine mesh (wherever doping changes rapidly). SDevice also reads this to know the net charge at every mesh node.

---

### Q4: Why is N-doping (1×10¹⁶ cm⁻³) lower than P-doping (1×10¹⁷ cm⁻³)?

**Answer:**
This creates a **p⁺n junction** (one-sided abrupt junction). In this configuration, the depletion region extends much further into the lightly-doped N-side and very little into the heavily-doped P-side. This is physically very common in real devices (solar cells, rectifier diodes, photodiodes). It also makes the simulation more interesting to analyze — the electric field is asymmetric, peaking at the junction and decaying into the N-side. If both sides had equal doping, the depletion region would be symmetric, which is a less realistic and less educational case.

---

## Session 1 — SMesh (Sentaurus Mesher)

### Q5: Why do we need three separate refinement mechanisms (SDE window + interface refinement + doping gradient) instead of just one?

**Answer:**
Each mechanism targets a different aspect of the problem:

- **SDE refinement window** targets a *spatial region* — it says "use fine mesh in this rectangular zone". It's blunt but effective for the general area around the junction.
- **Interface refinement** targets the *exact boundary line* between two regions. The junction at y = 0.5 µm is a mathematical line, and the potential gradient is steepest right on that line. The SDE window gives ~10 nm resolution 0.1 µm away from the junction; the interface refinement gives 2–5 nm resolution right at the junction itself.
- **Doping gradient refinement** is *adaptive* — it automatically finds wherever the doping changes most rapidly and splits those triangles. It doesn't need you to specify a location; it finds it automatically from the data.

Together they give you: correct resolution everywhere the physics demands it, without you having to manually identify every critical location.

---

### Q6: What does `MaxTransDiff 1.0` mean in physical terms — what happens to a triangle that violates it?

**Answer:**
`MaxTransDiff 1.0` means: if the doping concentration changes by more than **10^1.0 = 10×** across a single mesh element, that element is too coarse. SMesh automatically splits it into smaller triangles and checks again. This repeats until no element violates the constraint. In our device, the transition from 1×10¹⁷ (P-side) to 1×10¹⁶ (N-side) is a change of exactly 10×. This means the mesh at the junction will be split until each individual triangle spans at most a 10× doping change — ensuring the junction is resolved accurately across at least 1–2 triangles.

---

### Q7: If the device had a thin oxide layer (like a MOSFET gate), which refinement type would you use at the oxide-semiconductor interface?

**Answer:**
You would use **interface refinement** (`sdedr:define-refinement-interface`) between the oxide region and the silicon region — exactly as we did for the P_Region/N_Region boundary. The oxide-semiconductor interface is where the inversion layer forms (the channel in a MOSFET), and the carrier concentration changes from zero (inside oxide) to a very high value (inversion layer) over just a few nanometers. The interface refinement command tells SMesh to pack mesh nodes tightly right at that boundary line, giving 1–2 nm resolution where the physics demands it.

---

---

## Session 1 — SDevice (Sentaurus Device Solver)

### Q8: What are the 5 mandatory sections in every SDevice script and what does each one do?

**Answer:**
- `File { }` — tells SDevice which mesh file to read as input and what to name the output files (.tdr for 2D field data, .plt for I-V curve data).
- `Electrode { }` — lists every metal contact defined in SDE and sets its starting voltage. The names must exactly match the contact names from SDE.
- `Physics { }` — selects which physical models to activate (mobility models, recombination models, statistics). Only listed models run — everything else is ignored.
- `Math { }` — configures the numerical Newton solver: how many iterations, when to declare convergence, which linear algebra solver to use.
- `Solve { }` — specifies what simulations to run, in what order, and with what voltage targets. This is the "control script" that drives the entire simulation.

---

### Q9: Why does SDevice solve Poisson alone first, THEN solve all 3 equations together?

**Answer:**
Starting all 3 equations simultaneously from a zero-field initial guess is a very hard numerical problem — the Newton solver fails to converge because the starting point is too far from the true solution. The trick is to first solve only Poisson's equation, which is a simpler problem with a guaranteed solution. This gives you a physically reasonable potential distribution (built-in potential, depletion region). This Poisson-only solution is then used as the starting point (initial guess) for the full 3-equation coupled solve. With a good initial guess, the coupled solve converges in a few iterations. This two-step approach is the standard industry practice in TCAD.

---

### Q10: What is SRH recombination and why does it dominate in Silicon?

**Answer:**
Shockley-Read-Hall (SRH) recombination is a two-step process. An electron gets captured by a trap (defect energy level in the bandgap), and then a hole gets captured by the same trap — or vice versa. The trap acts as a stepping stone for the electron-hole recombination. Silicon has an indirect bandgap, meaning a direct electron-to-hole recombination requires simultaneous emission of both a photon AND a phonon — this is very unlikely. So in Si, carriers almost always recombine via traps (SRH). In GaAs (direct bandgap), carriers can recombine directly by emitting a photon, making radiative recombination dominant and SRH less important.

---

### Q11: What does the adaptive stepping in Quasistationary actually do?

**Answer:**
Instead of sweeping voltage in fixed steps (e.g., always 10 mV), adaptive stepping adjusts the step size dynamically based on how hard the solver is working. If it converges easily in few iterations, the step size is multiplied by `Increment` (1.5×) — the solver takes larger jumps, saving time. If it fails to converge, the step is divided by `Decrement` (3×) and retried from the last good point — the solver takes smaller steps through the difficult region. This is critical in the forward bias "knee" region (~0.5–0.7 V for Si) where current changes by many orders of magnitude over a small voltage range. Fixed stepping there would either be too coarse (inaccurate) or too fine everywhere (very slow).

---

### Q12: Why do we load the equilibrium state before the reverse bias sweep?

**Answer:**
After the forward bias sweep ends at +1.0 V, the device is in a high injection state — large amounts of minority carriers have been injected across the junction. If we immediately try to sweep to -20 V from this state, the solver must jump from a +1.0 V forward bias solution all the way to -20 V reverse bias in one step. This enormous jump will fail to converge. By loading the saved equilibrium state (0 V, no injection), we give the solver a clean, physically correct starting point for the reverse sweep. Each stage of a Solve block must start from a physically sensible state.

---

*— More Q&As will be added each session —*
