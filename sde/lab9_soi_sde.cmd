;======================================================================
; SOI MOSFET -- SENTARUS STRUCTURE EDITOR (SDE)
; Labsheet 9: SOI MOSFET Structure, Doping & Mesh Generation
; Verified on Synopsys Sentaurus Structure Editor (N-2017.09)
;======================================================================

(sde:clear)

;----------------------------------------------------------------------
; 1. Device Parameters
;----------------------------------------------------------------------
(define Lch     0.18)   ; Channel length [um]
(define Tox     0.004)  ; Gate oxide thickness [um] (4 nm)
(define Hepi    0.05)   ; SOI silicon film thickness [um] (50 nm)
(define Hbox    0.1)    ; Buried oxide (BOX) thickness [um] (100 nm)
(define Hsub    0.2)    ; Substrate thickness [um] (200 nm)
(define Hpol    0.1)    ; Polygate thickness [um] (100 nm)
(define Lcont   0.2)    ; S/D contact length [um]
(define EpiDop  1e17)   ; Body doping [cm^-3]
(define Gpn     5e-4)   ; Min mesh size at pn junction [um]

;--- Derived Coordinates ---
(define Xg      (/ Lch 2.0))          ; Gate half-width
(define Xsp     (+ Xg 0.01))          ; S/D edge (inner)
(define Xmax    (+ Xsp Lcont))        ; Device half-width
(define Ltot    (* 2.0 Xmax))
(define Lgox    Xg)
(define Xbc1    (+ Xg (* Lcont 0.3))) ; Body tie inner
(define Xbc2    (+ Xg (* Lcont 0.7))) ; Body tie outer

;--- Y coordinates (0=top surface of Silicon film) ---
(define Ygox   (- 0.0 Tox))           ; Gate oxide top
(define Ypol   (- Ygox Hpol))         ; Polygate top
(define Yepi   Hepi)                  ; SOI layer bottom
(define Ybox   (+ Yepi Hbox))         ; BOX bottom
(define Ysub   (+ Ybox Hsub))         ; Substrate bottom

;----------------------------------------------------------------------
; 2. Geometry Construction
;----------------------------------------------------------------------

; --- Silicon Substrate ---
(sdegeo:create-rectangle
  (position (* Xmax -1.0) Ybox 0.0)
  (position (* Xmax  1.0) Ysub 0.0)
  "Silicon" "R.Substrate")

; --- Buried Oxide (BOX) ---
(sdegeo:create-rectangle
  (position (* Xmax -1.0) Yepi 0.0)
  (position (* Xmax  1.0) Ybox 0.0)
  "SiO2" "R.Box")

; --- SOI Silicon Thin Film (Epi) ---
(sdegeo:create-rectangle
  (position (* Xmax -1.0) 0.0  0.0)
  (position (* Xmax  1.0) Yepi 0.0)
  "Silicon" "R.Siliconepi")

; --- Gate Oxide ---
(sdegeo:create-rectangle
  (position (* Xg -1.0) Ygox 0.0)
  (position (* Xg  1.0) 0.0  0.0)
  "SiO2" "R.Gateox")

; --- Polysilicon Gate ---
(sdegeo:create-rectangle
  (position (* Xg -1.0) Ypol 0.0)
  (position (* Xg  1.0) Ygox 0.0)
  "PolySi" "R.Polygate")

;----------------------------------------------------------------------
; 3. Contact Sets & Boundary Definitions
;----------------------------------------------------------------------
(sdegeo:define-contact-set "source"    4 (color:rgb 1 0 0) "##")
(sdegeo:define-contact-set "drain"     4 (color:rgb 0 0 1) "##")
(sdegeo:define-contact-set "gate"      4 (color:rgb 0 1 0) "##")
(sdegeo:define-contact-set "substrate" 4 (color:rgb 0 1 1) "##")
(sdegeo:define-contact-set "bodytie"   4 (color:rgb 1 1 0) "##")

; Source Contact (Left top edge of Silicon film)
(sdegeo:set-current-contact-set "source")
(sdegeo:set-contact
  (find-edge-id (position (* (+ (* Xsp -1.0) (* Xmax -1.0)) 0.5) 0.0 0.0))
  "source")

; Drain Contact (Right top edge of Silicon film)
(sdegeo:set-current-contact-set "drain")
(sdegeo:set-contact
  (find-edge-id (position (* (+ Xsp Xmax) 0.5) 0.0 0.0))
  "drain")

; Gate Contact (Top edge of Polygate)
(sdegeo:set-current-contact-set "gate")
(sdegeo:set-contact
  (find-edge-id (position 0.0 Ypol 0.0))
  "gate")

; Substrate Back Contact (Bottom edge of Substrate)
(sdegeo:set-current-contact-set "substrate")
(sdegeo:set-contact
  (find-edge-id (position 0.0 Ysub 0.0))
  "substrate")

; Body Tie Contact (Bottom boundary of SOI Silicon film)
(sdegeo:insert-vertex (position Xbc1 Yepi 0.0))
(sdegeo:insert-vertex (position Xbc2 Yepi 0.0))
(sdegeo:set-current-contact-set "bodytie")
(sdegeo:set-contact
  (find-edge-id (position (* (+ Xbc1 Xbc2) 0.5) Yepi 0.0))
  "bodytie")

;----------------------------------------------------------------------
; 4. Doping Profiles
;----------------------------------------------------------------------

; Substrate background doping (Boron P-type 1e16 cm^-3)
(sdedr:define-constant-profile "Const.Substrate"
  "BoronActiveConcentration" 1e16)
(sdedr:define-constant-profile-region "PlaceCD.Substrate"
  "Const.Substrate" "R.Substrate")

