# -*- coding: utf-8 -*-
"""
Présentation de soutenance — InventaireCFC
python generate_ppt.py
"""

import os, math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# ── couleurs ─────────────────────────────────────────────────────────────────
DARK   = RGBColor(0x1B, 0x34, 0x4A)
TEAL   = RGBColor(0x26, 0x6F, 0x8E)
GREEN  = RGBColor(0x5A, 0x7D, 0x2B)
LIGHT  = RGBColor(0xF3, 0xF6, 0xF8)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREY   = RGBColor(0x77, 0x88, 0x90)
SMOKE  = RGBColor(0xE8, 0xED, 0xF0)
BLACK  = RGBColor(0x00, 0x00, 0x00)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ppt_assets")

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK  = prs.slide_layouts[6]

# ── utilitaires ──────────────────────────────────────────────────────────────
def slide(): return prs.slides.add_slide(BLANK)

def bg(s, color):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = color

def box(s, x, y, w, h, fill, line_color=None, line_w=None, radius=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shp = s.shapes.add_shape(shape_type, x, y, w, h)
    if radius:
        shp.adjustments[0] = 0.05
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line_color:
        shp.line.color.rgb = line_color
        if line_w: shp.line.width = line_w
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp

def txt(s, x, y, w, h, text, size=18, color=DARK, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for i, ln in enumerate(text.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold
        r.font.italic = italic; r.font.color.rgb = color
        r.font.name = "Calibri"
    return tb

def blist(s, x, y, w, h, items, size=16, color=DARK, gap=6, bullet="•"):
    tb = s.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        r = p.add_run(); r.text = f"{bullet}  {it}"
        r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Calibri"

def A(stem):
    for f in sorted(os.listdir(ASSETS)):
        if f.startswith(stem + "_"): return os.path.join(ASSETS, f)
    return ""

def img_fit(s, path, x, y, w, h, valign="middle"):
    if not path or not os.path.exists(path):
        box(s, x, y, w, h, LIGHT); return
    iw, ih = Image.open(path).size
    ratio = min(w / iw, h / ih)
    nw, nh = int(iw * ratio), int(ih * ratio)
    nx = x + (w - nw) // 2
    ny = y + (h - nh) // 2 if valign == "middle" else (y if valign == "top" else y + h - nh)
    s.shapes.add_picture(path, nx, ny, nw, nh)

def header(s, title, num=None):
    bg(s, WHITE)
    box(s, 0, 0, SW, Inches(1.05), TEAL)
    box(s, 0, Inches(1.05), SW, Inches(0.07), GREEN)
    txt(s, Inches(0.5), 0, Inches(10.8), Inches(1.05), title,
        24, WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    img_fit(s, A("p01_3"), Inches(11.7), Inches(0.18), Inches(1.35), Inches(0.7))
    if num:
        txt(s, Inches(12.4), Inches(7.05), Inches(0.8), Inches(0.35),
            str(num), 11, GREY, align=PP_ALIGN.RIGHT)

def iphone_frame(s, cx, cy, phone_w, phone_h):
    """Dessine un cadre iPhone centré en (cx,cy) de taille phone_w x phone_h."""
    r  = Emu(phone_w * 0.12)   # rayon arrondi
    bw = Emu(phone_w * 0.05)   # épaisseur bordure
    # corps
    body = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               cx - phone_w//2, cy - phone_h//2, phone_w, phone_h)
    body.adjustments[0] = 0.12
    body.fill.solid(); body.fill.fore_color.rgb = RGBColor(0x1C,0x1C,0x1E)
    body.line.color.rgb = RGBColor(0x3A,0x3A,0x3C); body.line.width = Emu(18000)
    body.shadow.inherit = False
    # écran
    pad_x = Emu(phone_w * 0.07)
    pad_top = Emu(phone_h * 0.10)
    pad_bot = Emu(phone_h * 0.10)
    sx = cx - phone_w//2 + pad_x
    sy = cy - phone_h//2 + pad_top
    sw = phone_w - pad_x*2
    sh = phone_h - pad_top - pad_bot
    scr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, sx, sy, sw, sh)
    scr.fill.solid(); scr.fill.fore_color.rgb = RGBColor(0xE0,0xE8,0xEE)
    scr.line.fill.background(); scr.shadow.inherit = False
    # notch
    nw, nh = Emu(phone_w*0.3), Emu(phone_h*0.035)
    notch = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                cx - nw//2, cy - phone_h//2 + Emu(phone_h*0.005), nw, nh)
    notch.adjustments[0] = 0.5
    notch.fill.solid(); notch.fill.fore_color.rgb = RGBColor(0x1C,0x1C,0x1E)
    notch.line.fill.background(); notch.shadow.inherit = False
    # home bar
    hbw, hbh = Emu(phone_w*0.28), Emu(phone_h*0.012)
    hbar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                               cx - hbw//2, cy + phone_h//2 - Emu(phone_h*0.06), hbw, hbh)
    hbar.adjustments[0] = 0.5
    hbar.fill.solid(); hbar.fill.fore_color.rgb = RGBColor(0x88,0x88,0x88)
    hbar.line.fill.background(); hbar.shadow.inherit = False
    return sx, sy, sw, sh   # zone écran

# ═════════════════════════════════════════════════════════════════════════════
# 1 — COUVERTURE
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
bg(s, WHITE)
box(s, 0, 0, Inches(0.4), SH, TEAL)
box(s, Inches(0.4), 0, Inches(0.1), SH, GREEN)
img_fit(s, A("p01_0"), Inches(1.2),  Inches(0.25), Inches(1.55), Inches(1.55))
img_fit(s, A("p01_1"), Inches(5.85), Inches(0.35), Inches(1.55), Inches(1.45))
img_fit(s, A("p01_2"), Inches(9.6),  Inches(0.5),  Inches(2.7),  Inches(1.15))

box(s, Inches(1.2), Inches(2.05), Inches(11.2), Inches(0.06), GREEN)
txt(s, Inches(1.2), Inches(2.2), Inches(11.2), Inches(0.5),
    "RAPPORT DE STAGE   —   SOUTENANCE", 14, TEAL, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(1.2), Inches(2.85), Inches(11.2), Inches(1.5),
    "Conception et Développement d'une Application Android\nIntelligente pour la Gestion de l'Inventaire Physique",
    30, DARK, bold=True, align=PP_ALIGN.CENTER)

img_fit(s, A("p01_3"), Inches(5.55), Inches(4.2), Inches(2.25), Inches(0.95))
txt(s, Inches(1.0), Inches(5.2), Inches(11.4), Inches(0.5),
    "Audit, Ingénierie en Consulting et Formation — Casablanca",
    15, GREY, align=PP_ALIGN.CENTER, italic=True)
box(s, Inches(1.8), Inches(5.85), Inches(9.8), Inches(1.2), SMOKE, radius=True)
txt(s, Inches(2.2), Inches(5.98), Inches(4.8), Inches(0.95),
    "Réalisé par :\nKenza FOUDALI", 15, DARK, bold=True)
txt(s, Inches(7.1), Inches(5.98), Inches(4.3), Inches(0.95),
    "Encadrante :\nMme Laila MAADIR", 15, DARK, bold=True)
txt(s, Inches(1.0), Inches(7.08), Inches(11.4), Inches(0.35),
    "Année Universitaire 2025 / 2026   ·   04 mai – 13 juin 2026",
    12, GREY, align=PP_ALIGN.CENTER)

# ═════════════════════════════════════════════════════════════════════════════
# 2 — PLAN
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Plan de la présentation", 2)
plan = [
    ("01", "Introduction & Contexte"),
    ("02", "Présentation de l'organisme"),
    ("03", "Objectifs du projet"),
    ("04", "Gestion du projet"),
    ("05", "Conception UML"),
    ("06", "Technologies utilisées"),
    ("07", "Architecture du système"),
    ("08", "Présentation de la plateforme"),
    ("09", "Perspectives d'évolution"),
    ("10", "Conclusion"),
]
col1, col2 = plan[:5], plan[5:]
for col, ox in [(col1, Inches(1.2)), (col2, Inches(7.2))]:
    for i, (num, label) in enumerate(col):
        y = Inches(1.55) + i * Inches(1.0)
        box(s, ox, y, Inches(0.55), Inches(0.55), TEAL, radius=True)
        txt(s, ox, y, Inches(0.55), Inches(0.55), num, 18, WHITE, bold=True,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        txt(s, Emu(ox + Inches(0.7)), Emu(y + Inches(0.1)),
            Inches(5.3), Inches(0.45), label, 18, DARK, bold=False,
            anchor=MSO_ANCHOR.MIDDLE)

# ═════════════════════════════════════════════════════════════════════════════
# 3 — INTRODUCTION & CONTEXTE  (transformation papier → mobile)
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Introduction & Contexte", 3)

txt(s, Inches(0.7), Inches(1.3), Inches(11.9), Inches(0.85),
    "CF Consult réalise régulièrement des missions d'inventaire physique sur le "
    "terrain. L'objectif du projet : faire passer cette activité du papier au "
    "mobile, avec un outil moderne, rapide et intelligent.",
    17, DARK)

# ── HIER (carte grise) ──────────────────────────────────────────────────────
box(s, Inches(0.7), Inches(2.55), Inches(4.4), Inches(4.3), SMOKE, radius=True)
txt(s, Inches(0.7), Inches(2.7), Inches(4.4), Inches(0.55),
    "Hier", 20, GREY, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(0.7), Inches(3.35), Inches(4.4), Inches(1.0),
    "📋   📝   📊", 40, GREY, align=PP_ALIGN.CENTER)
blist(s, Inches(1.1), Inches(4.6), Inches(3.7), Inches(2.1), [
    "Fiches papier sur le terrain",
    "Re-saisie manuelle sur Excel",
    "Pas de photo ni de géolocalisation",
    "Suivi difficile en temps réel",
], size=14, color=DARK, gap=11, bullet="–")

# ── FLÈCHE centrale ─────────────────────────────────────────────────────────
arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW,
                           Inches(5.35), Inches(4.05), Inches(2.6), Inches(1.3))
arrow.fill.solid(); arrow.fill.fore_color.rgb = GREEN
arrow.line.fill.background(); arrow.shadow.inherit = False
txt(s, Inches(5.35), Inches(4.05), Inches(2.6), Inches(1.3),
    "Digitalisation", 15, WHITE, bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(5.35), Inches(3.45), Inches(2.6), Inches(0.5),
    "Application mobile", 13, GREEN, bold=True, align=PP_ALIGN.CENTER)

# ── AUJOURD'HUI (carte teal) ────────────────────────────────────────────────
box(s, Inches(8.2), Inches(2.55), Inches(4.4), Inches(4.3), TEAL, radius=True)
txt(s, Inches(8.2), Inches(2.7), Inches(4.4), Inches(0.55),
    "Aujourd'hui", 20, WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(8.2), Inches(3.35), Inches(4.4), Inches(1.0),
    "📱", 46, WHITE, align=PP_ALIGN.CENTER)
blist(s, Inches(8.6), Inches(4.6), Inches(3.7), Inches(2.1), [
    "Scan QR / code-barres instantané",
    "Photo & reconnaissance par IA",
    "Saisie & validation en un geste",
    "Export Excel / PDF immédiat",
], size=14, color=WHITE, gap=11, bullet="+")

# ═════════════════════════════════════════════════════════════════════════════
# 4 — PRÉSENTATION DE L'ORGANISME
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Présentation de CF Consult", 4)
img_fit(s, A("p01_3"), Inches(0.7), Inches(1.4), Inches(3.8), Inches(1.45))
box(s, Inches(0.7), Inches(3.05), Inches(3.8), Inches(3.7), SMOKE, radius=True)
blist(s, Inches(0.9), Inches(3.2), Inches(3.5), Inches(3.4), [
    "Audit & commissariat aux comptes",
    "Expertise comptable",
    "Conseil & ingénierie",
    "Digitalisation des SI",
    "Gestion des immobilisations",
    "Formation & recrutement",
], size=14, gap=11)
img_fit(s, A("p17_1"), Inches(5.0), Inches(1.35), Inches(7.8), Inches(2.5))
img_fit(s, A("p18_1"), Inches(5.2), Inches(3.9),  Inches(7.4), Inches(3.35))

# ═════════════════════════════════════════════════════════════════════════════
# 5 — OBJECTIFS (+ prompt Napkin)
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Objectifs du projet", 5)

goals = [
    ("🔐", "Authentification",  "Login JWT\nAgent & Admin"),
    ("📥", "Import données",    "Fichier Excel\ncomptable"),
    ("📷", "Scan & Photo",      "QR code,\ncode-barres"),
    ("🤖", "IA Gemini",         "Reconnaissance\nd'objets"),
    ("📊", "Dashboard",         "Tableau de bord\nadmin"),
    ("📤", "Export",            "Excel & PDF\ninstantané"),
]
w, gap = Inches(1.95), Inches(0.2)
total = w*6 + gap*5
x0 = Emu((SW - total) // 2)
for i, (icon, title, desc) in enumerate(goals):
    x = Emu(x0 + i*(w + gap))
    box(s, x, Inches(1.55), w, Inches(4.9),
        TEAL if i % 2 == 0 else SMOKE, radius=True)
    txt(s, x, Inches(1.7), w, Inches(0.9), icon, 34,
        WHITE if i%2==0 else TEAL, align=PP_ALIGN.CENTER)
    txt(s, x, Inches(2.7), w, Inches(0.55), title, 15,
        WHITE if i%2==0 else DARK, bold=True, align=PP_ALIGN.CENTER)
    txt(s, x, Inches(3.35), w, Inches(0.9), desc, 13,
        RGBColor(0xD0,0xE8,0xF0) if i%2==0 else GREY,
        align=PP_ALIGN.CENTER)

# Prompt Napkin
box(s, Inches(0.7), Inches(6.55), Inches(11.9), Inches(0.7),
    RGBColor(0xFF,0xF8,0xE1), radius=True)
txt(s, Inches(0.95), Inches(6.58), Inches(11.5), Inches(0.6),
    "💡 Napkin : 6 feature icons connected to a mobile phone — "
    "Login, QR Scan, AI recognition, Photo, Dashboard, Export — clean flat style",
    13, RGBColor(0x99,0x77,0x00), italic=True)

# ═════════════════════════════════════════════════════════════════════════════
# 6 — GANTT
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Gestion du projet — Diagramme de Gantt", 6)
img_fit(s, A("p28_0"), Inches(0.4), Inches(1.3), Inches(12.5), Inches(5.9))

# ═════════════════════════════════════════════════════════════════════════════
# 7 — UML : CAS D'UTILISATION
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Conception UML — Cas d'utilisation", 7)
img_fit(s, A("p33_0"), Inches(4.1), Inches(1.2), Inches(5.4), Inches(6.1))
box(s, Inches(0.5), Inches(1.5), Inches(3.4), Inches(5.6), SMOKE, radius=True)
txt(s, Inches(0.7), Inches(1.65), Inches(3.1), Inches(0.5), "Acteurs", 17, TEAL, bold=True)
blist(s, Inches(0.7), Inches(2.3), Inches(3.0), Inches(2.4), [
    "Agent d'inventaire",
    "Administrateur",
], size=15, gap=14)
txt(s, Inches(0.7), Inches(4.0), Inches(3.1), Inches(0.5), "Cas principaux", 17, TEAL, bold=True)
blist(s, Inches(0.7), Inches(4.6), Inches(3.0), Inches(2.3), [
    "Se connecter",
    "Scanner QR / CAB",
    "Saisir & valider un bien",
    "Photographier & IA",
    "Exporter les rapports",
    "Gérer les agents",
], size=14, gap=10)
# Accolade décorative
box(s, Inches(3.95), Inches(1.5), Inches(0.05), Inches(5.6), TEAL)

# ═════════════════════════════════════════════════════════════════════════════
# 8 — UML : CLASSES
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Conception UML — Diagramme de classes", 8)
img_fit(s, A("p35_0"), Inches(1.8), Inches(1.25), Inches(9.7), Inches(6.0))

# ═════════════════════════════════════════════════════════════════════════════
# 9 — TECHNOLOGIES (logos uniquement)
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Technologies utilisées", 9)

# Catégories + logos
cats = [
    ("Backend", TEAL,  ["p49_0", "p49_1", "p50_0", "p50_1"]),
    ("Base de données", GREEN, ["p53_0"]),
    ("Mobile", DARK, ["p54_0", "p55_0", "p56_1"]),
    ("IA & Outils", RGBColor(0x6A,0x3D,0x9A), ["p52_0", "p53_1", "p54_1"]),
]

col_w = Inches(3.1)
cx = Inches(0.5)
for cat, color, logos in cats:
    box(s, cx, Inches(1.35), col_w, Inches(0.5), color, radius=True)
    txt(s, cx, Inches(1.35), col_w, Inches(0.5), cat, 15, WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # logos dans une grille 2x2
    logo_h = Inches(2.5) if len(logos) <= 2 else Inches(1.3)
    lx = cx
    for j, stem in enumerate(logos):
        col = j % 2
        row = j // 2
        lx2 = cx + col * Inches(1.5)
        ly2 = Inches(2.0) + row * Inches(2.55)
        img_fit(s, A(stem), lx2, ly2, Inches(1.45), Inches(1.4))
    cx = Emu(cx + col_w + Inches(0.18))

# ═════════════════════════════════════════════════════════════════════════════
# 10 — ARCHITECTURE (générée proprement)
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Architecture du système", 10)
bg(s, WHITE)
box(s, 0, 0, SW, Inches(1.05), TEAL)
box(s, 0, Inches(1.05), SW, Inches(0.07), GREEN)
txt(s, Inches(0.5), 0, Inches(10.8), Inches(1.05), "Architecture du système",
    24, WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
img_fit(s, A("p01_3"), Inches(11.7), Inches(0.18), Inches(1.35), Inches(0.7))

# Couche présentation (gauche)
box(s, Inches(0.5), Inches(1.4), Inches(3.2), Inches(5.6), RGBColor(0xE3,0xF2,0xFD), radius=True)
txt(s, Inches(0.5), Inches(1.5), Inches(3.2), Inches(0.5),
    "📱  Application Android", 14, DARK, bold=True, align=PP_ALIGN.CENTER)
blist(s, Inches(0.7), Inches(2.15), Inches(2.8), Inches(3.5), [
    "Java natif",
    "Login JWT",
    "Scan QR / CAB",
    "Photo + IA Gemini",
    "Recherche & validation",
    "Export Excel / PDF",
], size=13, gap=10, color=DARK)
txt(s, Inches(0.5), Inches(6.6), Inches(3.2), Inches(0.35),
    "Couche présentation", 12, TEAL, bold=True, align=PP_ALIGN.CENTER)

# flèche HTTP REST
for y_offset in [Inches(2.8), Inches(3.8)]:
    shp = s.shapes.add_connector(1, Inches(3.7), y_offset, Inches(4.9), y_offset)
    shp.line.color.rgb = TEAL; shp.line.width = Emu(20000)
arrow_labels = ["HTTP REST / JSON ▶", "◀ JSON Response"]
for i, (lbl, y_off) in enumerate(zip(arrow_labels, [Inches(2.5), Inches(3.5)])):
    txt(s, Inches(3.7), y_off, Inches(1.25), Inches(0.35),
        lbl, 10, TEAL, italic=True, align=PP_ALIGN.CENTER)

# Couche métier (centre)
box(s, Inches(4.9), Inches(1.4), Inches(3.6), Inches(5.6), TEAL, radius=True)
txt(s, Inches(4.9), Inches(1.55), Inches(3.6), Inches(0.5),
    "⚙  Backend Spring Boot", 14, WHITE, bold=True, align=PP_ALIGN.CENTER)
blist(s, Inches(5.1), Inches(2.2), Inches(3.2), Inches(3.5), [
    "API REST / JSON",
    "Spring Security + JWT",
    "Controller → Service",
    "Repository (JPA)",
    "Import / Export Excel",
    "Génération QR Code",
    "Proxy API Gemini",
], size=13, gap=9, color=WHITE, bullet="›")
txt(s, Inches(4.9), Inches(6.6), Inches(3.6), Inches(0.35),
    "Couche métier", 12, WHITE, bold=True, align=PP_ALIGN.CENTER)

# flèche JDBC
for y_offset in [Inches(2.8), Inches(3.8)]:
    shp2 = s.shapes.add_connector(1, Inches(8.5), y_offset, Inches(9.6), y_offset)
    shp2.line.color.rgb = GREEN; shp2.line.width = Emu(20000)
for lbl2, y_off2 in zip(["JDBC / JPA ▶", "◀ Data"], [Inches(2.5), Inches(3.5)]):
    txt(s, Inches(8.5), y_off2, Inches(1.1), Inches(0.35),
        lbl2, 10, GREEN, italic=True, align=PP_ALIGN.CENTER)

# Couche données (droite)
box(s, Inches(9.6), Inches(1.4), Inches(3.2), Inches(5.6), RGBColor(0xE8,0xF5,0xE9), radius=True)
txt(s, Inches(9.6), Inches(1.55), Inches(3.2), Inches(0.5),
    "🗄  PostgreSQL", 14, DARK, bold=True, align=PP_ALIGN.CENTER)
blist(s, Inches(9.8), Inches(2.2), Inches(2.8), Inches(3.5), [
    "InventEquipement",
    "InventAutres",
    "Localisation",
    "Agent",
    "Etat",
    "Activite (logs)",
], size=13, gap=10, color=DARK)
txt(s, Inches(9.6), Inches(6.6), Inches(3.2), Inches(0.35),
    "Couche données", 12, GREEN, bold=True, align=PP_ALIGN.CENTER)

# Gemini en haut
box(s, Inches(5.5), Inches(1.42), Inches(2.3), Inches(0.55),
    RGBColor(0xED,0xE7,0xF6), radius=True)
txt(s, Inches(5.5), Inches(1.42), Inches(2.3), Inches(0.55),
    "🤖 Google Gemini AI", 12, RGBColor(0x6A,0x3D,0x9A), bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ═════════════════════════════════════════════════════════════════════════════
# 11, 12, 13 — PRÉSENTATION PLATEFORME (cadres iPhone)
# ═════════════════════════════════════════════════════════════════════════════
phone_w = Inches(3.0)
phone_h = Inches(5.8)
cy_phone = Inches(4.35)

for slide_num, (title, subtitle, color, img_stem, bullets_list) in enumerate([
    ("Interface Administrateur", "Gestion des agents · Import · Tableau de bord",
     TEAL, "p70_1", ["Import fichier Excel comptable", "Gestion des agents", "Suivi des activités"]),
    ("Interface Agent", "Login · Inventaire · Scan · Export",
     GREEN, "p65_1", ["Connexion sécurisée JWT", "Inventaire équipements & autres", "Scan QR / code-barres"]),
    ("Reconnaissance par IA", "Photo → Gemini → Identification automatique",
     RGBColor(0x6A,0x3D,0x9A), "p68_1", ["Photo via caméra ou galerie", "Analyse Gemini 2.5 Flash", "Champs pré-remplis automatiquement"]),
], 11):
    s = slide()
    header(s, title, slide_num)
    txt(s, Inches(0.5), Inches(1.2), Inches(12.3), Inches(0.4),
        subtitle, 15, GREY, italic=True, align=PP_ALIGN.CENTER)

    # 3 cadres iPhone côte à côte
    positions = [Inches(1.2), Inches(5.15), Inches(9.1)]
    phone_imgs = [img_stem, "p66_1" if slide_num < 13 else "p64_1",
                  "p69_1" if slide_num < 13 else "p68_1"]
    labels = ["Vue principale", "Vue liste", "Vue export"] if slide_num == 12 \
             else (["Dashboard", "Inventaire", "Export"] if slide_num == 11
                   else ["Photo", "Analyse", "Résultat"])

    for cx_phone, ph_img, lbl in zip(positions, phone_imgs, labels):
        sx, sy, sw2, sh2 = iphone_frame(s,
                                         Emu(cx_phone + phone_w//2),
                                         cy_phone, phone_w, phone_h)
        img_fit(s, A(ph_img), sx, sy, sw2, sh2, valign="top")
        txt(s, cx_phone, Inches(7.08), phone_w, Inches(0.35),
            lbl, 13, color, bold=True, align=PP_ALIGN.CENTER)

    # légende bullets
    blist(s, Inches(0.3), Inches(6.4), Inches(12.7), Inches(0.9),
          bullets_list, size=13, color=DARK, gap=0,
          bullet="·")


# ═════════════════════════════════════════════════════════════════════════════
# 14 — PERSPECTIVES D'ÉVOLUTION
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Perspectives d'évolution", 14)

persp = [
    ("📶", "Mode hors-ligne",   "Synchronisation différée\nquand le réseau revient"),
    ("🏷", "Étiquettes QR",     "Impression d'étiquettes\ndirectement depuis l'app"),
    ("🌍", "Multi-sites",       "Gestion de plusieurs\nentreprises et sites"),
    ("📈", "Analytics avancés", "Tableaux de bord\nstatistiques & KPIs"),
]
box_w = Inches(2.9)
bx = Inches(0.7)
for icon, title, desc in persp:
    box(s, bx, Inches(1.55), box_w, Inches(4.1), SMOKE, radius=True)
    box(s, bx, Inches(1.55), box_w, Inches(0.08), GREEN)
    txt(s, bx, Inches(1.8), box_w, Inches(1.0), icon, 45,
        TEAL, align=PP_ALIGN.CENTER)
    txt(s, bx, Inches(2.95), box_w, Inches(0.55), title, 16,
        DARK, bold=True, align=PP_ALIGN.CENTER)
    txt(s, bx, Inches(3.6), box_w, Inches(1.9), desc, 14,
        GREY, align=PP_ALIGN.CENTER)
    bx = Emu(bx + box_w + Inches(0.2))

# Prompt Napkin
box(s, Inches(0.7), Inches(6.0), Inches(11.9), Inches(1.1),
    RGBColor(0xFF,0xF8,0xE1), radius=True)
txt(s, Inches(0.95), Inches(6.08), Inches(11.5), Inches(0.9),
    "💡 Napkin : 4 futuristic roadmap cards going upward — "
    "Offline mode, QR labels, Multi-site, Analytics dashboard — "
    "connected by a glowing timeline, blue-green gradient",
    13, RGBColor(0x99,0x77,0x00), italic=True)

# ═════════════════════════════════════════════════════════════════════════════
# 15 — CONCLUSION
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
header(s, "Conclusion", 15)
txt(s, Inches(1.2), Inches(1.6), Inches(10.9), Inches(1.5),
    "Ce stage m'a permis de concevoir et développer, de A à Z, une solution "
    "complète de gestion d'inventaire physique combinant un backend Spring Boot "
    "sécurisé, une application Android native et une intelligence artificielle "
    "de reconnaissance d'objets.", 19, DARK)

box(s, Inches(1.2), Inches(3.35), Inches(10.9), Inches(0.07), GREEN)

apports = [
    "Maîtrise de l'architecture trois tiers (Android · REST · PostgreSQL)",
    "Intégration d'une IA dans une solution métier réelle",
    "Gestion complète d'un projet informatique sur 6 semaines",
]
blist(s, Inches(1.4), Inches(3.6), Inches(10.5), Inches(2.0),
      apports, size=18, color=TEAL, gap=14)

txt(s, Inches(1.2), Inches(5.85), Inches(10.9), Inches(1.3),
    "Une expérience enrichissante qui a transformé un processus manuel "
    "et faillible en un outil mobile moderne, rapide et intelligent.",
    18, DARK, italic=True)

# ═════════════════════════════════════════════════════════════════════════════
# 16 — MERCI
# ═════════════════════════════════════════════════════════════════════════════
s = slide()
bg(s, DARK)
box(s, 0, Inches(2.7), SW, Inches(0.1), TEAL)
box(s, 0, Inches(4.85), SW, Inches(0.1), GREEN)
txt(s, 0, Inches(2.9), SW, Inches(1.4),
    "Merci pour votre attention", 44, WHITE, bold=True,
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, 0, Inches(4.3), SW, Inches(0.5),
    "Avez-vous des questions ?", 22, TEAL,
    align=PP_ALIGN.CENTER)
txt(s, 0, Inches(6.75), SW, Inches(0.5),
    "Kenza FOUDALI  ·  CF Consult  ·  2025 / 2026",
    13, RGBColor(0x88,0x99,0xAA), align=PP_ALIGN.CENTER)

# ── sauvegarde ───────────────────────────────────────────────────────────────
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "soutenance_stage_inventaire_cfc.pptx")
prs.save(out)
print(f"✅  {out}  ({len(prs.slides._sldIdLst)} slides)")
