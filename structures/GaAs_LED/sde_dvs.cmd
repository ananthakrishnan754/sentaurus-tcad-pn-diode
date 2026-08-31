;; ============================================================
;; FILE:    structures/GaAs_LED/sde_dvs.cmd
;; TOOL:    Sentaurus Structure Editor (SDE)
;; PURPOSE: Define 3D Bulk PIN Light Emitting Diode (LED) for GaAs
;; ============================================================

(sde:clear)

;; 1. Geometric Dimensions (Units: micrometers)
(define xmin 0.0)
(define xmax 1.0)
(define ymin 0.0)
(define y_p_i 0.15)
(define y_i_n 0.35)
(define ymax 0.5)
(define zmin 0.0)
(define zmax 0.5)

;; 2. Region Definitions - 3D GaAs Bulk Material
(sdegeo:create-cuboid (position xmin ymin zmin) (position xmax y_p_i zmax) "GaAs" "P_Region")
(sdegeo:create-cuboid (position xmin y_p_i zmin) (position xmax y_i_n zmax) "GaAs" "I_Active_Region")
(sdegeo:create-cuboid (position xmin y_i_n zmin) (position xmax ymax zmax) "GaAs" "N_Region")

;; 3. Doping Profile Definitions
(sdedr:define-constant-profile "P_Doping" "CarbonActiveConcentration" 2e18)
(sdedr:define-constant-profile-region "P_Placement" "P_Doping" "P_Region")

(sdedr:define-constant-profile "I_Doping" "SiliconActiveConcentration" 1e14)
(sdedr:define-constant-profile-region "I_Placement" "I_Doping" "I_Active_Region")

(sdedr:define-constant-profile "N_Doping" "SiliconActiveConcentration" 2e18)
(sdedr:define-constant-profile-region "N_Placement" "N_Doping" "N_Region")

;; 4. Contact Definitions (3D Face Contacts)
(sdegeo:define-contact-set "Anode" 4 (color:rgb 1 0 0) "##")
(sdegeo:set-current-contact-set "Anode")
(sdegeo:set-contact-faces (find-face-id (position 0.5 0.0 0.25)))

(sdegeo:define-contact-set "Cathode" 4 (color:rgb 0 0 1) "##")
(sdegeo:set-current-contact-set "Cathode")
(sdegeo:set-contact-faces (find-face-id (position 0.5 0.5 0.25)))

;; 5. Save Boundary & Model Files
(sde:build-mesh "snmesh" "" "GaAs_LED_msh")
(sde:save-model "GaAs_LED")
