Title "Silicon PIN Photodiode Mesh Specification"

IOControls {
    InputFile = "Si_Photodiode_bnd.tdr"
    OutputFile = "Si_Photodiode_msh.tdr"
}

Definitions {
    Constant "BoronProfile" { Species = "BoronActiveConcentration" Value = 1e18 }
    Constant "IntrinsicProfile" { Species = "PhosphorusActiveConcentration" Value = 1e13 }
    Constant "PhosphorusProfile" { Species = "PhosphorusActiveConcentration" Value = 1e18 }
    
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
    Constant "BoronPlacement" {
        Reference = "BoronProfile"
        EvaluateWindow { Element = region ["P_Region"] }
    }
    Constant "IntrinsicPlacement" {
        Reference = "IntrinsicProfile"
        EvaluateWindow { Element = region ["I_Region"] }
    }
    Constant "PhosphorusPlacement" {
        Reference = "PhosphorusProfile"
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
