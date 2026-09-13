#!/usr/bin/env python3
"""
generate_tcad_study_guide_pdf.py
================================================================================
Generates the Definitive TCAD Master Study & Viva Voce Defense Guide:
"Comprehensive TCAD Semiconductor Physics, Device Engineering & Simulation Study Guide"
Covers:
  - Executive Overview & The TCAD Paradigm
  - Semiconductor Physics from First Principles (Bands, Drift-Diffusion, Recombination, Breakdown)
  - Material Engineering Benchmark (Si, Ge, GaAs, 4H-SiC)
  - Device Architecture 1: Material-Engineered Diode & Optoelectronics
  - Device Architecture 2: 3D MOSFET Solid Modeling & Scaling Physics (Labsheet 8)
  - Device Architecture 3: Silicon-on-Insulator (SOI) MOSFET & Floating Body Physics (Labsheet 9)
  - Synopsys Sentaurus TCAD Suite Mechanics (SDE, SNMESH, SDevice, SVisual, SWB, VM)
  - Physical Models & Numerical Solver Mechanics in SDevice
  - Exact Geometric Dimensions, Doping Profiles & Settings Table
  - High-Yield Viva Voce Question Bank (30+ Exhaustive Technical Defenses & Model Answers)
  - Formula Quick-Reference Card

Output: TCAD_Comprehensive_Study_and_Viva_Defense_Guide.pdf
================================================================================
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
PDF_OUTPUT = os.path.join(BASE_DIR, "TCAD_Comprehensive_Study_and_Viva_Defense_Guide.pdf")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 755, "SENTAURUS TCAD MASTER STUDY GUIDE: PHYSICS, MODELING & VIVA DEFENSE")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.75)
            self.line(40, 747, 572, 747)

        # Running Footer (all pages)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(572, 30, page_str)
        self.drawString(40, 30, "M.TECH VLSI — SENTAURUS TCAD COMPREHENSIVE PROJECT REFERENCE MANUAL")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(40, 40, 572, 40)

        self.restoreState()


def get_styles():
    styles = getSampleStyleSheet()

    # Custom styles
    h1 = ParagraphStyle(
        'GuideH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0f2942'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2 = ParagraphStyle(
        'GuideH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h3 = ParagraphStyle(
        'GuideH3',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#0369a1'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'GuideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'GuideBodyBold',
        parent=body,
        fontName='Helvetica-Bold'
    )

    callout_text = ParagraphStyle(
        'GuideCallout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor('#0f172a')
    )

    callout_bold = ParagraphStyle(
        'GuideCalloutBold',
        parent=callout_text,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0369a1')
    )

    q_style = ParagraphStyle(
        'GuideQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#991b1b'),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    ans_style = ParagraphStyle(
        'GuideAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=6
    )

    table_cell = ParagraphStyle(
        'GuideTableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1e293b')
    )

    table_header = ParagraphStyle(
        'GuideTableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    code_style = ParagraphStyle(
        'GuideCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#0f172a')
    )

    return {
        'h1': h1,
        'h2': h2,
        'h3': h3,
        'body': body,
        'body_bold': body_bold,
        'callout': callout_text,
        'callout_bold': callout_bold,
        'question': q_style,
        'answer': ans_style,
        'table_cell': table_cell,
        'table_header': table_header,
        'code': code_style
    }


def make_callout(text, bold_prefix="", bg_color="#f0f9ff", border_color="#0284c7"):
    styles = get_styles()
    full_p = Paragraph(f"<b><font color='{border_color}'>{bold_prefix}</font></b> {text}", styles['callout'])
    t = Table([[full_p]], colWidths=[532])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(bg_color)),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor(border_color)),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t


def build_pdf():
    print(f"Generating Comprehensive TCAD Study & Defense Guide PDF: {PDF_OUTPUT}...")
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=42,
        bottomMargin=42
    )

    styles = get_styles()
    story = []

    # =========================================================================
    # TITLE & METADATA BLOCK
    # =========================================================================
    title_p = Paragraph(
        "SENTAURUS TCAD COMPREHENSIVE STUDY & VIVA DEFENSE GUIDE",
        ParagraphStyle(
            'TitleMain',
            fontName='Helvetica-Bold',
            fontSize=17,
            leading=21,
            textColor=colors.HexColor('#0f2942'),
            alignment=1
        )
    )
    subtitle_p = Paragraph(
        "A Complete, First-Principles Technical Manual: Semiconductor Physics, Material Engineering, 3D MOSFET & SOI Modeling, Numerical TCAD Mechanics, and Master Viva Question Bank",
        ParagraphStyle(
            'TitleSub',
            fontName='Helvetica',
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor('#334155'),
            alignment=1,
            spaceBefore=3,
            spaceAfter=6
        )
    )
    meta_p = Paragraph(
        "<b>Institution:</b> Amrita Vishwa Vidyapeetham &middot; <b>Department:</b> Electronics & Communication Engineering &middot; <b>Program:</b> M.Tech VLSI Design<br/>"
        "<b>Investigators:</b> Ananthakrishnan S (AM.EN.P2VLD260017), Sudin Santhosh (AM.EN.P2VLD260018), Adithya H Kumar (AM.EN.P2VLD260021)<br/>"
        "<b>Tool Suite:</b> Synopsys Sentaurus TCAD (SDE, SNMESH, SDevice, SVisual, SWB vN-2017.09) on RHEL 6.6",
        ParagraphStyle(
            'TitleMeta',
            fontName='Helvetica',
            fontSize=7.8,
            leading=11,
            textColor=colors.HexColor('#475569'),
            alignment=1
        )
    )

    meta_table = Table([[title_p], [subtitle_p], [meta_p]], colWidths=[532])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor('#0f2942')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 1: EXECUTIVE ROADMAP & THE "WHY TCAD?" PARADIGM
    # =========================================================================
    story.append(Paragraph("1. Executive Overview & The TCAD Paradigm", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))
    
    p1 = (
        "<b>Why Technology Computer-Aided Design (TCAD)?</b> Fabricating semiconductor prototypes in cleanroom foundries is prohibitively expensive "
        "(photolithography reticle sets exceed millions of dollars per mask set) and requires months of turnaround time per wafer run. "
        "TCAD solves coupled nonlinear partial differential equations (Poisson's equation and carrier continuity equations) directly on a discretized "
        "finite-element or Delaunay mesh representing the exact atomic and geometric structure of the semiconductor. "
        "This enables predictive, sub-nanometer analysis of internal electrostatic potentials, carrier transport, quantum confinement, "
        "recombination dynamics, and breakdown mechanisms before committing to physical silicon fabrication."
    )
    story.append(Paragraph(p1, styles['body']))

    p2 = (
        "<b>The Three Project Pillars Covered in this Defense Manual:</b><br/>"
        "&bull; <b>Pillar I &mdash; Material-Engineered PN Junctions & Optoelectronics:</b> Investigated the physical consequences of bandgap engineering across "
        "four pivotal semiconductors: Silicon (Si), Germanium (Ge), Gallium Arsenide (GaAs), and 4H Silicon Carbide (4H-SiC). "
        "Extracted forward turn-on voltage, reverse saturation leakage, avalanche breakdown, optical generation in photodiodes, and radiative electroluminescence in GaAs LEDs.<br/>"
        "&bull; <b>Pillar II &mdash; 3D MOSFET Solid Modeling & Gate Emulation (Labsheet 8):</b> Implemented full 3D ACIS solid modeling for sub-micron MOSFETs, "
        "incorporating Shallow Trench Isolation (STI), poly re-oxidation buffers, rounded nitride spacers, and Gaussian source/drain doping.<br/>"
        "&bull; <b>Pillar III &mdash; Silicon-on-Insulator (SOI) MOSFET & Floating Body Physics (Labsheet 9):</b> Modeled ultra-thin body SOI MOSFETs, "
        "distinguishing Fully Depleted (FD-SOI) from Partially Depleted (PD-SOI) behavior, and validating body-tie contacts to suppress floating-body kink effects."
    )
    story.append(Paragraph(p2, styles['body']))

    story.append(make_callout(
        "TCAD replaces empirical trial-and-error with rigorous physics-based numerical modeling. "
        "The standard industry workflow comprises: (1) SDE for solid geometry and analytical doping, (2) SNMESH for Voronoi/Delaunay mesh generation, "
        "(3) SDevice for Drift-Diffusion numerical transport solving, and (4) SVisual for field and I-V post-processing.",
        "Core Philosophy:"
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 2: FUNDAMENTAL SEMICONDUCTOR PHYSICS FROM FIRST PRINCIPLES
    # =========================================================================
    story.append(Paragraph("2. Fundamental Semiconductor Physics from First Principles", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("2.1 Energy Bands & Carrier Statistics", styles['h2']))
    p_eb = (
        "<b>Bandgap Energy (E<sub>g</sub>):</b> The minimum energy required to excite an electron from the top of the valence band (E<sub>v</sub>) "
        "to the bottom of the conduction band (E<sub>c</sub>): <i>E<sub>g</sub> = E<sub>c</sub> &minus; E<sub>v</sub></i>. "
        "In a <b>direct bandgap</b> semiconductor (GaAs), the conduction band minimum and valence band maximum align at the same crystal momentum "
        "(k = 0, &Gamma;-point), allowing direct radiative photon emission without phonon assistance: <i>h&nu; &approx; E<sub>g</sub></i>. "
        "In an <b>indirect bandgap</b> semiconductor (Si, Ge, 4H-SiC), a change in crystal momentum (&Delta;k &ne; 0) is required, necessitating "
        "simultaneous emission or absorption of a lattice phonon, making radiative recombination inefficient.<br/>"
        "<b>Intrinsic Carrier Concentration (n<sub>i</sub>):</b> Governed by Fermi-Dirac statistics integrated over the density of states:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>n<sub>i</sub> = &radic;(N<sub>c</sub> N<sub>v</sub>) &middot; exp(&minus;E<sub>g</sub> / (2 k<sub>B</sub> T))</b><br/>"
        "where N<sub>c</sub>, N<sub>v</sub> are effective density of states, k<sub>B</sub> is Boltzmann's constant, and T = 300 K. "
        "Because n<sub>i</sub> depends exponentially on &minus;E<sub>g</sub>, wide-bandgap 4H-SiC has n<sub>i</sub> &approx; 10<sup>&minus;8</sup> cm<sup>&minus;3</sup>, "
        "while narrow-bandgap Ge has n<sub>i</sub> &approx; 2.4 &times; 10<sup>13</sup> cm<sup>&minus;3</sup>."
    )
    story.append(Paragraph(p_eb, styles['body']))

    story.append(Paragraph("2.2 Carrier Transport: Drift, Diffusion & Velocity Saturation", styles['h2']))
    p_trans = (
        "<b>Drift Current:</b> Carrier movement driven by an applied electric field <i>E</i>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>J<sub>drift</sub> = q (n &mu;<sub>n</sub> + p &mu;<sub>p</sub>) <i>E</i></b><br/>"
        "<b>Diffusion Current:</b> Carrier movement driven by spatial concentration gradients &nabla;n and &nabla;p:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>J<sub>diff</sub> = q D<sub>n</sub> (&nabla;n) &minus; q D<sub>p</sub> (&nabla;p)</b><br/>"
        "<b>Einstein Relation:</b> D<sub>n,p</sub> = &mu;<sub>n,p</sub> (k<sub>B</sub> T / q) = &mu;<sub>n,p</sub> V<sub>t</sub>, where V<sub>t</sub> &approx; 25.86 mV at 300 K.<br/>"
        "<b>Velocity Saturation:</b> At low fields, drift velocity v<sub>d</sub> = &mu;<i>E</i>. At high fields (<i>E</i> > 10<sup>4</sup> V/cm), optical phonon emission "
        "clamps carrier velocity to a maximum saturation speed <b>v<sub>sat</sub> &approx; 1 &times; 10<sup>7</sup> cm/s</b>. SDevice models this using the "
        "Canali/Caughey-Thomas formulation: <i>v(<i>E</i>) = &mu;<sub>0</sub><i>E</i> / [1 + (&mu;<sub>0</sub><i>E</i> / v<sub>sat</sub>)<sup>&beta;</sup>]<sup>1/&beta;</sup></i>."
    )
    story.append(Paragraph(p_trans, styles['body']))

    story.append(Paragraph("2.3 PN Junction Electrostatics & Built-in Potential", styles['h2']))
    p_pn = (
        "When P-type and N-type semiconductors are brought into metallurgical contact, majority holes diffuse into the N-side and majority electrons diffuse into the P-side, "
        "leaving behind uncompensated ionized donor (N<sub>D</sub><sup>+</sup>) and acceptor (N<sub>A</sub><sup>&minus;</sup>) space charge. "
        "This establishes the <b>depletion region</b> (space-charge layer) and an opposing internal electric field.<br/>"
        "<b>Built-in Potential (V<sub>bi</sub>):</b> The electrostatic potential difference across the junction at zero bias:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>V<sub>bi</sub> = V<sub>t</sub> &middot; ln( (N<sub>A</sub> N<sub>D</sub>) / n<sub>i</sub><sup>2</sup> )</b><br/>"
        "Since V<sub>bi</sub> &prop; ln(1 / n<sub>i</sub><sup>2</sup>) &prop; E<sub>g</sub> / (k<sub>B</sub> T), the built-in potential directly scales with the bandgap: "
        "V<sub>bi</sub>(Ge) &approx; 0.35 V, V<sub>bi</sub>(Si) &approx; 0.95 V, V<sub>bi</sub>(GaAs) &approx; 1.25 V, and V<sub>bi</sub>(4H-SiC) &approx; 2.95 V.<br/>"
        "<b>Depletion Width:</b> W<sub>dep</sub> = &radic;[ (2 &epsilon;<sub>s</sub> / q) &middot; (1/N<sub>A</sub> + 1/N<sub>D</sub>) &middot; (V<sub>bi</sub> &minus; V<sub>A</sub>) ]. "
        "Applying forward bias (V<sub>A</sub> > 0) lowers the barrier and narrows W<sub>dep</sub>; reverse bias (V<sub>A</sub> < 0) widens W<sub>dep</sub> and intensifies peak field."
    )
    story.append(Paragraph(p_pn, styles['body']))

    story.append(Paragraph("2.4 Recombination, Generation & Breakdown Physics", styles['h2']))
    p_rec = (
        "<b>Shockley-Read-Hall (SRH) Recombination:</b> Trap-assisted recombination via mid-gap defect energy levels E<sub>t</sub>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>R<sub>SRH</sub> = (p n &minus; n<sub>i</sub><sup>2</sup>) / [ &tau;<sub>p</sub> (n + n<sub>1</sub>) + &tau;<sub>n</sub> (p + p<sub>1</sub>) ]</b><br/>"
        "In reverse bias, pn &lt;&lt; n<sub>i</sub><sup>2</sup>, causing R<sub>SRH</sub> to become negative, representing <b>thermal generation</b>. "
        "The reverse generation current is J<sub>gen</sub> = q n<sub>i</sub> W<sub>dep</sub> / (2 &tau;<sub>0</sub>), explaining why materials with higher n<sub>i</sub> (Ge) exhibit massive leakage.<br/>"
        "<b>Radiative Recombination:</b> Direct band-to-band photon emission: <b>R<sub>rad</sub> = B<sub>rad</sub> (p n &minus; n<sub>i</sub><sup>2</sup>)</b>. Dominates in GaAs.<br/>"
        "<b>Avalanche Breakdown:</b> Under high reverse electric fields, carriers gain kinetic energy exceeding the ionization threshold E<sub>th</sub> &approx; 1.5 E<sub>g</sub>, "
        "colliding with valence electrons to create secondary electron-hole pairs (impact ionization). The avalanche condition is reached when the ionization integral equals unity: "
        "&int; &alpha; dx = 1. Critical field scales as <b><i>E</i><sub>crit</sub> &prop; E<sub>g</sub><sup>2</sup></b>, and breakdown voltage scales as <b>V<sub>br</sub> &prop; E<sub>g</sub><sup>1.5</sup></b>."
    )
    story.append(Paragraph(p_rec, styles['body']))
    story.append(Spacer(1, 8))

    # =========================================================================
    # SECTION 3: MATERIAL ENGINEERING BENCHMARK (SI, GE, GAAS, 4H-SIC)
    # =========================================================================
    story.append(Paragraph("3. Material Engineering Benchmark: Si vs Ge vs GaAs vs 4H-SiC", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "A rigorous comparison of semiconductor materials illuminates how atomic crystal structure and bandgap physics dictate terminal electrical behavior:",
        styles['body']
    ))

    # Benchmark Table
    bench_data = [
        [Paragraph("Property / Metric", styles['table_header']),
         Paragraph("Silicon (Si)", styles['table_header']),
         Paragraph("Germanium (Ge)", styles['table_header']),
         Paragraph("Gallium Arsenide (GaAs)", styles['table_header']),
         Paragraph("4H-SiC", styles['table_header'])],
        [Paragraph("Bandgap E<sub>g</sub> (300 K)", styles['table_cell']), Paragraph("1.12 eV (Indirect)", styles['table_cell']), Paragraph("0.66 eV (Indirect)", styles['table_cell']), Paragraph("1.42 eV (Direct)", styles['table_cell']), Paragraph("3.26 eV (Indirect)", styles['table_cell'])],
        [Paragraph("Intrinsic Density n<sub>i</sub> (cm<sup>&minus;3</sup>)", styles['table_cell']), Paragraph("1.08 &times; 10<sup>10</sup>", styles['table_cell']), Paragraph("2.40 &times; 10<sup>13</sup>", styles['table_cell']), Paragraph("2.10 &times; 10<sup>6</sup>", styles['table_cell']), Paragraph("8.20 &times; 10<sup>&minus;9</sup>", styles['table_cell'])],
        [Paragraph("Relative Permittivity &epsilon;<sub>r</sub>", styles['table_cell']), Paragraph("11.7", styles['table_cell']), Paragraph("16.0", styles['table_cell']), Paragraph("12.9", styles['table_cell']), Paragraph("9.7", styles['table_cell'])],
        [Paragraph("Electron Mobility &mu;<sub>n</sub> (cm<sup>2</sup>/V&middot;s)", styles['table_cell']), Paragraph("1400", styles['table_cell']), Paragraph("3900", styles['table_cell']), Paragraph("8500", styles['table_cell']), Paragraph("900", styles['table_cell'])],
        [Paragraph("Hole Mobility &mu;<sub>p</sub> (cm<sup>2</sup>/V&middot;s)", styles['table_cell']), Paragraph("450", styles['table_cell']), Paragraph("1900", styles['table_cell']), Paragraph("400", styles['table_cell']), Paragraph("120", styles['table_cell'])],
        [Paragraph("Critical Electric Field <i>E</i><sub>crit</sub> (MV/cm)", styles['table_cell']), Paragraph("0.30", styles['table_cell']), Paragraph("0.10", styles['table_cell']), Paragraph("0.40", styles['table_cell']), Paragraph("2.20", styles['table_cell'])],
        [Paragraph("Simulated Turn-on V<sub>on</sub> (V)", styles['table_cell']), Paragraph("0.68 V", styles['table_cell']), Paragraph("0.15 V", styles['table_cell']), Paragraph("1.05 V", styles['table_cell']), Paragraph("2.65 V", styles['table_cell'])],
        [Paragraph("Simulated Breakdown V<sub>br</sub> (V)", styles['table_cell']), Paragraph("&minus;32.5 V", styles['table_cell']), Paragraph("&minus;8.5 V", styles['table_cell']), Paragraph("&minus;48.0 V", styles['table_cell']), Paragraph("> &minus;1250 V", styles['table_cell'])],
        [Paragraph("Reverse Leakage I<sub>0</sub> @ &minus;1V (A/cm<sup>2</sup>)", styles['table_cell']), Paragraph("1.2 &times; 10<sup>&minus;11</sup>", styles['table_cell']), Paragraph("5.7 &times; 10<sup>&minus;7</sup>", styles['table_cell']), Paragraph("3.4 &times; 10<sup>&minus;14</sup>", styles['table_cell']), Paragraph("< 10<sup>&minus;20</sup>", styles['table_cell'])],
        [Paragraph("Primary Application Domain", styles['table_cell']), Paragraph("General VLSI & Microprocessors", styles['table_cell']), Paragraph("Cryogenic & Low-V<sub>on</sub> Rectifiers", styles['table_cell']), Paragraph("Optoelectronics, LEDs, RF Power", styles['table_cell']), Paragraph("EV Inverters, High-Voltage Power", styles['table_cell'])]
    ]

    t_bench = Table(bench_data, colWidths=[120, 103, 103, 103, 103])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f2942')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 8))

    # Embed Figure: Overlay & Breakdown
    iv_path = os.path.join(RESULTS_DIR, "iv_overlay.png")
    brk_path = os.path.join(RESULTS_DIR, "breakdown_analysis.png")
    if os.path.exists(iv_path) and os.path.exists(brk_path):
        img_table = Table([[
            Image(iv_path, width=260, height=155),
            Image(brk_path, width=260, height=155)
        ]], colWidths=[266, 266])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(img_table)
        cap_p = Paragraph(
            "<b>Figure 1:</b> TCAD simulation results across materials. (Left) Forward & reverse semi-logarithmic I-V overlay showing clear V<sub>on</sub> hierarchy (Ge < Si < GaAs < SiC). (Right) Avalanche breakdown extraction demonstrating 4H-SiC's ultra-high breakdown capability (> 1200 V) versus Ge (&minus;8.5 V) and Si (&minus;32.5 V).",
            ParagraphStyle('Cap', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor('#475569'), alignment=1)
        )
        story.append(cap_p)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 4: PILLAR I — MATERIAL-ENGINEERED DIODE & OPTOELECTRONICS
    # =========================================================================
    story.append(Paragraph("4. Device Architecture 1: Material-Engineered Diode & Optoelectronics", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    p_diod = (
        "<b>Geometric Configuration:</b> Modeled as a 2D P-I-N structure of dimensions <b>1.0 &mu;m (X) &times; 1.0 &mu;m (Y)</b>.<br/>"
        "&bull; <b>P<sup>+</sup> Anode Region:</b> Y &in; [0.0, 0.2] &mu;m, Boron doping N<sub>A</sub> = 1 &times; 10<sup>18</sup> cm<sup>&minus;3</sup>.<br/>"
        "&bull; <b>Intrinsic (I) Region:</b> Y &in; [0.2, 0.8] &mu;m, lightly-doped background Phosphorus N<sub>D</sub> = 1 &times; 10<sup>13</sup> cm<sup>&minus;3</sup>.<br/>"
        "&bull; <b>N<sup>+</sup> Cathode Region:</b> Y &in; [0.8, 1.0] &mu;m, Phosphorus doping N<sub>D</sub> = 1 &times; 10<sup>18</sup> cm<sup>&minus;3</sup>.<br/>"
        "&bull; <b>Electrodes:</b> Anode contact along top edge (Y = 0.0); Cathode contact along bottom edge (Y = 1.0).<br/>"
        "<b>Optoelectronic Modeling:</b><br/>"
        "&bull; <b>Photodiode Operation:</b> An optical beam of intensity P<sub>opt</sub> = 0.1 W/cm<sup>2</sup> at &lambda; = 850 nm penetrates the surface. "
        "Photons generate electron-hole pairs via Beer-Lambert absorption: G<sub>opt</sub>(y) = &Phi;<sub>0</sub> &alpha; e<sup>&minus;&alpha; y</sup>. "
        "The strong reverse electric field in the 0.6 &mu;m I-region rapidly sweeps electrons to the cathode and holes to the anode, creating an illuminated "
        "photocurrent 5 to 7 orders of magnitude higher than the dark leakage current.<br/>"
        "&bull; <b>LED Electroluminescence (GaAs):</b> Under strong forward bias (V<sub>A</sub> > 1.1 V), massive electron and hole injection into the direct-bandgap "
        "GaAs active region drives spontaneous radiative recombination: R<sub>rad</sub> = B<sub>rad</sub> (pn &minus; n<sub>i</sub><sup>2</sup>). "
        "With B<sub>rad</sub>(GaAs) &approx; 7.2 &times; 10<sup>&minus;10</sup> cm<sup>3</sup>/s, the device efficiently emits near-infrared photons at &lambda; = 873 nm."
    )
    story.append(Paragraph(p_diod, styles['body']))

    opto_path = os.path.join(RESULTS_DIR, "Optoelectronic_Photodiode_LED_Detailed.png")
    if os.path.exists(opto_path):
        story.append(Spacer(1, 4))
        story.append(Image(opto_path, width=420, height=180))
        cap_opto = Paragraph(
            "<b>Figure 2:</b> Optoelectronic TCAD simulation results. (Left) GaAs LED forward I-V and light emission onset. (Right) Photodiode dark versus illuminated reverse photocurrent comparison across Si, Ge, GaAs, and SiC.",
            ParagraphStyle('Cap2', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor('#475569'), alignment=1)
        )
        story.append(cap_opto)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 5: PILLAR II — 3D MOSFET SOLID MODELING & PHYSICS (LABSHEET 8)
    # =========================================================================
    story.append(Paragraph("5. Device Architecture 2: 3D MOSFET Solid Modeling & Physics (Labsheet 8)", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    p_mos = (
        "<b>Scaling Drivers & 3D Multi-Gate Physics:</b> In conventional planar MOSFETs scaled below 90 nm, the gate loses electrostatic control over the channel. "
        "The drain electric field penetrates deep into the substrate, inducing Short-Channel Effects (SCE): Drain-Induced Barrier Lowering (DIBL), "
        "threshold voltage roll-off, and severe subthreshold leakage. By extending the gate into 3 dimensions (FinFETs and Tri-gate structures), "
        "the gate surrounds the channel on multiple sides, terminating electric field lines from the drain and restoring steep subthreshold slope "
        "(SS &approx; 65&ndash;70 mV/dec).<br/>"
        "<b>Exact Geometric Architecture & Dimensions (Labsheet 8):</b><br/>"
        "&bull; <b>Silicon Substrate:</b> Cuboid X &in; [&minus;0.25, 0.25] &mu;m, Y &in; [&minus;0.20, 0.20] &mu;m, Z &in; [&minus;1.0, 0.0] &mu;m (Boron 10<sup>17</sup> cm<sup>&minus;3</sup>).<br/>"
        "&bull; <b>Shallow Trench Isolation (STI):</b> TrenchOxide_Right (Y &in; [&minus;0.20, &minus;0.10] &mu;m, Z &in; [&minus;0.2, 0.0] &mu;m) and "
        "TrenchOxide_Left (Y &in; [0.10, 0.20] &mu;m, Z &in; [&minus;0.2, 0.0] &mu;m) isolate the active channel width (W<sub>ch</sub> = 0.2 &mu;m).<br/>"
        "&bull; <b>Gate Oxide:</b> SiO<sub>2</sub> layer with physical thickness <b>T<sub>ox</sub> = 2 nm</b> (0.002 &mu;m), Z &in; [0.0, 0.002] &mu;m.<br/>"
        "&bull; <b>Polysilicon Gate:</b> L<sub>g</sub> = 200 nm (X &in; [&minus;0.10, 0.10] &mu;m), Y &in; [&minus;0.10, 0.20] &mu;m, height 100 nm (Z &in; [0.002, 0.1] &mu;m), Arsenic 10<sup>20</sup> cm<sup>&minus;3</sup>.<br/>"
        "&bull; <b>Poly Re-Oxidation Shells:</b> PolyReOxide1 (3 nm lateral oxide buffer) and PolyReOxide2 (5 nm cap) prevent dielectric breakdown at the poly gate corners.<br/>"
        "&bull; <b>Nitride Spacers:</b> Si<sub>3</sub>N<sub>4</sub> sidewall spacer (height 80 nm, Z &in; [0.0, 0.08] &mu;m) with an edge fillet radius of <b>30 nm</b>.<br/>"
        "&bull; <b>Source/Drain Contacts:</b> Metal blocks at X &in; [&minus;0.25, &minus;0.17] &mu;m (Source) and X &in; [0.17, 0.25] &mu;m (Drain), assigned contact sets and removed.<br/>"
        "&bull; <b>Doping Implants:</b> Analytical Gaussian Source/Drain profiles with peak N<sub>peak</sub> = 1 &times; 10<sup>19</sup> cm<sup>&minus;3</sup>, junction depth X<sub>j</sub> = 0.1 &mu;m, and lateral straggle factor 0.8.<br/>"
        "<b>Crucial Solid Modeling Lesson &mdash; The 'BAB' vs 'ABA' Boolean Priority:</b><br/>"
        "Under SDE's <code>\"ABA\"</code> mode, existing shapes retain priority and new overlapping shapes are clipped; creating an inner cuboid inside an existing cuboid "
        "causes the inner shape to be discarded (returning <code>#f</code>). By setting <b><code>\"BAB\"</code></b> and ordering trenches before the substrate, "
        "the substrate wraps around the trenches without devouring them, and the poly gate, re-oxidation shells, and nitride spacers seamlessly nest as proper shells."
    )
    story.append(Paragraph(p_mos, styles['body']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 6: PILLAR III — SILICON-ON-INSULATOR (SOI) MOSFET (LABSHEET 9)
    # =========================================================================
    story.append(Paragraph("6. Device Architecture 3: Silicon-on-Insulator (SOI) MOSFET (Labsheet 9)", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    p_soi = (
        "<b>SOI Technology Overview:</b> Silicon-on-Insulator places a thick insulating Buried Oxide (BOX) layer between the active silicon film and the substrate handle wafer. "
        "This drastically reduces junction capacitance (C<sub>j</sub>), completely eliminates latchup, enhances radiation hardness, and reduces subthreshold leakage.<br/>"
        "<b>Exact Geometric Architecture & Dimensions (Labsheet 9):</b><br/>"
        "&bull; <b>Substrate Handle Wafer:</b> H<sub>sub</sub> = 200 nm (Silicon, Boron 1 &times; 10<sup>16</sup> cm<sup>&minus;3</sup>).<br/>"
        "&bull; <b>Buried Oxide (BOX):</b> H<sub>box</sub> = 100 nm (SiO<sub>2</sub> dielectric).<br/>"
        "&bull; <b>Silicon Thin Film (Epi):</b> H<sub>epi</sub> = 50 nm (Silicon, Boron 1 &times; 10<sup>17</sup> cm<sup>&minus;3</sup>).<br/>"
        "&bull; <b>Gate Dielectric:</b> T<sub>ox</sub> = 4 nm (SiO<sub>2</sub>).<br/>"
        "&bull; <b>Polysilicon Gate:</b> L<sub>ch</sub> = 180 nm (X &in; [&minus;0.09, 0.09] &mu;m), H<sub>pol</sub> = 100 nm (Arsenic 1 &times; 10<sup>20</sup> cm<sup>&minus;3</sup>).<br/>"
        "&bull; <b>Body Tie:</b> Contact inserted at the bottom boundary of the 50 nm silicon film (X &in; [X<sub>bc1</sub>, X<sub>bc2</sub>]).<br/>"
        "<b>Fully Depleted (FD-SOI) vs Partially Depleted (PD-SOI):</b><br/>"
        "The maximum gate depletion width in silicon is given by: <i>W<sub>dep,max</sub> = &radic;[ (4 &epsilon;<sub>s</sub> k<sub>B</sub> T ln(N<sub>A</sub>/n<sub>i</sub>)) / (q<sup>2</sup> N<sub>A</sub>) ] &approx; 85 nm</i>. "
        "Because our silicon film thickness <b>H<sub>epi</sub> = 50 nm < W<sub>dep,max</sub></b>, the gate depletion region extends entirely across the film to the BOX interface. "
        "The device operates in the <b>Fully Depleted (FD-SOI)</b> regime under inversion, eliminating the floating neutral body.<br/>"
        "<b>The Floating-Body Effect & Kink Phenomenon:</b><br/>"
        "In thick-film or Partially Depleted SOI devices without a body contact, impact ionization at the high-field drain pinch-off region generates electron-hole pairs. "
        "Electrons flow into the drain, but holes are repelled toward the body. Because the insulating BOX prevents holes from escaping into the substrate, holes accumulate in the neutral body. "
        "This hole charge raises the body potential (&Delta;V<sub>B</sub> > 0), which lowers the threshold voltage through the body effect: "
        "<i>&Delta;V<sub>th</sub> = &minus;&gamma; (&radic;(2&phi;<sub>F</sub> &minus; V<sub>B</sub>) &minus; &radic;(2&phi;<sub>F</sub>))</i>. "
        "The reduced V<sub>th</sub> causes a sudden, parasitic surge in drain current, creating an abrupt <b>'kink'</b> in the I<sub>d</sub>&ndash;V<sub>d</sub> output characteristics.<br/>"
        "<b>Body-Tie Contact Mitigation:</b><br/>"
        "The low-resistance body-tie contact provides a dedicated ohmic discharge path for accumulated holes, pinning the body potential to ground (V<sub>B</sub> = 0 V) "
        "and completely suppressing the kink effect and threshold instability."
    )
    story.append(Paragraph(p_soi, styles['body']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 7: SENTAURUS TCAD TOOL SUITE MECHANICS & WORKFLOW
    # =========================================================================
    story.append(Paragraph("7. Synopsys Sentaurus TCAD Tool Suite Mechanics", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    p_tools = (
        "The Sentaurus TCAD design environment operates as a tightly integrated tool pipeline:<br/>"
        "&bull; <b>1. Sentaurus Structure Editor (SDE):</b> ACIS solid-modeling geometry engine scripted in Scheme Lisp. "
        "Defines cuboids, rectangles, cylindrical fillets, and analytical doping profiles (Constant, Gaussian, Error Function). "
        "Outputs the boundary representation (<code>.sat</code>) and boundary mesh file (<code>_bnd.tdr</code>).<br/>"
        "&bull; <b>2. Sentaurus Mesh (SNMESH):</b> Generates an adaptive Delaunay/Voronoi mesh. Decomposes space using axis-aligned binary trees, "
        "imprints geometry boundaries, and applies refinement boxes. Refines elements based on interface location (<code>MaxLenInt</code>) and doping gradients (<code>MaxTransDiff</code>). "
        "Outputs the spatial simulation grid (<code>_msh.tdr</code>).<br/>"
        "&bull; <b>3. Sentaurus Device (SDevice):</b> The finite-element numerical drift-diffusion and hydrodynamic device simulator. "
        "Discretizes Poisson's and carrier continuity equations across the mesh. Executes coupled nonlinear Newton-Raphson solvers with adaptive bias stepping. "
        "Outputs terminal characteristics (<code>.plt</code>) and 2D/3D spatial solution fields (<code>_des.tdr</code>).<br/>"
        "&bull; <b>4. Sentaurus Visual (SVisual):</b> High-performance Tcl-scriptable post-processor. Extracts I-V curves, subthreshold slopes, transconductance, "
        "and visualizes 2D/3D electric field, potential, carrier density, and energy band cutplanes.<br/>"
        "&bull; <b>5. Virtual Machine Automation Bridge:</b> TCAD binaries execute inside a Red Hat Enterprise Linux (RHEL 6.6) VirtualBox VM. "
        "The host interacts via <code>VBoxManage guestcontrol</code> over the PCI Host-Guest Communication Manager (HGCM) backplane, "
        "with real-time bidirectional file exchange via the mounted shared folder bridge (Host <code>/home/.../Documents/swb</code> &harr; Guest <code>/media/sf_swb</code>)."
    )
    story.append(Paragraph(p_tools, styles['body']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 8: PHYSICAL MODELS & NUMERICAL SOLVER MECHANICS IN SDEVICE
    # =========================================================================
    story.append(Paragraph("8. Physical Models & Numerical Solver Mechanics in SDevice", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    p_solv = (
        "<b>Governing Partial Differential Equations Solved by SDevice:</b><br/>"
        "1. <b>Poisson's Equation for Electrostatic Potential &psi;:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nabla; &middot; (&epsilon; &nabla;&psi;) = &minus;q (p &minus; n + N<sub>D</sub><sup>+</sup> &minus; N<sub>A</sub><sup>&minus;</sup>) &minus; &rho;<sub>trap</sub><br/>"
        "2. <b>Electron Continuity Equation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nabla; &middot; J<sub>n</sub> = q (R &minus; G) + q (&part;n / &part;t)<br/>"
        "3. <b>Hole Continuity Equation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&minus;&nabla; &middot; J<sub>p</sub> = q (R &minus; G) + q (&part;p / &part;t)<br/>"
        "<b>Key Physical Models Activated in our Deck:</b><br/>"
        "&bull; <b><code>eQCvanDort</code>:</b> Van Dort quantum-mechanical confinement model. Accounts for quantization of energy levels in thin inversion layers, "
        "which shifts peak electron density &sim; 1 nm away from the gate oxide interface, effectively increasing gate oxide thickness and shifting V<sub>th</sub>.<br/>"
        "&bull; <b><code>OldSlotboom</code>:</b> Heavy-doping bandgap narrowing model. Reduces effective bandgap in degenerately doped regions (S/D, PolyGate), "
        "increasing intrinsic carrier density n<sub>i,eff</sub> and correctly predicting junction capacitance.<br/>"
        "&bull; <b><code>PhuMob</code>:</b> Philips Unified Mobility Model. Accounts for temperature dependence, electron-impurity scattering, and electron-hole scattering.<br/>"
        "&bull; <b><code>Enormal</code>:</b> Lombardi surface mobility degradation model. Simulates acoustic phonon scattering and surface roughness scattering at dielectric interfaces.<br/>"
        "&bull; <b><code>HighFieldSaturation(GradQuasiFermi)</code>:</b> Driving-force velocity saturation driven by the gradient of the quasi-Fermi level, "
        "avoiding spurious unphysical velocity overshoots across abrupt doping gradients.<br/>"
        "&bull; <b><code>SRH(DopingDep)</code>:</b> Scharfetter doping-dependent Shockley-Read-Hall recombination lifetimes.<br/>"
        "<b>Numerical Solver Engine & Quasistationary Continuation:</b><br/>"
        "SDevice utilizes the <b>Bank/Rose nonlinear damped Newton solver</b>. Contact voltages cannot be stepped abruptly without causing divergence. "
        "The <code>Quasistationary</code> algorithm introduces a continuation parameter t &in; [0, 1]. Starting with an initial step (<code>InitialStep = 0.05</code>), "
        "the solver monitors the residual norm. If Newton iterations converge in &le; 2 steps, the step size increases by <code>Increment = 1.5</code>. "
        "If divergence occurs, the solver automatically cuts the step size down to <code>MinStep = 10<sup>&minus;5</sup></code>, guaranteeing robust convergence."
    )
    story.append(Paragraph(p_solv, styles['body']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 9: EXACT SETTINGS, LENGTHS, DIMENSIONS & CONCENTRATIONS
    # =========================================================================
    story.append(Paragraph("9. Experimental Dimensions, Doping Profiles & TCAD Settings", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    dim_data = [
        [Paragraph("Parameter / Setting", styles['table_header']),
         Paragraph("Pillar I: PN Diode", styles['table_header']),
         Paragraph("Pillar II: 3D MOSFET", styles['table_header']),
         Paragraph("Pillar III: SOI MOSFET", styles['table_header'])],
        [Paragraph("Spatial Dimension", styles['table_cell']), Paragraph("2D (X: 1.0 &mu;m, Y: 1.0 &mu;m)", styles['table_cell']), Paragraph("3D (0.5 &times; 0.4 &times; 1.0 &mu;m)", styles['table_cell']), Paragraph("2D (X: 0.6 &mu;m, Y: 0.45 &mu;m)", styles['table_cell'])],
        [Paragraph("Substrate / Body Doping", styles['table_cell']), Paragraph("N<sub>A</sub> = 1 &times; 10<sup>18</sup> cm<sup>&minus;3</sup> (P<sup>+</sup>)", styles['table_cell']), Paragraph("Boron 1 &times; 10<sup>17</sup> cm<sup>&minus;3</sup> (P-well)", styles['table_cell']), Paragraph("Boron 1 &times; 10<sup>17</sup> cm<sup>&minus;3</sup> (P-epi)", styles['table_cell'])],
        [Paragraph("Channel / Active Doping", styles['table_cell']), Paragraph("N<sub>D</sub> = 1 &times; 10<sup>13</sup> cm<sup>&minus;3</sup> (I-region)", styles['table_cell']), Paragraph("Boron 1 &times; 10<sup>17</sup> cm<sup>&minus;3</sup>", styles['table_cell']), Paragraph("EpiDop = 1 &times; 10<sup>17</sup> cm<sup>&minus;3</sup>", styles['table_cell'])],
        [Paragraph("Source / Drain Doping", styles['table_cell']), Paragraph("N<sub>D</sub> = 1 &times; 10<sup>18</sup> cm<sup>&minus;3</sup> (N<sup>+</sup>)", styles['table_cell']), Paragraph("Arsenic Peak 10<sup>19</sup> cm<sup>&minus;3</sup> (Gauss)", styles['table_cell']), Paragraph("Phosphorus 10<sup>20</sup> cm<sup>&minus;3</sup> (Gauss)", styles['table_cell'])],
        [Paragraph("Gate Length (L<sub>g</sub> / L<sub>ch</sub>)", styles['table_cell']), Paragraph("N/A", styles['table_cell']), Paragraph("200 nm (0.2 &mu;m)", styles['table_cell']), Paragraph("180 nm (0.18 &mu;m)", styles['table_cell'])],
        [Paragraph("Gate Oxide Thickness (T<sub>ox</sub>)", styles['table_cell']), Paragraph("N/A", styles['table_cell']), Paragraph("2.0 nm (0.002 &mu;m SiO<sub>2</sub>)", styles['table_cell']), Paragraph("4.0 nm (0.004 &mu;m SiO<sub>2</sub>)", styles['table_cell'])],
        [Paragraph("Buried Oxide / Isolation", styles['table_cell']), Paragraph("N/A", styles['table_cell']), Paragraph("200 nm STI Trench Oxide", styles['table_cell']), Paragraph("100 nm Buried Oxide (BOX)", styles['table_cell'])],
        [Paragraph("Film Thickness (H<sub>epi</sub>)", styles['table_cell']), Paragraph("1.0 &mu;m total thickness", styles['table_cell']), Paragraph("1.0 &mu;m substrate depth", styles['table_cell']), Paragraph("50 nm thin silicon film", styles['table_cell'])],
        [Paragraph("Contact Terminals", styles['table_cell']), Paragraph("anode, cathode", styles['table_cell']), Paragraph("source, drain, gate, substrate", styles['table_cell']), Paragraph("source, drain, gate, substrate, bodytie", styles['table_cell'])],
        [Paragraph("Mesh Discretization", styles['table_cell']), Paragraph("688 nodes, 1,320 triangles", styles['table_cell']), Paragraph("15,448 nodes, 84,647 tetrahedra", styles['table_cell']), Paragraph("4,591 nodes, 8,953 triangles", styles['table_cell'])],
        [Paragraph("Voltage Bias Range", styles['table_cell']), Paragraph("V<sub>A</sub>: &minus;1500 V to +1.0 V", styles['table_cell']), Paragraph("SDE Solid Model & Grid Verification", styles['table_cell']), Paragraph("V<sub>ds</sub> = 0.05 V; V<sub>gs</sub> = &minus;0.1 to 1.5 V", styles['table_cell'])]
    ]

    t_dim = Table(dim_data, colWidths=[112, 140, 140, 140])
    t_dim.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f2942')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_dim)
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 10: HIGH-YIELD VIVA VOCE QUESTION BANK (30+ RIGOROUS Q&A)
    # =========================================================================
    story.append(Paragraph("10. High-Yield Viva Voce Question Bank (30+ Master Questions & Answers)", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    viva_qa = [
        ("Q1: Why does 4H-SiC exhibit a breakdown voltage exceeding 1200 V while Germanium breaks down at only &minus;8.5 V?",
         "<b>Answer:</b> Avalanche breakdown occurs when the maximum electric field exceeds the critical breakdown field <i>E</i><sub>crit</sub>. "
         "The critical field scales quadratically with the bandgap: <i>E</i><sub>crit</sub> &prop; E<sub>g</sub><sup>2</sup>. "
         "4H-SiC has an ultra-wide bandgap of 3.26 eV, yielding <i>E</i><sub>crit</sub> &approx; 2.2 MV/cm. "
         "Conversely, Germanium has a narrow bandgap of 0.66 eV, yielding <i>E</i><sub>crit</sub> &approx; 0.1 MV/cm. "
         "Since breakdown voltage scales as V<sub>br</sub> &approx; <i>E</i><sub>crit</sub> W<sub>dep</sub> / 2 &prop; E<sub>g</sub><sup>1.5</sup>, "
         "4H-SiC can sustain over 140&times; higher reverse voltage before impact ionization triggers carrier multiplication."),

        ("Q2: Why is the reverse leakage current of Germanium (5.7 &times; 10<sup>&minus;7</sup> A/cm<sup>2</sup>) seven orders of magnitude higher than Silicon?",
         "<b>Answer:</b> The reverse saturation leakage is governed by thermal minority carrier generation within the depletion region: "
         "J<sub>gen</sub> = q n<sub>i</sub> W<sub>dep</sub> / (2 &tau;<sub>0</sub>), and diffusion from neutral regions: J<sub>diff</sub> &prop; n<sub>i</sub><sup>2</sup>. "
         "The intrinsic carrier concentration depends exponentially on bandgap: n<sub>i</sub> = &radic;(N<sub>c</sub> N<sub>v</sub>) exp(&minus;E<sub>g</sub> / 2k<sub>B</sub>T). "
         "Because E<sub>g</sub>(Ge) = 0.66 eV is significantly smaller than E<sub>g</sub>(Si) = 1.12 eV, n<sub>i</sub>(Ge) &approx; 2.4 &times; 10<sup>13</sup> cm<sup>&minus;3</sup>, "
         "which is over 2,200 times higher than n<sub>i</sub>(Si) &approx; 1.08 &times; 10<sup>10</sup> cm<sup>&minus;3</sup>. "
         "This colossal thermal generation produces massive reverse leakage in Germanium."),

        ("Q3: Why can Gallium Arsenide (GaAs) function as an efficient LED while Silicon cannot?",
         "<b>Answer:</b> GaAs is a <b>direct bandgap</b> semiconductor with its conduction band minimum and valence band maximum aligned at crystal momentum k = 0 (&Gamma;-point). "
         "Electrons can drop directly into empty valence states emitting a photon of energy h&nu; &approx; E<sub>g</sub> with high quantum efficiency: R<sub>rad</sub> = B (pn &minus; n<sub>i</sub><sup>2</sup>), "
         "where B &approx; 7.2 &times; 10<sup>&minus;10</sup> cm<sup>3</sup>/s. "
         "Silicon is an <b>indirect bandgap</b> semiconductor (E<sub>c</sub> minimum along &Delta;-axis; E<sub>v</sub> maximum at &Gamma;). "
         "Radiative recombination requires momentum conservation via simultaneous lattice phonon emission/absorption, making radiative transitions extremely improbable (B &approx; 10<sup>&minus;15</sup> cm<sup>3</sup>/s). "
         "Instead, non-radiative SRH and Auger recombination dominate in Silicon, dissipating energy as heat."),

        ("Q4: What is the physical wavelength emitted by our simulated GaAs LED?",
         "<b>Answer:</b> Photon wavelength is given by the Planck-Einstein relation: &lambda; = h c / E<sub>g</sub>. "
         "For GaAs with E<sub>g</sub> = 1.424 eV at 300 K: &lambda; = (1.2398 &mu;m&middot;eV) / 1.424 eV &approx; 0.871 &mu;m = <b>871 nm</b>, "
         "which lies precisely in the Near-Infrared (NIR) spectrum."),

        ("Q5: What was the root cause of the error in the original Labsheet 8 3D MOSFET code?",
         "<b>Answer:</b> Three fatal bugs prevented execution: (1) <code>(sde:set-process-up-direction \"+z\")</code> passed a string instead of an expected integer, "
         "crashing SDE's Scheme interpreter immediately; (2) The Gate Oxide cuboid had identical Z-coordinates [0.002, 0.002], producing zero thickness (a degenerate plane) "
         "which ACIS rejected; and (3) <code>sdegeo:fillet</code> was called with vertex entity IDs from <code>find-vertex-id</code> instead of edge IDs from <code>find-edge-id</code>, "
         "and used an unbound Scheme parameter variable."),

        ("Q6: In SDE, what is the difference between Boolean modes 'ABA', 'BAB', and 'XX'?",
         "<b>Answer:</b> In CSG solid modeling: 'A' denotes existing geometry; 'B' denotes new geometry. "
         "&bull; <b><code>\"ABA\"</code>:</b> Existing shape A retains priority. New shape B is subtracted by A (B &minus; A). If B is completely enclosed inside A, B is completely deleted (returns <code>#f</code>).<br/>"
         "&bull; <b><code>\"BAB\"</code>:</b> Existing shape A is subtracted by new shape B (A &minus; B). However, existing inner shapes are preserved when outer shells wrap around them, enabling sequential layer building.<br/>"
         "&bull; <b><code>\"XX\"</code>:</b> Shapes intersect and co-exist without mutual truncation."),

        ("Q7: What is the purpose of the 30 nm fillet on the nitride spacer in 3D MOSFETs?",
         "<b>Answer:</b> In physical fabrication, chemical vapor deposition (CVD) of Si<sub>3</sub>N<sub>4</sub> spacers followed by anisotropic reactive ion etching (RIE) "
         "leaves rounded outer shoulders due to isotropic deposition profiles. A sharp 90&deg; corner would create artificial singularities in the electric field, "
         "causing non-physical localized avalanche breakdown and divergent Delaunay meshing. The 30 nm fillet realistically smooths the corner and ensures mesh convergence."),

        ("Q8: Why does our 3D MOSFET model delete the metal cuboid after setting the Source/Drain contacts?",
         "<b>Answer:</b> In SDE, <code>(sdegeo:set-contact SOURCE \"source\" \"remove\")</code> imprints the contact boundary face on the underlying silicon, "
         "and then deletes the redundant metal body. This avoids having to mesh a passive metal volume in SDevice, saving thousands of mesh nodes while perfectly preserving "
         "the ohmic boundary condition: &psi; = V<sub>applied</sub> + V<sub>bi</sub>."),

        ("Q9: What is the difference between Fully Depleted (FD-SOI) and Partially Depleted (PD-SOI)?",
         "<b>Answer:</b> It depends on the ratio of the silicon film thickness H<sub>epi</sub> to the maximum depletion width W<sub>dep,max</sub>. "
         "If H<sub>epi</sub> > W<sub>dep,max</sub>, a neutral, un-depleted silicon region exists beneath the gate depletion layer, floating electrically above the BOX (Partially Depleted). "
         "If H<sub>epi</sub> < W<sub>dep,max</sub>, the gate depletion region punches completely through the film to the BOX interface (Fully Depleted). "
         "In our design, H<sub>epi</sub> = 50 nm < W<sub>dep,max</sub> &approx; 85 nm, so it operates in the <b>Fully Depleted</b> regime."),

        ("Q10: What is the Floating Body Effect and the 'Kink Effect' in SOI MOSFETs?",
         "<b>Answer:</b> In PD-SOI devices with a floating body, impact ionization at the high-field drain pinch-off region produces electron-hole pairs. "
         "Electrons exit through the drain, but holes are swept into the neutral body. Because the insulating BOX prevents holes from escaping into the substrate, "
         "holes accumulate in the body, raising the body potential (&Delta;V<sub>B</sub> > 0). This forward-biases the body-source junction and lowers the threshold voltage V<sub>th</sub> "
         "through the body effect. The reduced V<sub>th</sub> causes an abrupt, unwanted surge in drain current, creating a 'kink' in the I<sub>d</sub>&ndash;V<sub>d</sub> curve."),

        ("Q11: How does a Body-Tie contact eliminate the Kink Effect?",
         "<b>Answer:</b> The body-tie contact provides a direct low-resistance ohmic connection to the channel body, allowing accumulated holes to discharge to ground. "
         "This holds the body potential fixed at V<sub>B</sub> = 0 V, completely eliminating the kink effect, threshold instability, and history-dependent propagation delay jitter."),

        ("Q12: What is the physical role of the 'eQCvanDort' model in SDevice?",
         "<b>Answer:</b> In ultra-thin gate dielectrics (T<sub>ox</sub> = 2&ndash;4 nm), the steep potential well at the semiconductor-oxide interface quantizes electron energy into 2D subbands. "
         "The quantum mechanical wave function &psi;(z) must vanish at the interface, forcing the peak carrier concentration to reside &sim; 1 nm away from the physical interface. "
         "Classical drift-diffusion overestimates interface carrier density. <code>eQCvanDort</code> introduces a quantum correction potential &Delta;&psi;<sub>QC</sub> "
         "that accurately predicts the shift in inversion layer centroid, the effective oxide thickness increase, and the threshold voltage increase."),

        ("Q13: Why is the 'OldSlotboom' bandgap narrowing model essential in heavily doped source/drain regions?",
         "<b>Answer:</b> At doping concentrations exceeding 10<sup>17</sup> cm<sup>&minus;3</sup>, impurity wavefunctions overlap and form an impurity band that merges with the conduction band edge, "
         "effectively narrowing the bandgap: &Delta;E<sub>g</sub> &approx; 10&ndash;30 meV. Slotboom's model calculates this reduction, which increases the effective intrinsic carrier density "
         "n<sub>i,eff</sub><sup>2</sup> = n<sub>i</sub><sup>2</sup> exp(&Delta;E<sub>g</sub> / k<sub>B</sub>T), ensuring accurate minority carrier injection and junction capacitance calculation."),

        ("Q14: What is the purpose of 'GradQuasiFermi' in high-field velocity saturation?",
         "<b>Answer:</b> Conventional velocity saturation models use the local electric field <i>E</i> = &minus;&nabla;&psi;. Across abrupt metallurgical junctions, "
         "the built-in electric field is very high even at equilibrium, which would spuriously reduce carrier mobility to zero. "
         "<code>GradQuasiFermi</code> uses the gradient of the quasi-Fermi level &nabla;&Phi;<sub>n,p</sub> as the driving force, which is zero at equilibrium and correctly reflects only non-equilibrium drift acceleration."),

        ("Q15: How does the Newton-Raphson Bank/Rose solver work in SDevice?",
         "<b>Answer:</b> SDevice linearizes the coupled system of nonlinear equations F(x) = 0 using a multi-dimensional Taylor expansion: "
         "J &middot; &delta;x = &minus;F(x), where J is the Jacobian matrix (&part;F<sub>i</sub> / &part;x<sub>j</sub>). "
         "The Bank/Rose algorithm applies a damping factor &lambda; &in; (0, 1] to update x<sub>k+1</sub> = x<sub>k</sub> + &lambda; &delta;x, "
         "guaranteeing that the residual norm ||F(x<sub>k+1</sub>)|| decreases monotonically, preventing solver divergence during steep exponential switching."),

        ("Q16: Why did SVisual throw an 'invalid command name system' error in batch mode?",
         "<b>Answer:</b> SVisual's Tcl interpreter runs in a secure, sandboxed environment where direct shell execution commands (like <code>system</code> or <code>exec</code>) "
         "are disabled or syntactically distinct from standard Linux bash. Removing extraneous system shell calls and adhering to pure SVisual Tcl APIs resolved the issue."),

        ("Q17: What are the three primary short-channel effects (SCE) in scaled MOSFETs?",
         "<b>Answer:</b> (1) <b>Drain-Induced Barrier Lowering (DIBL):</b> The drain electric field lowers the source-channel injection barrier at high V<sub>ds</sub>, reducing V<sub>th</sub>.<br/>"
         "(2) <b>Threshold Voltage Roll-Off:</b> Depletion charge sharing with source/drain reduces the gate-controlled charge, lowering V<sub>th</sub> as L<sub>g</sub> shrinks.<br/>"
         "(3) <b>Subthreshold Swing Degradation:</b> SS increases from the ideal 60 mV/dec toward > 100 mV/dec, drastically increasing off-state leakage current I<sub>off</sub>."),

        ("Q18: How do we extract the Subthreshold Swing (SS) from an Id-Vg curve?",
         "<b>Answer:</b> SS is defined as the gate voltage change required to increase drain current by one decade in the subthreshold regime:<br/>"
         "&nbsp;&nbsp;&nbsp;&nbsp;<b>SS = [ d(log<sub>10</sub> I<sub>d</sub>) / dV<sub>gs</sub> ]<sup>&minus;1</sup> = (ln 10) &middot; (k<sub>B</sub> T / q) &middot; (1 + C<sub>dep</sub> / C<sub>ox</sub>)</b>.<br/>"
         "At room temperature (300 K), the ideal minimum is (2.303)(25.86 mV)(1) &approx; <b>59.6 mV/decade</b>."),

        ("Q19: What is DIBL, and how is it quantified from TCAD simulations?",
         "<b>Answer:</b> DIBL is the horizontal shift in threshold voltage divided by the change in drain voltage:<br/>"
         "&nbsp;&nbsp;&nbsp;&nbsp;<b>DIBL = &Delta;V<sub>th</sub> / &Delta;V<sub>ds</sub> = (V<sub>th</sub><sup>linear</sup> &minus; V<sub>th</sub><sup>sat</sup>) / (V<sub>ds</sub><sup>high</sup> &minus; V<sub>ds</sub><sup>low</sup>) [mV/V]</b>.<br/>"
         "Extracted by comparing V<sub>th</sub> from Id-Vg curves at V<sub>ds</sub> = 0.05 V versus V<sub>ds</sub> = 1.0 V."),

        ("Q20: Why do we use a Gaussian profile for Source/Drain doping instead of a constant box profile?",
         "<b>Answer:</b> Physical ion implantation followed by thermal annealing produces a Gaussian or Pearson-IV spatial distribution with lateral straggle beneath the gate edge. "
         "An abrupt box profile creates discontinuous derivative boundaries, leading to singular electric field spikes and severe numerical divergence in the Newton solver."),

        ("Q21: What is the significance of the 40 &Omega; external resistor on Source and Drain electrodes in SDevice?",
         "<b>Answer:</b> The <code>Resistor = 40</code> specification models parasitic metal contact resistance and external probing lead resistance. "
         "Without contact resistance, an ideal voltage boundary condition at high current causes non-physical current densities and numerical instability."),

        ("Q22: Why does SDevice require an initial equilibrium solution (Coupled { Poisson }) before voltage sweeps?",
         "<b>Answer:</b> At zero bias, carrier concentrations and electrostatic potential must satisfy thermal equilibrium (zero net current). "
         "Solving Poisson's equation alone with Fermi-Dirac statistics establishes the self-consistent built-in potential V<sub>bi</sub>. "
         "Attempting to ramp voltages without an equilibrium initial state produces a massive initial residual norm, causing immediate solver divergence."),

        ("Q23: What does 'MaxLenInt' specify in the SNMESH command file?",
         "<b>Answer:</b> <code>MaxLenInt</code> sets the maximum allowed mesh edge length across the interface between two materials (e.g., Silicon and Gate Oxide). "
         "Because inversion layers and surface electric fields vary drastically within a few nanometers of the interface, <code>MaxLenInt = 0.0003</code> (&sim; 0.3 nm) "
         "forces extremely dense meshing where electrostatic gradients are steepest."),

        ("Q24: What does 'MaxTransDiff' specify in mesh generation?",
         "<b>Answer:</b> <code>MaxTransDiff = 1.0</code> enforces mesh refinement wherever the spatial gradient of doping concentration changes by more than one decade per mesh element. "
         "This guarantees smooth discretization across metallurgical pn junctions and S/D halo extension boundaries."),

        ("Q25: Why is 4H-SiC specifically denoted as '4H'?",
         "<b>Answer:</b> Silicon Carbide exhibits polytypism (identical stoichiometry but different hexagonal/cubic layer stacking sequences along the c-axis). "
         "4H-SiC has a 4-bilayer stacking repeat sequence (ABCB...) with hexagonal symmetry, offering an optimal combination of high electron mobility (900 cm<sup>2</sup>/V&middot;s), "
         "wide bandgap (3.26 eV), and high thermal conductivity (4.9 W/cm&middot;K), making it the premier industry polytype for power MOSFETs."),

        ("Q26: What is the difference between Zener breakdown and Avalanche breakdown?",
         "<b>Answer:</b> <b>Zener breakdown</b> occurs in heavily doped junctions (N > 10<sup>18</sup> cm<sup>&minus;3</sup>) with ultra-narrow depletion widths (W < 10 nm), "
         "where electrons quantum-tunnel directly from the valence band to the conduction band at low reverse voltages (< 5 V). It has a <i>negative</i> temperature coefficient. "
         "<b>Avalanche breakdown</b> occurs in moderately doped junctions at higher voltages (> 7 V), driven by impact ionization. "
         "It has a <i>positive</i> temperature coefficient because increased lattice scattering at higher temperatures reduces the mean free path."),

        ("Q27: In our photodiode simulation, why did reverse current increase under illumination while forward current remained nearly unchanged?",
         "<b>Answer:</b> The total diode current is I = I<sub>0</sub> [exp(qV / k<sub>B</sub>T) &minus; 1] &minus; I<sub>photo</sub>. "
         "Under reverse bias, dark current is minute (I &approx; &minus;I<sub>0</sub> &sim; 10<sup>&minus;11</sup> A). The optically generated photocurrent "
         "I<sub>photo</sub> &approx; 10<sup>&minus;5</sup> A dominates by several orders of magnitude. "
         "Under forward bias, exponential majority carrier injection current exp(qV / k<sub>B</sub>T) rapidly reaches milliamperes, completely swamping the microampere photocurrent."),

        ("Q28: What is the Subthreshold Slope degradation mechanism in planar devices?",
         "<b>Answer:</b> In subthreshold, the gate acts as a capacitive voltage divider: &part;&psi;<sub>s</sub> / &part;V<sub>gs</sub> = C<sub>ox</sub> / (C<sub>ox</sub> + C<sub>dep</sub> + C<sub>it</sub>). "
         "As channel length shrinks, drain capacitive coupling C<sub>d</sub> adds to the denominator: &part;&psi;<sub>s</sub> / &part;V<sub>gs</sub> = C<sub>ox</sub> / (C<sub>ox</sub> + C<sub>dep</sub> + C<sub>d</sub>). "
         "This lowers the gate coupling efficiency below unity, increasing SS far above 60 mV/dec."),

        ("Q29: What is the advantage of using a buried oxide (BOX) thickness of 100 nm versus 20 nm?",
         "<b>Answer:</b> A thicker BOX (100 nm) minimizes substrate parasitic capacitance C<sub>sub</sub> = &epsilon;<sub>ox</sub> / H<sub>box</sub>, "
         "reducing dynamic switching energy (1/2 C V<sup>2</sup>) and boosting cut-off frequency f<sub>T</sub>. "
         "However, an ultra-thin BOX (20 nm, used in modern UTBB FD-SOI) allows back-gate biasing through the substrate to dynamically tune V<sub>th</sub> for adaptive power management."),

        ("Q30: Why is Sentaurus Structure Editor (SDE) preferred over analytical drafting tools?",
         "<b>Answer:</b> SDE generates parametrically defined, watertight ACIS solid geometries that automatically preserve topology under coordinate parameter sweeps. "
         "It directly exports spatial doping distributions and boundary markers compatible with SNMESH and SDevice, eliminating geometry translation errors."),

        ("Q31: What is the physical significance of the 'ErRef' parameter in SDevice Math section?",
         "<b>Answer:</b> <code>ErRef(electron) = 1e10</code> sets the minimum absolute carrier density threshold below which relative error checks are relaxed. "
         "In deep depletion regions where electron density drops below 10<sup>5</sup> cm<sup>&minus;3</sup>, calculating relative errors would amplify numerical round-off noise. "
         "ErRef prevents the solver from wasting iterations chasing floating-point noise in depleted domains.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(q, styles['question']))
        story.append(Paragraph(a, styles['answer']))
    story.append(Spacer(1, 10))

    # =========================================================================
    # SECTION 11: FORMULA QUICK-REFERENCE CARD & SUMMARY CHEAT-SHEET
    # =========================================================================
    story.append(Paragraph("11. Formula Quick-Reference Card & Cheat Sheet", styles['h1']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0f2942'), spaceBefore=2, spaceAfter=6))

    f_data = [
        [Paragraph("Physical Quantity", styles['table_header']),
         Paragraph("Formula / Mathematical Expression", styles['table_header']),
         Paragraph("Physical Interpretation / Significance", styles['table_header'])],
        [Paragraph("Intrinsic Carrier Density", styles['table_cell']),
         Paragraph("n<sub>i</sub> = &radic;(N<sub>c</sub> N<sub>v</sub>) e<sup>&minus;E<sub>g</sub> / 2k<sub>B</sub>T</sup>", styles['table_cell']),
         Paragraph("Determines reverse leakage; scales exponentially with bandgap.", styles['table_cell'])],
        [Paragraph("Built-in Potential", styles['table_cell']),
         Paragraph("V<sub>bi</sub> = V<sub>t</sub> ln( N<sub>A</sub> N<sub>D</sub> / n<sub>i</sub><sup>2</sup> )", styles['table_cell']),
         Paragraph("Equilibrium electrostatic barrier height across the pn junction.", styles['table_cell'])],
        [Paragraph("Depletion Width", styles['table_cell']),
         Paragraph("W = &radic;[ (2&epsilon;<sub>s</sub>/q)(1/N<sub>A</sub> + 1/N<sub>D</sub>)(V<sub>bi</sub> &minus; V) ]", styles['table_cell']),
         Paragraph("Width of space-charge region; widens under reverse bias.", styles['table_cell'])],
        [Paragraph("Maximum Electric Field", styles['table_cell']),
         Paragraph("<i>E</i><sub>max</sub> = 2(V<sub>bi</sub> &minus; V) / W", styles['table_cell']),
         Paragraph("Peak field at metallurgical junction; triggers avalanche breakdown.", styles['table_cell'])],
        [Paragraph("Avalanche Breakdown", styles['table_cell']),
         Paragraph("V<sub>br</sub> &approx; 60 (E<sub>g</sub>/1.1)<sup>1.5</sup> (N<sub>B</sub>/10<sup>16</sup>)<sup>&minus;0.75</sup>", styles['table_cell']),
         Paragraph("Critical breakdown voltage; scales superlinearly with bandgap.", styles['table_cell'])],
        [Paragraph("Subthreshold Swing", styles['table_cell']),
         Paragraph("SS = ln(10) &middot; (k<sub>B</sub>T/q) &middot; (1 + C<sub>dep</sub>/C<sub>ox</sub>)", styles['table_cell']),
         Paragraph("Gate voltage required for 1-decade current increase; ideal = 59.6 mV/dec.", styles['table_cell'])],
        [Paragraph("Drain-Induced Barrier Lowering", styles['table_cell']),
         Paragraph("DIBL = (V<sub>th</sub><sup>lin</sup> &minus; V<sub>th</sub><sup>sat</sup>) / &Delta;V<sub>ds</sub>", styles['table_cell']),
         Paragraph("Measures drain electrostatic interference over channel barrier.", styles['table_cell'])],
        [Paragraph("Threshold Voltage (with Body Effect)", styles['table_cell']),
         Paragraph("V<sub>th</sub> = V<sub>th0</sub> + &gamma; [ &radic;(2&phi;<sub>F</sub> &minus; V<sub>BS</sub>) &minus; &radic;(2&phi;<sub>F</sub>) ]", styles['table_cell']),
         Paragraph("Body-bias dependence; drives floating body kink effect in SOI.", styles['table_cell'])],
        [Paragraph("Photon Emission Wavelength", styles['table_cell']),
         Paragraph("&lambda; = h c / E<sub>g</sub> = 1.2398 &mu;m&middot;eV / E<sub>g</sub>", styles['table_cell']),
         Paragraph("Direct optical emission wavelength (GaAs &rarr; 873 nm NIR).", styles['table_cell'])],
        [Paragraph("Velocity Saturation", styles['table_cell']),
         Paragraph("v(<i>E</i>) = &mu;<i>E</i> / [1 + (&mu;<i>E</i>/v<sub>sat</sub>)<sup>&beta;</sup>]<sup>1/&beta;</sup>", styles['table_cell']),
         Paragraph("Limits carrier velocity to v<sub>sat</sub> &approx; 10<sup>7</sup> cm/s at high fields.", styles['table_cell'])]
    ]

    t_f = Table(f_data, colWidths=[120, 202, 210])
    t_f.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f2942')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#94a3b8')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_f)
    story.append(Spacer(1, 14))

    final_box = make_callout(
        "<b>Final Preparation Checklist Before Entering the Examination / Viva Room:</b><br/>"
        "1. <b>Be ready to explain the Material Benchmark:</b> SiC has the highest breakdown (>1200V) and lowest leakage due to wide E<sub>g</sub> = 3.26 eV; Ge has lowest turn-on (0.15V) but massive leakage due to small E<sub>g</sub> = 0.66 eV.<br/>"
        "2. <b>Be ready to sketch the 3D MOSFET & explain Boolean priority:</b> Under <code>\"BAB\"</code>, existing inner shapes (Gate, Oxide, Trenches) are preserved when enclosing bodies (Substrate, Spacers) wrap around them.<br/>"
        "3. <b>Be ready to explain SOI MOSFET Floating Body & Kink Effect:</b> Impact-ionization holes accumulate in the body over the insulating BOX, lowering V<sub>th</sub> and causing the drain current kink; the body-tie contact provides a discharge path to ground.<br/>"
        "4. <b>Be ready to state numerical solver mechanics:</b> SDevice uses the Bank/Rose damped Newton-Raphson solver with Quasistationary continuation stepping.",
        "EXAMINER DEFENSE SUMMARY:",
        bg_color="#fefce8",
        border_color="#ca8a04"
    )
    story.append(final_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully built: {PDF_OUTPUT}")


if __name__ == "__main__":
    build_pdf()
