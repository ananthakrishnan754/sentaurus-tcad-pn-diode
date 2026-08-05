* ============================================================
* FILE:    sdevice/sdevice_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Solve the semiconductor equations for the PN diode.
*          Runs three simulations in sequence:
*          1. Equilibrium (0 V, device at rest)
*          2. Forward I-V sweep (0 V to +1.0 V)
*          3. Reverse I-V sweep (0 V to -20 V)
*
* NOTE:    Comments in SDevice use * (asterisk), NOT ;
*          This is different from SDE which uses ; (semicolon)
*          Mixing them up causes a syntax error.
*
* INPUT:   MaterialDiode_msh.tdr  (from SMesh)
* OUTPUT:  MaterialDiode_des.plt  (I-V plot data)
*          MaterialDiode_des.tdr  (2D field data at each bias)
* ============================================================


* ============================================================
* SECTION 1: FILE { }
* Tells SDevice which files to read as input and which files
* to write as output. These names MUST match the mesh file
* that SMesh produced.
* ============================================================

File {
    * --- Input: the meshed device from SMesh ---
    Grid    = "MaterialDiode_msh.tdr"
    * This is the ONLY input file SDevice needs.
    * It contains everything: geometry, mesh, doping, contacts.

    * --- Output 1: Plot file for I-V curves ---
    Plot    = "MaterialDiode_des.tdr"
    * This saves 2D spatial data (electric field, carrier
    * concentration, potential, etc.) at each bias point.
    * You open this in SVisual to see 2D color maps.

    * --- Output 2: Current-Voltage data ---
    Current = "MaterialDiode_des.plt"
    * This saves terminal currents vs voltage as a table.
    * SVisual reads this to plot the I-V curve.
    * It is a text file — you can also open it in Python.

    * --- Output 3: Parameter file (material properties) ---
    Parameter = "MaterialDiode.par"
    * SDevice writes the material parameters it used.
    * Useful for verifying that Sentaurus loaded the correct
    * bandgap, mobility, etc. for your chosen @mat@ material.
}


* ============================================================
* SECTION 2: ELECTRODE { }
* Defines every metal contact in the device and sets its
* initial condition at the start of simulation.
*
* For a PN diode we have two contacts:
*   Anode   → connected to P-region (top)
*   Cathode → connected to N-region (bottom)
*
* Names here MUST exactly match what SDE used when defining
* contacts. Case-sensitive — "Anode" ≠ "anode".
* ============================================================

Electrode {
    { Name = "Anode"
      Voltage = 0.0 }
    * The Anode starts at 0 V.
    * During the forward sweep, SWB will ramp this voltage up.
    * During the reverse sweep, SWB will ramp this voltage down.
    * Voltage is in Volts.

    { Name = "Cathode"
      Voltage = 0.0 }
    * The Cathode is held at 0 V throughout ALL simulations.
    * It is the reference (ground) terminal.
    * All voltages are measured relative to this terminal.

    * IMPORTANT: In semiconductor convention, we always apply
    * voltage to the Anode and keep Cathode at ground.
    * Forward bias:  Anode > Cathode (positive Anode voltage)
    * Reverse bias:  Anode < Cathode (negative Anode voltage)
}


* ============================================================
* SECTION 3: PHYSICS { }
* This is where you SELECT which physical phenomena to model.
* Sentaurus has dozens of models — you must explicitly enable
* each one you want. Models you don't enable are ignored.
*
* For a PN diode we need:
*   - Drift-Diffusion transport (always required)
*   - SRH recombination (dominant in Si, Ge)
*   - Auger recombination (important at high injection)
*   - Bandgap narrowing (important for heavily doped regions)
*   - Fermi statistics (more accurate than Boltzmann)
* ============================================================

