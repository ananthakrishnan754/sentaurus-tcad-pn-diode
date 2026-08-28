Title "4H-SiC PIN Photodiode Mesh Specification"

IOControls {
    InputFile = "SiC4H_Photodiode_bnd.tdr"
    OutputFile = "SiC4H_Photodiode_msh.tdr"
}

Definitions {
    Constant "AluminumProfile" { Species = "BoronActiveConcentration" Value = 1e18 }
    Constant "IntrinsicProfile" { Species = "NitrogenActiveConcentration" Value = 1e13 }
    Constant "NitrogenProfile" { Species = "NitrogenActiveConcentration" Value = 1e18 }
    
    Refinement "Junction" {
        MaxElementSize = (0.05 0.01)
        MinElementSize = (0.005 0.002)
    }
    Refinement "Bulk" {
        MaxElementSize = (0.1 0.05)
        MinElementSize = (0.02 0.01)
    }
}

Placements {
    Constant "AluminumPlacement" {
        Reference = "AluminumProfile"
        EvaluateWindow { Element = region ["P_Region"] }
    }
    Constant "IntrinsicPlacement" {
        Reference = "IntrinsicProfile"
        EvaluateWindow { Element = region ["I_Region"] }
    }
    Constant "NitrogenPlacement" {
        Reference = "NitrogenProfile"
        EvaluateWindow { Element = region ["N_Region"] }
    }
    
    Refinement "Junction_place" {
        Reference = "Junction"
        RefineWindow = rectangle [(0.0 0.15) (1.0 0.85)]
    }
    Refinement "Bulk_place" {
        Reference = "Bulk"
        RefineWindow = rectangle [(0.0 0.0) (1.0 1.0)]
    }
}
