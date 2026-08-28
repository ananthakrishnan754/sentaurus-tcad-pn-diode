; ============================================================
; FILE:    sde/sde_dvs.cmd
; TOOL:    Sentaurus Device Editor (SDE)
; PURPOSE: Define the geometry, doping, and contacts of a
;          2D Vertical PIN Photodiode (P+ / Intrinsic / N+).
;
; WORKBENCH VARIABLE: @mat@ is replaced by SWB with one of:
;          Silicon | Germanium | GaAs | SiC4H
;
; OUTPUT:  MaterialDiode_bnd.tdr  (boundary/geometry file)
;          MaterialDiode_dop.tdr  (doping file)
;          Both are fed to SMesh as inputs.
; ============================================================


; ============================================================
; SECTION 1: DEVICE DIMENSIONS
; PIN Photodiode structure:
;   P+ Region: Top 0.2 µm (y = 0.0 to 0.2 µm)
;   I Region:  Middle 0.6 µm (y = 0.2 to 0.8 µm) - Absorption Layer
;   N+ Region: Bottom 0.2 µm (y = 0.8 to 1.0 µm)
; ============================================================

(define xmin 0.0)    ; left edge of device (µm)
(define xmax 1.0)    ; right edge of device (1 µm wide)
(define ymin 0.0)    ; top edge of device (anode side)
(define y_p_i 0.2)   ; P+ to Intrinsic interface boundary (y = 0.2 µm)
(define y_i_n 0.8)   ; Intrinsic to N+ interface boundary (y = 0.8 µm)
(define ymax 1.0)    ; bottom edge of device (cathode side)


; ============================================================
; SECTION 2: CREATE SEMICONDUCTOR REGIONS
; ============================================================

; --- P+ Region (Top: y = 0.0 to 0.2 µm) ---
(sdegeo:create-rectangle
    (position xmin ymin 0)     ; top-left  = (0.0, 0.0)
    (position xmax y_p_i 0)    ; bot-right = (1.0, 0.2)
    "@mat@"                    ; material from Workbench variable
    "P_Region")                ; region label

; --- Intrinsic Region (Middle: y = 0.2 to 0.8 µm) ---
(sdegeo:create-rectangle
    (position xmin y_p_i 0)    ; top-left  = (0.0, 0.2)
    (position xmax y_i_n 0)    ; bot-right = (1.0, 0.8)
    "@mat@"                    ; same material
    "I_Region")                ; intrinsic absorption region

; --- N+ Region (Bottom: y = 0.8 to 1.0 µm) ---
(sdegeo:create-rectangle
    (position xmin y_i_n 0)    ; top-left  = (0.0, 0.8)
    (position xmax ymax 0)     ; bot-right = (1.0, 1.0)
    "@mat@"                    ; same material
    "N_Region")                ; region label


; ============================================================
; SECTION 3: DEFINE DOPING PROFILES
; P+ doping  : 1e18 cm^-3 (Boron)
; Intrinsic  : 1e13 cm^-3 (Light background Phosphorus)
; N+ doping  : 1e18 cm^-3 (Phosphorus)
; ============================================================

; --- P+ Doping: Boron at 1e18 cm^-3 in P_Region ---
(sdedr:define-constant-profile
    "BoronProfile"
    "BoronActiveConcentration"
    1e18)              ; 1×10^18 cm^-3 — heavy p-type doping

(sdedr:define-constant-profile-region
    "BoronPlacement"
    "BoronProfile"
    "P_Region")

; --- Intrinsic Doping: Light background Phosphorus at 1e13 cm^-3 ---
(sdedr:define-constant-profile
    "IntrinsicProfile"
    "PhosphorusActiveConcentration"
    1e13)              ; 1×10^13 cm^-3 — lightly-doped intrinsic region

(sdedr:define-constant-profile-region
    "IntrinsicPlacement"
    "IntrinsicProfile"
    "I_Region")

; --- N+ Doping: Phosphorus at 1e18 cm^-3 in N_Region ---
(sdedr:define-constant-profile
    "PhosphorusProfile"
    "PhosphorusActiveConcentration"
    1e18)              ; 1×10^18 cm^-3 — heavy n-type doping

(sdedr:define-constant-profile-region
    "PhosphorusPlacement"
    "PhosphorusProfile"
    "N_Region")


; ============================================================
; SECTION 4: DEFINE METAL CONTACTS
; ============================================================

; --- Anode Contact: top edge of P_Region (y = 0.0) ---
(sdegeo:define-contact-set "Anode" 4 (color:rgb 1 0 0) "##")
(sdegeo:set-current-contact-set "Anode")
(sdegeo:set-contact-edges
    (find-edge-id (position 0.5 0.0 0)))

; --- Cathode Contact: bottom edge of N_Region (y = 1.0) ---
(sdegeo:define-contact-set "Cathode" 4 (color:rgb 0 0 1) "##")
(sdegeo:set-current-contact-set "Cathode")
(sdegeo:set-contact-edges
    (find-edge-id (position 0.5 1.0 0)))


; ============================================================
; SECTION 5: MESH REFINEMENT WINDOWS
; Fine mesh in the Intrinsic region & around P-I / I-N junctions
; ============================================================

; --- Fine mesh window covering Intrinsic layer (y = 0.15 to 0.85 µm) ---
(sdedr:define-refinement-window
    "IRefineWindow"
    "Rectangle"
    (position 0.0 0.15 0)
    (position 1.0 0.85 0))

(sdedr:define-refinement-size
    "IRefineSize"
    0.01                     ; max element size = 10 nm inside absorption region
    0.005)                   ; min element size = 5 nm

(sdedr:define-refinement-region
    "IRefinePlacement"
    "IRefineSize"
    "IRefineWindow")

; --- Global bulk mesh window ---
(sdedr:define-refinement-window
    "BulkRefineWindow"
    "Rectangle"
    (position 0.0 0.0 0)
    (position 1.0 1.0 0))

(sdedr:define-refinement-size
    "BulkRefineSize"
    0.04                     ; max element size = 40 nm
    0.01)                    ; min element size = 10 nm

(sdedr:define-refinement-region
    "BulkRefinePlacement"
    "BulkRefineSize"
    "BulkRefineWindow")


; ============================================================
; SECTION 6: SAVE THE STRUCTURE
; ============================================================

(sde:save-model "MaterialDiode")

; ============================================================
; END OF SDE SCRIPT
; ============================================================

