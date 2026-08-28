* ============================================================
* FILE:    sdevice/sdevice_des.cmd
* TOOL:    Sentaurus Device (SDevice)
* PURPOSE: Unified solver script for PIN Photodiode characterization
*          under both DARK and OPTICAL ILLUMINATION conditions.
*
* WORKBENCH VARIABLE: @mat@ is substituted by SWB with one of:
*          Silicon | Germanium | GaAs | SiC4H
*
* SIMULATION STAGES:
*   [DARK CHARACTERIZATION]
*     1. Equilibrium (0 V)
*     2. Dark Reverse Bias Sweep (0 V to -10.0 V)
*     3. Dark Forward Bias Sweep (0 V to +1.0 V)
*   [OPTICAL ILLUMINATION CHARACTERIZATION]
*     4. Illuminated Reverse Bias Sweep (0 V to -3.0 V)
*     5. Wavelength Sweep (λ = 0.3 µm to 1.8 µm) for Responsivity R(λ)
* ============================================================

File {
    Grid    = "MaterialDiode_msh.tdr"
    Plot    = "MaterialDiode_des.tdr"
    Current = "MaterialDiode_des.plt"
}

Electrode {
    { Name = "Anode"   Voltage = 0.0 }
    { Name = "Cathode" Voltage = 0.0 }
}

Physics {
    * --- MOBILITY MODELS ---
    Mobility (
        DopingDependence
        HighFieldSaturation
    )

    * --- RECOMBINATION MODELS ---
    Recombination (
        SRH ( DopingDependence )
        Auger
        Radiative
    )

    * --- BAND STATISTICS & BANDGAP NARROWING ---
    Fermi
    EffectiveIntrinsicDensity ( BandGapNarrowing(OldSlotBoom) )

    * --- OPTICAL GENERATION & SOLVER PHYSICS ---
    Optics (
        OpticalSolver ( RayTrace )
        OpticalGeneration ( QuantumYield = 1.0 )
    )
    Temperature = 300
}

Optics {
    * Monochromatic optical illumination vertically incident on top surface (y = 0)
    OpticalIntensity (
        Wavelength = 0.55             * 550 nm (green light) baseline
        Intensity  = 0.01             * 10 mW/cm^2 optical power density
        Direction  = (0, 1, 0)        * Downward illumination along +y axis
        Origin     = (0.5, -0.001, 0) * Origin above top surface
        Width      = 1.0              * Cover full device width (1.0 µm)
    )
}

Math {
    Iterations = 30
    RelErrControl
    Digits = 5
    NotDamped = 50
    Extrapolate
    Method = ParDiSo
    -CheckUndefinedModels
    Number_of_Threads = 4
}

Plot {
    ElectricField
    ElectrostaticPotential
    SpaceCharge
    eDensity
    hDensity
    Doping
    DonorConcentration
    AcceptorConcentration
    BandGap
    ConductionBand
    ValenceBand
    eQuasiFermi
    hQuasiFermi
    IntrinsicDensity
    OpticalGeneration         * Photogenerated carrier rate (cm^-3 s^-1)
    OpticalAbsorption         * Optical absorption profile
    eCurrent
    hCurrent
    TotalCurrent
    SRHRecombination
    AugerRecombination
    RadiativeRecombination
    eMobility
    hMobility
}

Solve {
    * ==========================================================
    * PART 1: DARK CHARACTERIZATION
    * ==========================================================

    * --- Stage 1: Equilibrium Simulation (0 V) ---
    Poisson
    Coupled { Poisson Electron Hole }
    Plot (FilePrefix = "MaterialDiode_dark_equil")

    * --- Stage 2: Dark Reverse Bias Sweep (0 V to -10.0 V) ---
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.5
        Increment   = 1.5
        Decrement   = 5
        Goal { Name = "Anode" Voltage = -10.0 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "MaterialDiode_dark_rev")

    * --- Stage 3: Dark Forward Bias Sweep (0 V to +1.0 V) ---
    Load (FilePrefix = "MaterialDiode_dark_equil")
    Quasistationary (
        InitialStep = 0.005
        MinStep     = 0.0001
        MaxStep     = 0.02
        Increment   = 1.5
        Decrement   = 3
        Goal { Name = "Anode" Voltage = 1.0 }
    ) { Coupled { Poisson Electron Hole } }
    Plot (FilePrefix = "MaterialDiode_dark_fwd")


    * ==========================================================
    * PART 2: OPTICAL ILLUMINATION CHARACTERIZATION
    * ==========================================================

    * --- Stage 4: Illuminated Reverse Bias Sweep (0 V to -3.0 V) ---
    Load (FilePrefix = "MaterialDiode_dark_equil")
    Quasistationary (
        InitialStep = 0.01
        MinStep     = 0.0001
        MaxStep     = 0.2
        Increment   = 1.5
        Decrement   = 3
        NewCurrentPrefix = "Illuminated_"
        Goal { Name = "Anode" Voltage = -3.0 }
    ) { Coupled { Poisson Electron Hole Optics } }
    Plot (FilePrefix = "MaterialDiode_opt_rev")

    * --- Stage 5: Wavelength Sweep for Spectral Responsivity R(λ) ---
    * At fixed VR = -3.0 V, sweep wavelength λ from 0.3 µm to 1.8 µm
    Quasistationary (
        InitialStep = 0.02
        MinStep     = 0.001
        MaxStep     = 0.05
        Increment   = 1.5
        Decrement   = 3
        NewCurrentPrefix = "Spectral_"
        Goal { Parameter = "Wavelength" Value = 1.8 }  * Sweep to 1800 nm (IR region)
    ) { Coupled { Poisson Electron Hole Optics } }
    Plot (FilePrefix = "MaterialDiode_opt_wavelength")
}

* ============================================================
* END OF UNIFIED SDEVICE SCRIPT
* ============================================================