; SOI Silicon film body doping (Boron P-type 1e17 cm^-3)
(sdedr:define-constant-profile "Const.SiEpi"
  "BoronActiveConcentration" EpiDop)
(sdedr:define-constant-profile-region "PlaceCD.SiEpi"
  "Const.SiEpi" "R.Siliconepi")

; Polysilicon gate doping (Arsenic N+ 1e20 cm^-3)
(sdedr:define-constant-profile "Const.Gate"
  "ArsenicActiveConcentration" 1e20)
(sdedr:define-constant-profile-region "PlaceCD.Gate"
  "Const.Gate" "R.Polygate")

; Source baseline
(sdedr:define-refeval-window "BaseLine.Source" "Line"
  (position (* Xmax -2.0) 0.0 0.0)
  (position (* Xsp  -1.0) 0.0 0.0))

; Drain baseline
(sdedr:define-refeval-window "BaseLine.Drain" "Line"
  (position Xsp 0.0 0.0)
  (position (* Xmax 2.0) 0.0 0.0))

; Source/Drain Gaussian profile (Phosphorus N+ 1e20 cm^-3)
(sdedr:define-gaussian-profile "Impl.SDprof"
  "PhosphorusActiveConcentration"
  "PeakPos" 0 "PeakVal" 1e20
  "ValueAtDepth" EpiDop "Depth" (* Hepi 1.2)
  "Gauss" "Factor" 0.4)

(sdedr:define-analytical-profile-placement "Impl.Source"
  "Impl.SDprof" "BaseLine.Source" "Symm" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "Impl.Drain"
  "Impl.SDprof" "BaseLine.Drain" "Symm" "NoReplace" "Eval")

; Source/Drain extension baselines
(sdedr:define-refeval-window "BaseLine.SourceExt" "Line"
  (position (* Xmax -2.0) 0.0 0.0)
  (position (* Xg   -1.0) 0.0 0.0))
(sdedr:define-refeval-window "BaseLine.DrainExt" "Line"
  (position Xg 0.0 0.0)
  (position (* Xmax 2.0) 0.0 0.0))

; S/D extension (arsenic halo)
(sdedr:define-gaussian-profile "Impl.SDextprof"
  "ArsenicActiveConcentration"
  "PeakPos" 0 "PeakVal" 5e18
  "ValueAtDepth" EpiDop "Depth" (* Hepi 0.35)
  "Gauss" "Factor" 0.8)

(sdedr:define-analytical-profile-placement "Impl.SourceExt"
  "Impl.SDextprof" "BaseLine.SourceExt" "Symm" "NoReplace" "Eval")
(sdedr:define-analytical-profile-placement "Impl.DrainExt"
  "Impl.SDextprof" "BaseLine.DrainExt" "Symm" "NoReplace" "Eval")

;----------------------------------------------------------------------
; 5. Meshing Strategy
;----------------------------------------------------------------------

; Substrate Refinement
(sdedr:define-refinement-size "Ref.Substrate"
  (/ Ltot 4.0) (/ Hsub 8.0)
  Gpn Gpn)
(sdedr:define-refinement-function "Ref.Substrate"
  "DopingConcentration" "MaxTransDiff" 1)
(sdedr:define-refinement-region "RefPlace.Substrate"
  "Ref.Substrate" "R.Substrate")

; Buried Oxide Refinement
(sdedr:define-refinement-size "Ref.BOX"
  (/ Ltot 4.0) (/ Hbox 4.0)
  Gpn Gpn)
(sdedr:define-refinement-region "RefPlace.BOX"
  "Ref.BOX" "R.Box")

; SOI Silicon Film Refinement
(sdedr:define-refinement-size "Ref.SiEpi"
  (/ Lcont 4.0) (/ Hepi 8.0)
  Gpn Gpn)
(sdedr:define-refinement-function "Ref.SiEpi"
  "DopingConcentration" "MaxTransDiff" 1)
(sdedr:define-refinement-region "RefPlace.SiEpi"
  "Ref.SiEpi" "R.Siliconepi")

; Gate Oxide Refinement
(sdedr:define-refinement-size "Ref.GOX"
  (/ Ltot 4.0) (/ Tox 4.0)
  Gpn (/ Tox 8.0))
(sdedr:define-refinement-region "RefPlace.GOX"
  "Ref.GOX" "R.Gateox")

; Gate Poly Multibox
(sdedr:define-refeval-window "MBWindow.Gate" "Rectangle"
  (position (* Xg -1.0) Ypol 0.0)
  (position (* Xg  1.0) Ygox 0.0))
(sdedr:define-multibox-size "MBSize.Gate"
  (/ Lch 4.0) (/ Hpol 8.0)
  (/ Lch 8.0) 2e-4
  1.0 -1.35)
(sdedr:define-multibox-placement "MBPlace.Gate"
  "MBSize.Gate" "MBWindow.Gate")

; Channel Multibox
(sdedr:define-refeval-window "MBWindow.Channel" "Rectangle"
  (position (* Xg -1.2) 0.0 0.0)
  (position (* Xg  1.2) Yepi 0.0))
(sdedr:define-multibox-size "MBSize.Channel"
  (/ Lch 8.0) (/ Hepi 8.0)
  (/ Lch 10.0) 1e-4
  1.0 1.35)
(sdedr:define-multibox-placement "MBPlace.Channel"
  "MBSize.Channel" "MBWindow.Channel")

;----------------------------------------------------------------------
; 6. Build Mesh and Save Model
;----------------------------------------------------------------------
(sde:save-model "n@node@")
(sde:build-mesh "n@node@")
