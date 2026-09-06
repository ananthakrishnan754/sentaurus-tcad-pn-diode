;====================================================
; 3D MOSFET - SDE CODE (CORRECTED & WORKING)
; Labsheet 8: 3D MOSFET Structure Editor Emulation
; Verified on Synopsys Sentaurus TCAD Structure Editor (SDE)
;====================================================

(sde:clear)

;----------------------------------------------------
; 1. Coordinate system and Boolean Configuration
;----------------------------------------------------
; Under "BAB", existing shapes retain priority when
; enclosing shapes are added, ensuring inner volumes
; (gate, dielectrics, trenches) are preserved as shells.
(sdegeo:set-default-boolean "BAB")


;----------------------------------------------------
; 2. Trench Isolation Oxides
;    (Created first under "BAB" so that Substrate
;     surrounds the trench oxides without overwriting them)
;----------------------------------------------------
(sdegeo:create-cuboid
    (position -0.20 -0.20 -0.2)
    (position  0.20 -0.10  0.0)
    "Oxide"
    "TrenchOxide_Right"
)

(sdegeo:create-cuboid
    (position -0.20  0.10 -0.2)
    (position  0.20  0.20  0.0)
    "Oxide"
    "TrenchOxide_Left"
)


;----------------------------------------------------
; 3. Silicon Substrate
;----------------------------------------------------
(sdegeo:create-cuboid
    (position -0.25 -0.20 -1.0)
    (position  0.25  0.20  0.0)
    "Silicon"
    "SubsSilicon"
)


;----------------------------------------------------
; 4. Gate Oxide
;    (Fixed: non-zero thickness from Z = 0.0 to 0.002 um)
;----------------------------------------------------
(sdegeo:create-cuboid
    (position -0.15 -0.10 0.0)
    (position  0.15  0.10 0.002)
    "Oxide"
    "GateOxide"
)


;----------------------------------------------------
; 5. Polysilicon Gate
;----------------------------------------------------
(sdegeo:create-cuboid
    (position -0.10 -0.10 0.002)
    (position  0.10  0.20 0.1)
    "PolySi"
    "PolyGate"
)


;----------------------------------------------------
; 6. Poly Reoxidation
;----------------------------------------------------
(sdegeo:create-cuboid
    (position -0.103 -0.103 0.0)
    (position  0.103  0.20  0.1)
    "Oxide"
    "PolyReOxide1"
)

(sdegeo:create-cuboid
    (position -0.15 -0.15 0.0)
    (position  0.15  0.20 0.005)
    "Oxide"
    "PolyReOxide2"
)


;----------------------------------------------------
; 7. Nitride Spacer
;----------------------------------------------------
(sdegeo:create-cuboid
    (position -0.15 -0.15 0.0)
    (position  0.15  0.20 0.08)
    "Nitride"
    "NiSpacer"
)


;----------------------------------------------------
; 8. Fillet on Spacer Edge
;    (Fixed: define Scheme variable and find edge ID)
;----------------------------------------------------
(define fillet-radius 0.03)
(sde:define-parameter "fillet-radius" fillet-radius 0.0 0.0)

(sdegeo:fillet
    (list
        (car
            (find-edge-id
                (position 0.0 -0.15 0.08)
            )
        )
    )
    fillet-radius
)


;----------------------------------------------------
; 9. Contact Sets Definition
;----------------------------------------------------
(sdegeo:define-contact-set "substrate" 4 (color:rgb 1 0 0) "##")
(sdegeo:define-contact-set "gate"      4 (color:rgb 0 1 0) "##")
(sdegeo:define-contact-set "source"    4 (color:rgb 0 0 1) "##")
(sdegeo:define-contact-set "drain"     4 (color:rgb 1 1 0) "##")


;----------------------------------------------------
; 10. Substrate Contact
;----------------------------------------------------
(sdegeo:set-current-contact-set "substrate")
(sdegeo:set-contact
    (find-face-id
        (position 0.0 0.0 -1.0)
    )
    "substrate"
)


;----------------------------------------------------
; 11. Gate Contact (Top center of PolyGate)
;----------------------------------------------------
(sdegeo:set-current-contact-set "gate")
(sdegeo:set-contact
    (find-face-id
        (position 0.0 0.05 0.1)
    )
    "gate"
)


;----------------------------------------------------
; 12. Source Metal & Contact Removal
;----------------------------------------------------
(define SOURCE
    (sdegeo:create-cuboid
        (position -0.25 -0.10 0.0)
        (position -0.17  0.10 0.05)
        "Metal"
        "Source"
    )
)

(sdegeo:set-current-contact-set "source")
(sdegeo:set-contact
    SOURCE
    "source"
    "remove"
)


