; ============================================================
; FILE:    sde/sde_dvs.cmd
; TOOL:    Sentaurus Device Editor (SDE)
; PURPOSE: Define the geometry, doping, and contacts of a
;          vertical PN junction diode.
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
; We define the device as a 2D cross-section (X-Y plane).
; X = width direction (horizontal)
; Y = depth direction (vertical, downward is positive)
;
; Coordinate system in SDE:
;   Origin (0,0) is at the TOP-LEFT corner.
;   Y increases DOWNWARD (into the device).
; ============================================================

; --- Define key dimension variables ---
; These make it easy to change the geometry in one place.

(define xmin 0.0)    ; left edge of device, in micrometers
(define xmax 1.0)    ; right edge of device, 1 µm wide
(define ymin 0.0)    ; top edge of device (anode side)
(define yjunc 0.5)   ; Y position of the PN junction
(define ymax 1.0)    ; bottom edge of device (cathode side)

; WHY THESE VALUES?
; 1 µm × 1 µm is tiny enough to mesh fast and solve quickly.
; The junction is at the midpoint (0.5 µm) for symmetry.
; We use micrometers (µm) because Sentaurus defaults to µm.


; ============================================================
; SECTION 2: CREATE SEMICONDUCTOR REGIONS
; Each "sdegeo:create-rectangle" command draws a rectangular
; region and assigns it a material and a name.
;
; Syntax:
;   (sdegeo:create-rectangle
;     (position x1 y1 0)   ; top-left corner
;     (position x2 y2 0)   ; bottom-right corner
;     "MaterialName"        ; Sentaurus material database name
;     "RegionName")         ; your label for this region
;
; The third coordinate is always 0 for 2D simulations.
; ============================================================

; --- P-type region (top half: y = 0 to 0.5 µm) ---
(sdegeo:create-rectangle
    (position xmin ymin 0)     ; top-left  = (0.0, 0.0)
    (position xmax yjunc 0)    ; bot-right = (1.0, 0.5)
    "@mat@"                    ; material from Workbench variable
    "P_Region")                ; region label

; NOTE: When SWB runs this with @mat@ = "Silicon", Sentaurus
; looks up "Silicon" in its built-in material database and
; assigns all Si properties (bandgap, mobility, etc.) to this
; region automatically. This is why we use the Workbench
; variable — same script, 4 different materials.


; --- N-type region (bottom half: y = 0.5 to 1.0 µm) ---
(sdegeo:create-rectangle
    (position xmin yjunc 0)    ; top-left  = (0.0, 0.5)
    (position xmax ymax 0)     ; bot-right = (1.0, 1.0)
    "@mat@"                    ; same material as P-region
    "N_Region")                ; region label

; IMPORTANT: Both regions use the same semiconductor material.
; The difference between P and N comes ONLY from doping,
; which we define in Section 3 below.
; The material itself (band structure, mobility) is identical.


; ============================================================
; SECTION 3: DEFINE DOPING PROFILES
; We use uniform (constant) doping for simplicity.
; In a real device, doping would have Gaussian profiles
; from ion implantation, but uniform doping is the correct
; starting point for understanding device physics.
;
; Syntax:
;   (sdedr:define-constant-profile
;     "ProfileName"   ; label for this doping specification
;     "DopantName"    ; "BoronActiveConcentration" or
;                     ; "PhosphorusActiveConcentration"
;     concentration)  ; in cm^-3
;
;   (sdedr:define-constant-profile-region
;     "PlacementName" ; label for this placement
;     "ProfileName"   ; which profile to apply
;     "RegionName")   ; which region to apply it to
; ============================================================

; --- P-type doping: Boron at 1e17 cm^-3 in P_Region ---
(sdedr:define-constant-profile
    "BoronProfile"
    "BoronActiveConcentration"
    1e17)              ; 1×10^17 cm^-3 — moderate p-type doping

(sdedr:define-constant-profile-region
    "BoronPlacement"
    "BoronProfile"
    "P_Region")

; WHY 1e17?
; This gives a hole concentration of ~1e17 cm^-3 in the P-side.
; It's a realistic doping for a standard PN diode.
; Too high (>1e19) causes heavy doping effects and degeneracy.
; Too low (<1e14) makes the depletion approximation break down.


; --- N-type doping: Phosphorus at 1e16 cm^-3 in N_Region ---
(sdedr:define-constant-profile
    "PhosphorusProfile"
    "PhosphorusActiveConcentration"
    1e16)              ; 1×10^16 cm^-3 — lighter n-type doping

(sdedr:define-constant-profile-region
    "PhosphorusPlacement"
    "PhosphorusProfile"
    "N_Region")