Physics {
    * --- MOBILITY MODELS ---
    * These models determine how fast carriers move
    * under electric field and doping conditions.
    Mobility (
        DopingDependence        * mobility decreases with doping
        HighFieldSaturation     * velocity saturates at high fields
        Enormal                 * normal field dependence (less critical in 2D)
    )
    * WHY DopingDependence?
    * In a heavily doped region (1e17 cm^-3), dopant atoms
    * scatter carriers and reduce their mobility. Without this
    * model, mobility is constant everywhere — which is wrong.
    * With it, mobility in the P-region (~1e17) is lower than
    * in the N-region (~1e16), as it should be physically.
    *
    * WHY HighFieldSaturation?
    * Near the junction, the electric field can be very strong
    * (>1e5 V/cm). At high fields, carrier velocity doesn't
    * keep increasing linearly — it saturates at ~1e7 cm/s.
    * Without this model, SDevice overestimates current at
    * high reverse bias and gives unphysical I-V curves.


    * --- RECOMBINATION MODELS ---
    * Recombination = electrons and holes annihilating each
    * other. This is what limits forward current at low bias
    * and determines reverse leakage current.
    Recombination (
        SRH (
            DopingDependence    * SRH lifetime depends on doping
        )
        Auger                   * band-to-band recombination at high carrier density
        Radiative               * photon emission (important for GaAs — direct bandgap)
    )
    * WHAT IS SRH?
    * Shockley-Read-Hall recombination occurs through defect
    * energy levels (traps) in the bandgap. Every real silicon
    * crystal has defects from dopant atoms, crystal boundaries,
    * and impurities. Carriers get captured by these traps.
    * SRH is the dominant recombination mechanism in Si and Ge.
    * DopingDependence means the trap density (and thus the
    * recombination rate) increases with doping concentration.
    *
    * WHAT IS AUGER?
    * Auger recombination involves 3 carriers — an electron and
    * hole recombine, giving their energy to a third carrier
    * (another electron or hole). It's negligible at low carrier
    * concentrations but becomes dominant above ~1e18 cm^-3.
    * At high forward bias (high injection), you get very high
    * carrier concentrations and Auger becomes important.
    *
    * WHAT IS RADIATIVE?
    * When an electron falls from conduction band to valence band
    * across a direct bandgap, it emits a photon. This is
    * critical for GaAs (direct gap) but negligible for Si and
    * Ge (indirect gap). We enable it for all materials because
    * SDevice will use a near-zero rate for indirect gap
    * materials automatically — no harm in leaving it on.


    * --- BAND STATISTICS ---
    * This controls whether Fermi-Dirac or Boltzmann statistics
    * are used to compute carrier concentrations.
    Fermi                       * use full Fermi-Dirac statistics
    * WHY FERMI instead of default Boltzmann?
    * The default Boltzmann approximation is valid only when
    * the Fermi level is far from the band edges (>3kT away).
    * In our P-region at Na=1e17, the Fermi level is close to
    * the valence band. Boltzmann underestimates the hole
    * concentration there. Fermi-Dirac is exact and adds
    * almost no simulation time.


    * --- BANDGAP NARROWING ---
    * At high doping (>~5e17 cm^-3), the discrete dopant atoms
    * create a band of energy levels that effectively narrows
    * the semiconductor bandgap. This increases ni (intrinsic
    * carrier concentration) significantly.
    BandGapNarrowing (OldSlotboom)
    * We use the Slotboom model — a classic, well-validated
    * model for Si. For GaAs and SiC, Sentaurus will
    * automatically substitute the appropriate BGN parameters
    * from its material database.
    * This model matters most for the P-region (Na=1e17).
    * Without it, ni in the P-region is slightly underestimated.


    * --- TEMPERATURE ---
    * Set simulation temperature in Kelvin.
    * All 4 materials use the same temperature — 300 K (27°C).
    * Changing temperature would change every material property,
    * which would make the material comparison unfair.
    Temperature = 300
}


* ============================================================
* SECTION 4: MATH { }
* Controls the numerical solver — how it iterates, when it
* considers a solution "converged", and what to do when it
* struggles.
*
* You rarely need to touch this for a working simulation,
* but when convergence fails, these settings are your
* debugging levers.
* ============================================================