;----------------------------------------------------
; 13. Drain Metal & Contact Removal
;----------------------------------------------------
(define DRAIN
    (sdegeo:create-cuboid
        (position 0.17 -0.10 0.0)
        (position 0.25  0.10 0.05)
        "Metal"
        "Drain"
    )
)

(sdegeo:set-current-contact-set "drain")
(sdegeo:set-contact
    DRAIN
    "drain"
    "remove"
)


;====================================================
; 14. DOPING PROFILES
;====================================================

;----------------------------------------------------
; Bulk Substrate Doping (Boron P-type 1e17 cm^-3)
;----------------------------------------------------
(sdedr:define-constant-profile
    "Const.Bulk"
    "BoronActiveConcentration"
    1e17
)

(sdedr:define-constant-profile-region
    "PlaceCD.Bulk"
    "Const.Bulk"
    "SubsSilicon"
)


;----------------------------------------------------
; Poly Gate Doping (Arsenic N+ 1e20 cm^-3)
;----------------------------------------------------
(sdedr:define-constant-profile
    "Const.Poly"
    "ArsenicActiveConcentration"
    1e20
)

(sdedr:define-constant-profile-region
    "PlaceCD.Poly"
    "Const.Poly"
    "PolyGate"
)


;----------------------------------------------------
; 15. Source Reference Window (Negative X matching Source contact)
;----------------------------------------------------
(sdedr:define-refeval-window
    "BaseLine.Source"
    "Rectangle"
    (position -0.30 -0.25 0.0)
    (position -0.15  0.25 0.0)
)


;----------------------------------------------------
; 16. Drain Reference Window (Positive X matching Drain contact)
;----------------------------------------------------
(sdedr:define-refeval-window
    "BaseLine.Drain"
    "Rectangle"
    (position 0.15 -0.25 0.0)
    (position 0.30  0.25 0.0)
)


;----------------------------------------------------
; 17. Gaussian Source/Drain Profile
;----------------------------------------------------
(sdedr:define-gaussian-profile
    "Gauss.SourceDrain"
    "ArsenicActiveConcentration"

    "PeakPos"       0.0
    "PeakVal"       1e19
    "ValueAtDepth"  1e17
    "Depth"         0.1

    "Gauss"
    "Factor"        0.8
)


;----------------------------------------------------
; 18. Place Source Doping
;----------------------------------------------------
(sdedr:define-analytical-profile-placement
    "PlaceAP.Source"
    "Gauss.SourceDrain"
    "BaseLine.Source"
    "Both"
    "NoReplace"
    "Eval"
)


;----------------------------------------------------
; 19. Place Drain Doping
;----------------------------------------------------
(sdedr:define-analytical-profile-placement
    "PlaceAP.Drain"
    "Gauss.SourceDrain"
    "BaseLine.Drain"
    "Both"
    "NoReplace"
    "Eval"
)


;====================================================
; 20. 3D MESH REFINEMENT CRITERIA
;====================================================

;----------------------------------------------------
; Global Mesh Window & Refinement
;----------------------------------------------------
(sdedr:define-refeval-window
    "RefWin.Global"
    "Cuboid"
    (position -0.25 -0.20 -1.0)
    (position  0.25  0.20  0.1)
)

(sdedr:define-refinement-size
    "RefDef.Global"
    0.1  0.1  0.1
    0.05 0.05 0.05
)

(sdedr:define-refinement-placement
    "Place.Global"
    "RefDef.Global"
    "RefWin.Global"
)


;----------------------------------------------------
; Active Region Refinement
;----------------------------------------------------
(sdedr:define-refeval-window
    "RefWin.Active"
    "Cuboid"
    (position -0.25 -0.20 -0.15)
    (position  0.25  0.20  0.0)
)

(sdedr:define-refinement-size
    "RefDef.Active"
    0.025  0.025  0.025
    0.0125 0.0125 0.0125
)

(sdedr:define-refinement-placement
    "Place.Active"
    "RefDef.Active"
    "RefWin.Active"
)


;----------------------------------------------------
; Channel Refinement & Multibox
;----------------------------------------------------
(sdedr:define-refeval-window
    "RefWin.Channel"
    "Cuboid"
    (position -0.12 -0.10 -0.05)
    (position  0.12  0.10  0.0)
)

(sdedr:define-multibox-size
    "RefDefMB.Channel"
    0.1  0.1  0.01
    0.05 0.05 0.001
    1 1 -1.5
)

(sdedr:define-multibox-placement
    "PlaceMB.Channel"
    "RefDefMB.Channel"
    "RefWin.Channel"
)


;====================================================
; 21. BUILD MESH AND SAVE MODEL
;====================================================
(sde:save-model "n@node@")
(sde:build-mesh "n@node@")
