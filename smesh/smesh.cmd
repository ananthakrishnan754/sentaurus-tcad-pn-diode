; ============================================================
; FILE:    smesh/smesh.cmd
; TOOL:    Sentaurus Mesher (SMesh / SNode)
; PURPOSE: Control how the mesh is generated from the SDE
;          geometry output. Defines global mesh quality rules
;          and saves the final mesh file for SDevice.
;
; INPUT:   MaterialDiode_bnd.tdr  (from SDE)
;          MaterialDiode_dop.tdr  (from SDE)
;
; OUTPUT:  MaterialDiode_msh.tdr  (mesh file for SDevice)
; ============================================================


; ============================================================
; SECTION 1: LOAD THE SDE OUTPUT FILES
; We must tell SMesh which files to read from SDE.
; The file names here MUST match what SDE wrote in its
; (sde:save-model "MaterialDiode") command.
; ============================================================

(sde:set-meshing-attributes
    -mode      snmesh          ; use the SNMesh meshing engine
    -boundary  "MaterialDiode_bnd.tdr"
    -doping    "MaterialDiode_dop.tdr")

; WHY snmesh?
; Sentaurus has two mesh engines: snmesh and mdmesh.
; snmesh (Sentaurus N-Mesh) is the standard choice for 2D
; device simulations. It produces Delaunay triangular meshes
; which are well-suited for the finite-element method used
; by SDevice.
; mdmesh is used for 3D simulations — we don't need it here.


; ============================================================
; SECTION 2: GLOBAL MESH QUALITY PARAMETERS
; These parameters control the overall quality of triangles
; in the mesh. Poor quality triangles (very thin or very
; elongated) cause numerical errors in the solver.
;
; Key concept — Delaunay criterion:
; Every triangle in the mesh should be as close to equilateral
; as possible. Elongated triangles with very sharp angles cause
; large numerical errors in gradient calculations.
; ============================================================

(snmesh:set-meshing-options
    -max-angle    150          ; maximum interior angle of any triangle (degrees)
    -min-edge     0.0001       ; minimum allowed edge length (µm) = 0.1 nm
    -max-edge     0.1          ; maximum allowed edge length (µm) = 100 nm
    -max-area     0.005)       ; maximum triangle area (µm²)

; EXPLANATION OF EACH PARAMETER:
;
; -max-angle 150:
;   No triangle should have an interior angle greater than 150°.
;   Angles above 120° start causing numerical problems.
;   150° is a reasonable limit — strict enough to avoid bad
;   triangles, loose enough to let the mesher work efficiently.
;
; -min-edge 0.0001:
;   No edge (side of a triangle) can be shorter than 0.1 nm.
;   This prevents the mesher from creating infinitesimally thin
;   triangles that would cause division-by-zero errors.
;
; -max-edge 0.1:
;   No edge can be longer than 100 nm anywhere in the device.
;   This is your global upper limit — even in the bulk where
;   we don't care about fine detail, edges won't exceed 100 nm.
;   Note: the refinement windows from SDE already force finer
;   mesh near the junction. This is just the absolute maximum.
;
; -max-area 0.005:
;   No triangle can cover an area larger than 0.005 µm².
;   This is a secondary quality check to prevent large, flat
;   triangles in the bulk regions.


; ============================================================
; SECTION 3: INTERFACE REFINEMENT
; Boundary 1: P_Region / I_Region interface at y = 0.2 µm
; Boundary 2: I_Region / N_Region interface at y = 0.8 µm
; ============================================================

(sdedr:define-refinement-interface
    "PI_JunctionInterface"       ; P-I junction interface
    "P_Region"                   ; first region
    "I_Region"                   ; second region
    0.005                        ; max element size at interface = 5 nm
    0.002)                       ; min element size at interface = 2 nm

(sdedr:define-refinement-interface
    "IN_JunctionInterface"       ; I-N junction interface
    "I_Region"                   ; first region
    "N_Region"                   ; second region
    0.005                        ; max element size at interface = 5 nm
    0.002)                       ; min element size at interface = 2 nm