Math {
    * --- CONVERGENCE CRITERIA ---
    Iterations = 30
    * Maximum Newton iterations per bias point.
    * If the solver doesn't converge in 30 iterations,
    * it tries to reduce the voltage step size and retry.
    * Increasing this doesn't always help — if convergence
    * fails at 30 it usually means a physics or mesh problem.

    RelErrControl               * use relative error for convergence check
    Digits = 5
    * Solution is "converged" when the relative error drops
    * below 10^-5 (0.001%). This is the default and is
    * accurate enough for device-level simulation.
    * Tighter (Digits=7) is more accurate but slower.

    * --- VOLTAGE STEPPING ---
    NotDamped = 50
    * How many Newton iterations before the solver applies
    * damping (reduces the correction step size).
    * Setting this to 50 means the solver tries full Newton
    * steps aggressively first — good for well-posed problems.

    Extrapolate                 * extrapolate solution from previous bias as initial guess
    * When sweeping voltage from 0 to 0.7 V in steps,
    * the solution at 0.7 V is close to the solution at 0.69 V.
    * Extrapolation uses the trend from previous points to
    * generate a better initial guess — speeds up convergence
    * dramatically, especially in the forward bias region.

    * --- SOLVER TYPE ---
    Method = ParDiSo
    * ParDiSo is the parallel direct solver. It factorizes
    * the Jacobian matrix directly — more robust than iterative
    * solvers for semiconductor device problems.
    * For small 2D devices like ours, it is fast and reliable.
    * For 3D devices with millions of nodes, you'd switch to
    * an iterative solver to save memory.

    * --- NUMBER FORMAT ---
    Number_of_Threads = 4
    * Use 4 CPU threads for the matrix solve.
    * Adjust this to match the college PC's CPU core count.
    * More threads = faster, but with diminishing returns.
    * Check the PC with: nproc (in terminal)
}


* ============================================================
* SECTION 5: PLOT { }
* Defines WHICH physical quantities to save in the output
* .tdr file at each bias point.
* Only listed quantities are saved — unlisted ones are lost.
* Adding more quantities increases file size but gives you
* more to analyze in SVisual.
* ============================================================

Plot {
    * --- ELECTROSTATICS ---
    ElectricField               * E-field vector (V/cm)
    ElectrostaticPotential      * φ (V) — the built-in + applied potential
    SpaceCharge                 * net charge density = q(p - n + Nd - Na)

    * --- CARRIER CONCENTRATIONS ---
    eDensity                    * electron concentration n (cm^-3)
    hDensity                    * hole concentration p (cm^-3)
    Doping                      * total net doping Nd - Na (cm^-3)
    DonorConcentration          * Nd (cm^-3)
    AcceptorConcentration       * Na (cm^-3)

    * --- ENERGY BANDS ---
    BandGap                     * Eg (eV) — varies across junction
    ConductionBand              * Ec (eV) — conduction band edge
    ValenceBand                 * Ev (eV) — valence band edge
    eQuasiFermi                 * Efn (eV) — electron quasi-Fermi level
    hQuasiFermi                 * Efp (eV) — hole quasi-Fermi level
    IntrinsicDensity            * ni (cm^-3) — intrinsic carrier concentration

    * --- CURRENT DENSITY ---
    eCurrent                    * electron current density Jn (A/cm^2)
    hCurrent                    * hole current density Jp (A/cm^2)
    TotalCurrent                * Jn + Jp (A/cm^2)

    * --- RECOMBINATION RATES ---
    SRHRecombination            * RSRH (cm^-3 s^-1) — trap-mediated recombination
    AugerRecombination          * RAuger — 3-carrier recombination
    RadiativeRecombination      * Rrad — photon-emitting recombination

    * --- MOBILITY ---
    eMobility                   * µn (cm^2/V·s)
    hMobility                   * µp (cm^2/V·s)
}


* ============================================================
* SECTION 6: SOLVE { }
* This is the simulation control section.
* It tells SDevice WHAT to solve and in WHAT ORDER.
*
* We run three stages:
*   Stage 1: Equilibrium (no voltage)
*   Stage 2: Forward I-V sweep
*   Stage 3: Reverse I-V sweep
*
* The order matters — each stage uses the previous stage's
* solution as its starting point (initial condition).
* ============================================================

