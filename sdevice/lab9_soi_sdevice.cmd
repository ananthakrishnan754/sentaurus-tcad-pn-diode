*---------------------------------------------------------------------
* SOI MOSFET -- SENTAURUS DEVICE (SDEVICE) COMMAND FILE
* Labsheet 9: SOI MOSFET Transfer & Output Characteristics
* Physics: Quantum Corrections, Slotboom Bandgap Narrowing,
*          Doping-Dependent Mobility (PhuMob), High-Field Saturation,
*          SRH Recombination, Body-Tie & Floating Body Dynamics
* Verified on Synopsys Sentaurus Device (N-2017.09)
*---------------------------------------------------------------------

Electrode {
  { Name="source"    Voltage= 0.0  Resistor= 40 }
  { Name="drain"     Voltage= 0.0  Resistor= 40 }
  { Name="gate"      Voltage=-0.1 }
  { Name="substrate" Voltage= 0.0 }
  { Name="bodytie"   Voltage= 0.0 eRecVelocity=0 }
}

File {
  Grid    = "n@node@_msh.tdr"
  Plot    = "n@node@_des.tdr"
  Current = "n@node@_des.plt"
  Output  = "n@node@_des.log"
}

Physics {
  eQCvanDort
  EffectiveIntrinsicDensity(OldSlotboom)
  Recombination(
    SRH(DopingDep)
  )
}

Physics(Material="Silicon") {
  Mobility(
    PhuMob
    Enormal
    eHighFieldsaturation(GradQuasiFermi)
    hHighFieldsaturation(GradQuasiFermi)
  )
  Recombination(
    SRH(DopingDep)
  )
}

Plot {
  eDensity hDensity
  TotalCurrent/Vector eCurrent/Vector hCurrent/Vector
  eMobility hMobility
  eVelocity hVelocity
  eQuasiFermi hQuasiFermi
  eTemperature
  ElectricField/Vector Potential SpaceCharge
  Doping DonorConcentration AcceptorConcentration
  SRH Band2Band
  ImpactIonization eImpactIonization hImpactIonization
  eGradQuasiFermi/Vector hGradQuasiFermi/Vector
  eEparallel hEparallel eENormal hENormal
  BandGap
  BandGapNarrowing
  Affinity
  ConductionBand ValenceBand
}

Math {
  Extrapolate
  Avalderivatives
  RelErrControl
  Digits=5
  ErRef(electron)=1.e10
  ErRef(hole)=1.e10
  Notdamped=50
  Iterations=20
  DirectCurrent
}

Solve {
  NewCurrentPrefix="init"
  Coupled(Iterations=100){ Poisson }
  Coupled{ Poisson Electron Hole }

* Step 1: Ramp Vds to 0.05 V (Linear Conduction Regime)
  Quasistationary(
    InitialStep=1e-1
    Increment=1.2
    MinStep=1e-5
    MaxStep=0.1
    Goal{ Name="drain" Voltage=0.05 }
  ){
    Coupled{ Poisson Electron Hole }
  }

* Step 2: Sweep Gate Voltage from -0.1 V to 1.5 V (Id-Vg Transfer Curve)
  NewCurrentPrefix="IdVg_"
  Quasistationary(
    DoZero
    InitialStep=5e-2
    Increment=1.5
    MinStep=1e-5
    MaxStep=0.05
    Goal{ Name="gate" Voltage=1.5 }
  ){
    Coupled{ Poisson Electron Hole }
    CurrentPlot(
      Time=(Range=(0 1) Intervals=20)
    )
  }
}