; ============================================================
; SECTION 4: CONTACT REFINEMENT
; Near the metal contacts (Anode at y=0, Cathode at y=1),
; there is also rapid variation — the quasi-Fermi levels
; transition from their bulk values to the contact value.
; We refine the mesh near contacts as well.
; ============================================================

(sdedr:define-refinement-interface
    "AnodeInterface"
    "Anode"                      ; metal contact region
    "P_Region"                   ; adjacent semiconductor
    0.01                         ; max 10 nm near the contact
    0.005)                       ; min 5 nm right at the contact

(sdedr:define-refinement-interface
    "CathodeInterface"
    "Cathode"
    "N_Region"
    0.01
    0.005)

; WHY REFINE NEAR CONTACTS?
; Contacts impose a Dirichlet boundary condition on the
; potential (fixed voltage). Near an ohmic contact, the
; carrier concentration is forced to its equilibrium value.
; This creates a sharp spatial transition if there is any
; voltage applied. Fine mesh there avoids numerical kinks
; in the solution near the contacts.


; ============================================================
; SECTION 5: DOPING GRADIENT REFINEMENT
; This is the most physically motivated refinement.
; We ask SMesh to automatically refine the mesh wherever
; the doping changes rapidly.
;
; In our device, the doping changes sharply at y = 0.5 µm
; (from 1e17 on P-side to 1e16 on N-side). The mesh should
; be finer wherever the logarithm of doping changes fast.
; ============================================================

(sdedr:define-refinement-function
    "DopingGradRefine"           ; name for this rule
    "DopingConcentration"        ; the quantity to watch
    "MaxTransDiff"  1.0          ; max allowed log10 change per element
    "MaxValue"      1e20         ; ignore regions with doping above this
    "MinValue"      1e10)        ; ignore regions with doping below this

; HOW MaxTransDiff WORKS:
; If the doping changes by more than 10^1.0 = 10x across a
; single mesh element, that element is too coarse and will be
; automatically split into smaller triangles.
; This ensures smooth representation of the doping profile.
;
; Setting MaxTransDiff = 1.0 means:
; If doping changes by more than 10x across one triangle,
; SMesh splits it. This is a tight but reasonable constraint
; for an abrupt junction.
;
; MaxValue / MinValue: we ignore very heavily or lightly
; doped regions where the gradient rule would create
; unnecessary mesh refinement in unimportant areas.


; ============================================================
; SECTION 6: GENERATE AND SAVE THE MESH
; This command triggers the actual mesh generation.
; SMesh runs its meshing algorithm using all the constraints
; defined above and saves the result.
; ============================================================

(sde:build-mesh
    -mesh    "snmesh"
    -model   "MaterialDiode")

; WHAT THIS PRODUCES:
; A file called MaterialDiode_msh.tdr
; This is the ONLY file SDevice needs. It contains:
;   - All mesh node positions (x, y coordinates)
;   - Which nodes form each triangle
;   - The doping value at every node
;   - The region label at every node (P_Region or N_Region)
;   - The contact assignment at boundary nodes
;
; TYPICAL MESH SIZE FOR THIS DEVICE:
; With the settings above, expect roughly 8,000 to 15,000
; mesh nodes and 15,000 to 30,000 triangles.
; This is small enough to run an I-V sweep in 2-5 minutes.


; ============================================================
; SECTION 7: MESH VERIFICATION (OPTIONAL BUT RECOMMENDED)
; After meshing, it's good practice to check if the mesh
; quality is acceptable before running SDevice.
; SDE/SMesh can report mesh statistics.
; ============================================================

(sde:display-mesh-info)

; This prints to the SWB log window:
;   - Total number of nodes
;   - Total number of triangles
;   - Minimum and maximum element sizes
;   - Any mesh quality warnings
;
; WHAT TO LOOK FOR:
; If you see warnings like "poor quality elements detected"
; or "mesh quality threshold violated", the mesh has some
; bad triangles. This can cause SDevice convergence problems.
; The fix is usually to reduce -max-angle or -max-edge.
;
; If the node count is VERY large (>100,000 for this small
; device), something is wrong — likely a refinement window
; is too aggressive. That makes simulation very slow.

; ============================================================
; END OF SMESH SCRIPT
; ============================================================