Solve {

    * ==========================================================
    * STAGE 1: EQUILIBRIUM SIMULATION
    * Apply 0 V to all contacts. Solve only Poisson's equation.
    * This gives us the built-in potential, depletion width,
    * and equilibrium carrier distribution.
    *
    * WHY START WITH POISSON ONLY?
    * Solving all 3 equations simultaneously from scratch is
    * hard — there is no good initial guess. The equilibrium
    * Poisson solution gives an excellent initial guess for
    * the full coupled system. This is standard practice.
    * ==========================================================

    Poisson                     * Step 1a: solve Poisson alone
    Coupled { Poisson Electron Hole }   * Step 1b: solve full coupled system

    * After these two lines, SDevice has the complete
    * equilibrium solution — built-in potential = ~0.7 V for Si,
    * depletion region formed, Fermi level flat across the device.
    * Save this state to file.

    Plot (FilePrefix = "MaterialDiode_equil")
    * WHY SAVE EQUILIBRIUM SEPARATELY?
    * You want to visualize the device BEFORE any voltage is
    * applied. This lets you verify:
    *   - The depletion region is at y = 0.5 µm (correct location)
    *   - The built-in potential matches theory (~0.7 V for Si)
    *   - Electron and hole concentrations are correct
    *   - Band diagram shows the correct junction shape
    * If equilibrium looks wrong, don't run the sweeps yet.
    * Fix the structure first.


    * ==========================================================
    * STAGE 2: FORWARD BIAS I-V SWEEP
    * Ramp Anode from 0 V to +1.0 V in small steps.
    * Record Anode current at each step.
    * This generates the forward I-V characteristic.
    *
    * STEP SIZE STRATEGY:
    * Use small steps (5 mV) in the low-bias region (0 to 0.3 V)
    * where the current changes very slowly.
    * Use medium steps (10 mV) in the exponential region.
    * This balances accuracy vs simulation time.
    * ==========================================================

    Quasistationary (
        InitialStep  = 0.005    * start with 5 mV steps
        MinStep      = 0.0001   * minimum allowed step = 0.1 mV
        MaxStep      = 0.02     * maximum allowed step = 20 mV
        Increment    = 1.5      * if step converges easily, multiply step by 1.5
        Decrement    = 3        * if step fails, divide step by 3 and retry
        Goal { Parameter = "Anode" Voltage = 1.0 }  * sweep to +1.0 V
    ) { Coupled { Poisson Electron Hole } }

    * HOW THE ADAPTIVE STEPPING WORKS:
    * SDevice starts with InitialStep = 5 mV.
    * If it converges easily (few iterations), it multiplies
    *   the step by Increment (1.5) → next step = 7.5 mV
    * If it struggles or fails, it divides by Decrement (3)
    *   → next step = 1.67 mV, and retries from last good point.
    * This continues until Voltage = 1.0 V is reached.
    * The adaptive stepping is crucial in the knee region
    * (~0.5 to 0.7 V for Si) where current changes rapidly.

    * Save forward bias results
    Plot (FilePrefix = "MaterialDiode_fwd")


    * ==========================================================
    * STAGE 3: REVERSE BIAS I-V SWEEP
    * Starting from equilibrium (0 V), ramp Anode to -20 V.
    * This sweeps through reverse bias and towards breakdown.
    *
    * IMPORTANT: We must go back to equilibrium first.
    * After the forward sweep, the device is in a high-current
    * state. We must reset to 0 V before going negative.
    * The "Load" command re-reads the equilibrium solution.
    * ==========================================================

    Load (FilePrefix = "MaterialDiode_equil")
    * This restores the equilibrium state (from Stage 1).
    * Now we can start the reverse sweep from 0 V.

    Quasistationary (
        InitialStep  = 0.01     * start with 10 mV steps
        MinStep      = 0.0001   * minimum 0.1 mV
        MaxStep      = 0.5      * maximum 500 mV (reverse is smoother)
        Increment    = 1.5
        Decrement    = 5        * more aggressive reduction near breakdown
        Goal { Parameter = "Anode" Voltage = -20.0 }  * sweep to -20 V
    ) { Coupled { Poisson Electron Hole } }

    * WHY -20 V?
    * Silicon breakdown voltage for Na=1e17, Nd=1e16 is
    * approximately 30-50 V. Going to -20 V will show the
    * reverse leakage current plateau and the beginning of
    * the avalanche region.
    * For Ge (smaller bandgap), breakdown is at lower voltage.
    * For GaAs and SiC, breakdown is much higher.
    * If -20 V is not enough for a material, you'll see the
    * curve still flat — increase this to -50 V or -100 V.
    *
    * CONVERGENCE NOTE FOR BREAKDOWN:
    * Near breakdown, current increases rapidly and the solver
    * may struggle. That is normal. If it stops before -20 V,
    * that is actually useful information — it means breakdown
    * is occurring at that voltage.

    * Save reverse bias results
    Plot (FilePrefix = "MaterialDiode_rev")
}

* ============================================================
* END OF SDEVICE SCRIPT
* ============================================================