; WHY 1e16 (lower than P-side)?
; An asymmetric junction (Na >> Nd) is called a p+n junction.
; The depletion region extends further into the lighter-doped
; N-side. This is very common in real devices (like solar cells).
; It also makes your electric field profile more interesting to
; analyze — the peak field is at the junction, asymmetrically.


; ============================================================
; SECTION 4: DEFINE METAL CONTACTS
; Contacts are boundaries where external voltage is applied.
; We define them on the TOP edge (Anode) and BOTTOM edge
; (Cathode) of the device.
;
; Syntax:
;   (sdegeo:define-contact-set "ContactName" ...)
;   (sdegeo:set-current-contact-set "ContactName")
;   (sdegeo:set-contact-edges (find-edge-id ...))
;
; The easiest way is to use the built-in edge-finding function.
; ============================================================

; --- Anode contact: top edge of P_Region (y = 0.0) ---
(sdegeo:define-contact-set "Anode" 4  (color:rgb 1 0 0) "##")
(sdegeo:set-current-contact-set "Anode")
(sdegeo:set-contact-edges
    (find-edge-id (position 0.5 0.0 0)))
; The (position 0.5 0.0 0) picks any point ON the top edge.
; SDE finds the edge that passes through that point and
; marks the entire edge as the "Anode" contact.
; Color (1 0 0) = red in the SDE viewer — just for visualization.


; --- Cathode contact: bottom edge of N_Region (y = 1.0) ---
(sdegeo:define-contact-set "Cathode" 4  (color:rgb 0 0 1) "##")
(sdegeo:set-current-contact-set "Cathode")
(sdegeo:set-contact-edges
    (find-edge-id (position 0.5 1.0 0)))
; Same idea — pick a point on the bottom edge (y = 1.0).
; Color (0 0 1) = blue.


; ============================================================
; SECTION 5: MESH REFINEMENT WINDOWS
; A mesh refinement window tells SMesh (the mesher) to use
; finer mesh elements in a specific region.
;
; The most critical area is the PN JUNCTION (around y = 0.5).
; The depletion region, electric field peak, and all the
; interesting physics happen there. A coarse mesh there will
; give wrong results.
;
; We define a thin window around the junction and ask for
; fine mesh inside it.
; ============================================================

; --- Fine mesh window around the PN junction ---
(sdedr:define-refinement-window
    "JunctionRefine"         ; name for this refinement
    "Rectangle"              ; shape
    (position 0.0 0.4 0)     ; top-left  (start 0.1 µm above junction)
    (position 1.0 0.6 0))    ; bot-right (end  0.1 µm below junction)

(sdedr:define-refinement-size
    "JunctionRefineSize"
    0.01                     ; maximum element size = 10 nm in this window
    0.005)                   ; minimum element size = 5 nm

(sdedr:define-refinement-region
    "JunctionRefinePlacement"
    "JunctionRefineSize"
    "JunctionRefine")

; WHY 10 nm near the junction?
; The depletion width in Si at Na=1e17, Nd=1e16 is ~0.35 µm.
; To accurately resolve the electric field, we need at least
; 10-20 mesh points across the depletion region.
; 10 nm spacing × 35 points = good resolution.

; --- Coarser mesh in the bulk regions ---
; Outside the junction, the physics is boring (mostly flat
; potential, uniform carrier concentration). We can use a
; coarser mesh to save simulation time.

(sdedr:define-refinement-window
    "BulkRefine"
    "Rectangle"
    (position 0.0 0.0 0)
    (position 1.0 1.0 0))

(sdedr:define-refinement-size
    "BulkRefineSize"
    0.05                     ; max element size = 50 nm in bulk
    0.02)                    ; min element size = 20 nm

(sdedr:define-refinement-region
    "BulkRefinePlacement"
    "BulkRefineSize"
    "BulkRefine")

; NOTE: Both windows overlap. In the junction region,
; the FINER mesh (JunctionRefine = 10 nm) wins because
; SMesh always applies the most restrictive constraint.


; ============================================================
; SECTION 6: SAVE THE STRUCTURE
; This command writes the final geometry + doping + contact
; information to the two output .tdr files.
;
; The file names follow the SWB naming convention:
;   <ProjectName>_bnd.tdr  = boundary file (geometry)
;   <ProjectName>_dop.tdr  = doping profile file
; ============================================================

(sde:save-model "MaterialDiode")

; WHAT HAPPENS AFTER THIS:
; SWB reads these two files and passes them to SMesh.
; SMesh uses the boundary file to know the device shape,
; and uses the doping file to know the doping at every mesh point.
; The junction refinement windows you defined above are also
; embedded in these files so SMesh knows where to refine.

; ============================================================
; END OF SDE SCRIPT
; ============================================================
