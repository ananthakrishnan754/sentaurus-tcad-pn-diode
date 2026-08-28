Title "GaAs LED Mesh Specification"

IOControls {
    InputFile = "GaAs_LED_bnd.tdr"
    OutputFile = "GaAs_LED_msh.tdr"
}

Definitions {
    Constant "P_Doping" { Species = "CarbonActiveConcentration" Value = 2e18 }
    Constant "I_Doping" { Species = "SiliconActiveConcentration" Value = 1e14 }
    Constant "N_Doping" { Species = "SiliconActiveConcentration" Value = 2e18 }
    
    Refinement "ActiveRegion" {
        MaxElementSize = (0.02 0.005)
        MinElementSize = (0.002 0.001)
    }
    Refinement "Bulk" {
        MaxElementSize = (0.05 0.02)
        MinElementSize = (0.01 0.005)
    }
}

Placements {
    Constant "P_Placement" {
        Reference = "P_Doping"
        EvaluateWindow { Element = region ["P_Region"] }
    }
    Constant "I_Placement" {
        Reference = "I_Doping"
        EvaluateWindow { Element = region ["I_Active_Region"] }
    }
    Constant "N_Placement" {
        Reference = "N_Doping"
        EvaluateWindow { Element = region ["N_Region"] }
    }
    
    Refinement "Active_place" {
        Reference = "ActiveRegion"
        RefineWindow = rectangle [(0.0 0.10) (1.0 0.40)]
    }
    Refinement "Bulk_place" {
        Reference = "Bulk"
        RefineWindow = rectangle [(0.0 0.0) (1.0 0.5)]
    }
}
