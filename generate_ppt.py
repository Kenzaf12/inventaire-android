"""
Génère le PPT de soutenance de stage — Inventaire CFC
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Couleurs charte ──────────────────────────────────────────────────────────
DARK   = RGBColor(0x1F, 0x4E, 0x79)   # bleu foncé
MID    = RGBColor(0x26, 0x6F, 0x8E)   # bleu moyen
LIGHT  = RGBColor(0x5A, 0x91, 0xA8)   # bleu clair
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GRAY   = RGBColor(0xF2, 0xF2, 0xF2)
ACCENT = RGBColor(0x61, 0x87, 0x3B)   # vert

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]   # entièrement vide

# ── Helpers ──────────────────────────────────────────────────────────────────
def bg(slide, color=DARK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def rect(slide, l, t, w, h, color, alpha=None):
    from pptx.util import Inches
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def txt(slide, text, l, t, w, h, size=18, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, wrap=True):
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box

def title_slide(title, subtitle, num=""):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, DARK)
    rect(slide, 0, 0, 13.33, 0.08, ACCENT)          # bande verte haut
    rect(slide, 0, 7.42, 13.33, 0.08, ACCENT)        # bande verte bas
    rect(slide, 0, 2.8, 13.33, 2.2, MID)             # bandeau central
    txt(slide, title,    0.5, 2.95, 12.3, 1.0, size=36, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, subtitle, 0.5, 4.05, 12.3, 0.8, size=20,
        color=RGBColor(0xB0,0xD4,0xE3), align=PP_ALIGN.CENTER)
    if num:
        txt(slide, num, 12.8, 7.1, 0.5, 0.3, size=10,
            color=RGBColor(0x80,0xA0,0xB0), align=PP_ALIGN.RIGHT)
    return slide

def content_slide(title, bullets, num=""):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, GRAY)
    rect(slide, 0, 0, 13.33, 1.2, DARK)
    rect(slide, 0, 1.2, 0.07, 6.3, ACCENT)
    txt(slide, title, 0.4, 0.2, 12.5, 0.85, size=28, bold=True,
        color=WHITE, align=PP_ALIGN.LEFT)

    y = 1.45
    for b in bullets:
        indent = b.startswith("  ")
        text   = b.strip()
        if text.startswith("##"):               # sous-titre section
            txt(slide, text[2:].strip(), 0.4, y, 12.5, 0.4, size=15, bold=True,
                color=DARK)
            y += 0.42
        elif text == "---":                      # séparateur visuel
            y += 0.15
        else:
            prefix = "  ▸ " if indent else "▶ "
            fsize  = 14 if indent else 16
            col    = RGBColor(0x33,0x33,0x33) if indent else DARK
            txt(slide, prefix + text, 0.5, y, 12.3, 0.38,
                size=fsize, color=col)
            y += 0.40

    if num:
        txt(slide, num, 12.8, 7.1, 0.5, 0.3, size=10,
            color=RGBColor(0x80,0x80,0x80), align=PP_ALIGN.RIGHT)
    return slide

def two_col_slide(title, left_items, right_items, num=""):
    slide = prs.slides.add_slide(BLANK)
    bg(slide, GRAY)
    rect(slide, 0, 0, 13.33, 1.2, DARK)
    rect(slide, 0, 1.2, 0.07, 6.3, ACCENT)
    txt(slide, title, 0.4, 0.2, 12.5, 0.85, size=28, bold=True,
        color=WHITE)
    # colonnes
    rect(slide, 0.4, 1.35, 5.9, 5.8, WHITE)
    rect(slide, 7.0, 1.35, 5.9, 5.8, WHITE)

    def fill_col(items, lx):
        y = 1.55
        for item in items:
            if item.startswith("##"):
                txt(slide, item[2:], lx+0.15, y, 5.6, 0.38, size=14, bold=True, color=MID)
            else:
                txt(slide, "▶ " + item, lx+0.15, y, 5.6, 0.38, size=13, color=DARK)
            y += 0.42

    fill_col(left_items,  0.4)
    fill_col(right_items, 7.0)
    if num:
        txt(slide, num, 12.8, 7.1, 0.5, 0.3, size=10,
            color=RGBColor(0x80,0x80,0x80), align=PP_ALIGN.RIGHT)
    return slide

# ════════════════════════════════════════════════════════════════════════════
#  SLIDES
# ════════════════════════════════════════════════════════════════════════════

# 1 — Couverture
s = prs.slides.add_slide(BLANK)
bg(s, DARK)
rect(s, 0, 0, 13.33, 0.1, ACCENT)
rect(s, 0, 7.4, 13.33, 0.1, ACCENT)
rect(s, 0, 2.4, 13.33, 2.8, MID)
txt(s, "PRÉSENTATION DE STAGE", 0.5, 0.4, 12.3, 0.5, size=13,
    color=RGBColor(0xB0,0xD4,0xE3), align=PP_ALIGN.CENTER)
txt(s, "Conception & Développement d'une\nApplication Android", 0.5, 2.55, 12.3, 1.2,
    size=34, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Gestion de l'Inventaire Physique — CFC Audit", 0.5, 3.75, 12.3, 0.55,
    size=20, color=RGBColor(0xD4,0xE8,0xC2), align=PP_ALIGN.CENTER)
rect(s, 1.5, 5.5, 10.33, 0.05, RGBColor(0x40,0x80,0xA0))
txt(s, "Réalisé par : Kenza OUDALI", 0.5, 5.65, 6.0, 0.4, size=14,
    color=RGBColor(0xB0,0xD4,0xE3))
txt(s, "Encadrante : Mme Laila MAADIR", 0.5, 6.05, 6.0, 0.4, size=14,
    color=RGBColor(0xB0,0xD4,0xE3))
txt(s, "Année universitaire 2025/2026", 7.0, 5.65, 5.8, 0.4, size=14,
    color=RGBColor(0xB0,0xD4,0xE3), align=PP_ALIGN.RIGHT)
txt(s, "CFC — Casablanca  |  Mai 2026", 7.0, 6.05, 5.8, 0.4, size=14,
    color=RGBColor(0xB0,0xD4,0xE3), align=PP_ALIGN.RIGHT)

# 2 — Sommaire
content_slide("Sommaire", [
    "01 — Introduction & Contexte",
    "02 — Présentation de l'organisme d'accueil",
    "03 — Problématique & Objectifs",
    "04 — Déroulement du stage (Diagramme de Gantt)",
    "05 — Conception du système",
    "06 — Architecture & Technologies",
    "07 — Réalisation",
    "08 — Conclusion & Perspectives",
], "2/16")

# 3 — Introduction
content_slide("Introduction", [
    "Stage de fin d'études — Licence Professionnelle",
    "Durée : [durée du stage] — CFC Audit, Ingénierie & Consulting, Casablanca",
    "---",
    "## Contexte général",
    "La gestion manuelle de l'inventaire physique est source d'erreurs,",
    "  de pertes de temps et de manque de traçabilité",
    "---",
    "## Problématique",
    "Comment digitaliser et automatiser l'inventaire physique des biens",
    "  d'une entreprise de façon fiable, mobile et accessible ?",
], "3/16")

# 4 — Organisme d'accueil
content_slide("Présentation de l'Organisme d'Accueil", [
    "## CFC — Audit, Ingénierie & Consulting Information",
    "Siège : Casablanca, Maroc",
    "Secteur : Audit, conseil, ingénierie informatique",
    "---",
    "## Missions principales",
    "Audit financier et organisationnel",
    "Conseil en systèmes d'information",
    "Ingénierie et développement de solutions métier",
    "---",
    "## Environnement technique existant",
    "Gestion d'inventaire actuellement réalisée sur papier / Excel",
    "Besoin d'une solution mobile moderne et connectée",
], "4/16")

# 5 — Problématique & Objectifs
two_col_slide("Problématique & Objectifs",
    left_items=[
        "## Problèmes identifiés",
        "Saisie manuelle longue et sujette aux erreurs",
        "Pas de traçabilité en temps réel",
        "Aucune solution mobile sur le terrain",
        "Difficulté à identifier les biens rapidement",
        "Exports et rapports chronophages",
    ],
    right_items=[
        "## Objectifs du projet",
        "Application Android connectée au SI",
        "Scan QR code / code-barres automatique",
        "Reconnaissance IA des équipements",
        "Import de classeur Excel (données initiales)",
        "Export Excel & PDF des états d'inventaire",
        "Panneau d'administration des agents",
    ], num="5/16")

# 6 — Gantt
content_slide("Déroulement du Stage — Diagramme de Gantt", [
    "## Phase 1 — Analyse & Spécification  (Semaines 1–2)",
    "Étude de l'existant, recueil des besoins, rédaction du cahier des charges",
    "---",
    "## Phase 2 — Conception  (Semaines 3–4)",
    "Diagrammes UML : cas d'utilisation, séquence, classes",
    "Maquettage des interfaces (wireframes)",
    "---",
    "## Phase 3 — Développement Backend  (Semaines 5–7)",
    "API REST Spring Boot · Base de données · Authentification JWT",
    "---",
    "## Phase 4 — Développement Mobile  (Semaines 8–11)",
    "Application Android (Java) · Retrofit · ZXing · Gemini IA",
    "---",
    "## Phase 5 — Tests & Déploiement  (Semaines 12–13)",
    "Tests unitaires, intégration, recette utilisateur",
    "---",
    "## Phase 6 — Rédaction du rapport  (Semaine 14)",
], "6/16")

# 7 — Acteurs du système
content_slide("Conception — Acteurs du Système", [
    "## Acteurs principaux",
    "Agent d'inventaire — saisit, scanne, photographie les biens sur le terrain",
    "Administrateur — gère les agents, importe les données, consulte les états",
    "Système IA (Gemini) — identifie automatiquement les biens par photo",
    "---",
    "## Cas d'utilisation principaux",
    "S'authentifier (login / JWT)",
    "Consulter et modifier l'inventaire (Équipements & Autres)",
    "Scanner un QR code ou code-barres pour accéder à une fiche",
    "Prendre une photo et l'analyser avec l'IA",
    "Importer un classeur Excel (données initiales)",
    "Exporter les états en Excel ou PDF · Partager par email/WhatsApp",
    "Gérer les agents (ajout, suppression, mot de passe)",
], "7/16")

# 8 — Diagrammes UML
two_col_slide("Conception — Diagrammes UML",
    left_items=[
        "## Diagramme de classes",
        "InventEquipement",
        "InventAutres",
        "Agent / Activite",
        "SessionManager (JWT)",
        "ApiService (Retrofit)",
        "## Diagramme de séquence",
        "Connexion → Token JWT",
        "Scan → Recherche API → Fiche",
        "Photo → Gemini → Résultat",
    ],
    right_items=[
        "## Diagramme de cas d'utilisation",
        "Acteur : Agent",
        "Acteur : Administrateur",
        "Include : Authentification",
        "Extend : Scan / IA",
        "## Diagramme d'activité",
        "Flux : Import Excel → Validation",
        "Flux : Inventaire terrain",
        "Flux : Export & Partage",
    ], num="8/16")

# 9 — Architecture
content_slide("Architecture Globale du Système", [
    "## Couche Mobile (Android)",
    "Java · Retrofit2 · ZXing · Gemini AI API · FileProvider",
    "---",
    "## Couche Backend (Serveur entreprise)",
    "Spring Boot (Java) · API REST · JWT Authentication",
    "Base de données relationnelle · Gestion fichiers (photos, Excel)",
    "---",
    "## Couche Web (Interface administrateur)",
    "Interface web complémentaire pour la gestion centralisée",
    "---",
    "## Communication",
    "HTTPS · JSON · Authentification Bearer Token (JWT)",
    "Upload multipart (photos) · Download fichiers (Excel / PDF)",
    "---",
    "[ Voir figure : Architecture complète ci-après ]",
], "9/16")

# 10 — Figure Architecture (placeholder)
s10 = prs.slides.add_slide(BLANK)
bg(s10, GRAY)
rect(s10, 0, 0, 13.33, 1.2, DARK)
rect(s10, 0, 1.2, 0.07, 6.3, ACCENT)
txt(s10, "Architecture Technique Complète", 0.4, 0.2, 12.5, 0.85,
    size=28, bold=True, color=WHITE)

# Schéma ASCII en boîtes
boxes = [
    # (l, t, w, h, color, label)
    (0.3,  2.0, 3.0, 3.5, LIGHT,  "📱 APPLICATION\nANDROID\n\nJava\nRetrofit2\nZXing\nGemini AI"),
    (5.0,  1.5, 3.5, 1.2, MID,    "🔐 Auth JWT"),
    (5.0,  3.0, 3.5, 1.2, MID,    "📦 API REST\nSpring Boot"),
    (5.0,  4.5, 3.5, 1.2, MID,    "🗄️ Base de données"),
    (9.5,  2.0, 3.3, 1.5, ACCENT, "🌐 Interface Web\nAdmin"),
    (9.5,  4.0, 3.3, 1.5, RGBColor(0x7B,0x3F,0xA0), "🤖 Gemini AI\n(Google)"),
]
for (l,t,w,h,col,label) in boxes:
    r = s10.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = col
    r.line.color.rgb = WHITE; r.line.width = Pt(1)
    tf = r.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = label
    run.font.size = Pt(13); run.font.color.rgb = WHITE; run.font.bold = True

# Flèches texte
txt(s10, "⟷  HTTPS / JSON", 3.35, 3.3, 1.6, 0.4, size=11,
    color=DARK, align=PP_ALIGN.CENTER)
txt(s10, "⟷", 8.55, 2.5, 0.9, 0.4, size=18, color=DARK, align=PP_ALIGN.CENTER)
txt(s10, "⟷", 8.55, 4.5, 0.9, 0.4, size=18, color=DARK, align=PP_ALIGN.CENTER)
txt(s10, "10/16", 12.8, 7.1, 0.5, 0.3, size=10,
    color=RGBColor(0x80,0x80,0x80), align=PP_ALIGN.RIGHT)

# 11 — Technologies
two_col_slide("Technologies Utilisées",
    left_items=[
        "## Backend",
        "Java Spring Boot — API REST",
        "JWT — Authentification sécurisée",
        "JPA / Hibernate — ORM",
        "Apache POI — Génération Excel",
        "MySQL / PostgreSQL",
        "## Web",
        "HTML · CSS · JavaScript",
        "Thymeleaf / Angular (interface admin)",
    ],
    right_items=[
        "## Mobile (Android)",
        "Java — Langage principal",
        "Retrofit2 + OkHttp — Appels API",
        "ZXing — Scan QR / Code-barres",
        "Gemini AI API — Reconnaissance IA",
        "Material Design 3 — UI/UX",
        "FileProvider — Partage fichiers",
        "SharedPreferences — Session JWT",
    ], num="11/16")

# 12 — Réalisation : Login & Dashboard
content_slide("Réalisation — Authentification & Tableau de Bord", [
    "## Écran de connexion",
    "Login + mot de passe · Validation JWT · Redirection selon rôle (Admin / Agent)",
    "---",
    "## Tableau de bord",
    "4 tuiles : Inventaire Équipements · Inventaire Autres",
    "États & Export · Administration (visible Admin uniquement)",
    "Bandeau Bonjour [Prénom Nom] · Bouton déconnexion",
    "---",
    "[ Insérer captures d'écran : Login + Dashboard ]",
], "12/16")

# 13 — Réalisation : Inventaire & Scan
content_slide("Réalisation — Inventaire & Scan", [
    "## Liste des équipements / autres",
    "RecyclerView avec carte par article",
    "Recherche en temps réel · Filtre par état",
    "---",
    "## Fiche détail",
    "Tous les champs éditables · Spinner État & Validé",
    "Date/heure inventaire automatique",
    "Prise de photo (caméra ou galerie)",
    "Bouton Sauvegarder · Bouton Supprimer (header)",
    "---",
    "## Scanner QR code / Code-barres",
    "ZXing : scan via caméra → fiche s'ouvre automatiquement",
    "Recherche par CAB si code simple · JSON structuré si QR",
    "---",
    "[ Insérer captures : Liste · Fiche détail · Scanner ]",
], "13/16")

# 14 — Réalisation : IA & Export
content_slide("Réalisation — Reconnaissance IA & Export", [
    "## Reconnaissance IA (Gemini)",
    "Photo prise ou importée depuis galerie",
    "Envoi à l'API Gemini · Retour : type de bien + description",
    "Utilisation du résultat pour pré-remplir une nouvelle fiche",
    "---",
    "## Export & Partage",
    "Export Excel (.xlsx) : Équipements, Autres, État récapitulatif",
    "Export PDF : rapport par catégorie et rapport global",
    "Dialogue de partage natif Android (email, WhatsApp, Drive…)",
    "---",
    "## Administration",
    "Liste des agents · Dialogue détail : infos, mot de passe, activités",
    "Ajout / Suppression d'agent · Changer mot de passe",
    "Import de classeur Excel pour initialiser l'inventaire",
    "---",
    "[ Insérer captures : IA · Export · Admin ]",
], "14/16")

# 15 — Conclusion
content_slide("Conclusion & Perspectives", [
    "## Bilan du stage",
    "Application Android fonctionnelle et déployable",
    "Toutes les fonctionnalités clés livrées et testées",
    "Expérience complète : analyse → conception → développement → tests",
    "---",
    "## Compétences acquises",
    "Développement Android (Java, Material Design, Architecture REST)",
    "Intégration d'une IA dans une app mobile (Gemini API)",
    "Travail en équipe, gestion de projet, communication client",
    "---",
    "## Perspectives d'amélioration",
    "Synchronisation hors-ligne (mode offline avec Room DB)",
    "Notifications push pour les alertes d'inventaire",
    "Tableau de bord statistique avec graphiques",
    "Version iOS de l'application",
], "15/16")

# 16 — Merci
s_end = prs.slides.add_slide(BLANK)
bg(s_end, DARK)
rect(s_end, 0, 0, 13.33, 0.1, ACCENT)
rect(s_end, 0, 7.4, 13.33, 0.1, ACCENT)
rect(s_end, 0, 3.0, 13.33, 1.8, MID)
txt(s_end, "Merci pour votre attention", 0.5, 3.15, 12.3, 0.9,
    size=38, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s_end, "Questions ?", 0.5, 4.1, 12.3, 0.5,
    size=22, color=RGBColor(0xD4,0xE8,0xC2), align=PP_ALIGN.CENTER)
txt(s_end, "Kenza OUDALI — Stage CFC Audit, Ingénierie & Consulting — 2025/2026",
    0.5, 6.5, 12.3, 0.5, size=13,
    color=RGBColor(0x80,0xA0,0xB0), align=PP_ALIGN.CENTER)

# ── Sauvegarde ───────────────────────────────────────────────────────────────
out = "soutenance_stage_inventaire_cfc.pptx"
prs.save(out)
print(f"✅  {out} créé ({prs.slides.__len__()} slides)")
