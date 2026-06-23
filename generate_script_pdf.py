from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = landscape(A4)
TEAL   = colors.HexColor("#1E8875")
LTEAL  = colors.HexColor("#E8F7F3")
DARK   = colors.HexColor("#1A1A2E")
GREY   = colors.HexColor("#555555")
LGREY  = colors.HexColor("#F5F5F5")
AMBER  = colors.HexColor("#FF8F00")
WHITE  = colors.white

styles = getSampleStyleSheet()

def S(name, **kw):
    base = styles["Normal"]
    return ParagraphStyle(name, parent=base, **kw)

TITLE_S  = S("title",  fontSize=26, textColor=WHITE,      alignment=TA_CENTER, spaceAfter=6, leading=32, fontName="Helvetica-Bold")
SUB_S    = S("sub",    fontSize=14, textColor=WHITE,      alignment=TA_CENTER, spaceAfter=4, leading=18)
SECHEAD  = S("sech",   fontSize=13, textColor=WHITE,      backColor=TEAL, leading=20, fontName="Helvetica-Bold", leftIndent=8, spaceBefore=10, spaceAfter=4)
SLNUM_S  = S("slnum",  fontSize=10, textColor=TEAL,       fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=2)
SLTIT_S  = S("sltit",  fontSize=12, textColor=DARK,       fontName="Helvetica-Bold", spaceBefore=2, spaceAfter=3)
BODY_S   = S("body",   fontSize=10, textColor=GREY,       leading=15, spaceAfter=2)
Q_S      = S("q",      fontSize=10, textColor=TEAL,       fontName="Helvetica-Bold", backColor=LTEAL, leftIndent=6, leading=14, spaceBefore=6, spaceAfter=2)
A_S      = S("a",      fontSize=10, textColor=colors.HexColor("#333333"), leading=15, leftIndent=12, spaceAfter=4)
TERM_S   = S("term",   fontSize=10, textColor=TEAL,       fontName="Helvetica-Bold")
DEF_S    = S("def",    fontSize=10, textColor=GREY,       leading=14)
CAT_S    = S("cat",    fontSize=11, textColor=TEAL,       fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=4)

def doc_build(path):
    doc = SimpleDocTemplate(
        path,
        pagesize=landscape(A4),
        leftMargin=1.8*cm, rightMargin=1.8*cm,
        topMargin=2.2*cm, bottomMargin=1.8*cm,
        title="Script Soutenance Kenza FOUDALI"
    )

    story = []

    # ─── PAGE DE GARDE ───────────────────────────────────────────────────────
    def cover_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(TEAL)
        canvas.rect(0, 0, W, H, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#16705F"))
        canvas.rect(0, H*0.55, W, H*0.45, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 32)
        canvas.drawCentredString(W/2, H*0.6, "SCRIPT DE SOUTENANCE")
        canvas.setFont("Helvetica", 18)
        canvas.drawCentredString(W/2, H*0.52, "Inventaire Mobile CFC — Application Android")
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawCentredString(W/2, H*0.42, "Kenza FOUDALI — Stagiaire CF Consult Casablanca")
        canvas.setFont("Helvetica", 12)
        canvas.drawCentredString(W/2, H*0.34, "Script complet  |  Questions du jury  |  Abréviations & Glossaire")
        canvas.restoreState()

    # ─── HEADER/FOOTER ───────────────────────────────────────────────────────
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(TEAL)
        canvas.rect(0, H-1.5*cm, W, 1.5*cm, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawCentredString(W/2, H-1.0*cm, "SCRIPT DE SOUTENANCE — Inventaire Mobile CFC   |   Kenza FOUDALI")
        canvas.setFillColor(LGREY)
        canvas.rect(0, 0, W, 1.0*cm, fill=1, stroke=0)
        canvas.setFillColor(GREY)
        canvas.setFont("Helvetica", 8)
        canvas.drawCentredString(W/2, 0.35*cm, f"Page {doc.page}")
        canvas.restoreState()

    # ─── SECTION 1 : SCRIPT SLIDES ───────────────────────────────────────────
    story.append(Paragraph("PARTIE 1 — SCRIPT DES SLIDES", SECHEAD))
    story.append(Spacer(1, 0.3*cm))

    slides = [
        (1, "Titre / Introduction",
         "Bonjour, je suis Kenza FOUDALI, stagiaire au sein de CF Consult à Casablanca. "
         "Durant ce stage, j'ai eu l'opportunité de concevoir et développer une application mobile Android "
         "pour la gestion de l'inventaire physique de l'entreprise. C'est ce projet que je vais vous présenter aujourd'hui."),

        (2, "Présentation de l'organisme d'accueil",
         "CF Consult est un cabinet de conseil et d'expertise comptable basé à Casablanca. "
         "L'entreprise accompagne ses clients dans la gestion administrative, financière et organisationnelle. "
         "Elle doit tenir à jour un inventaire précis de son patrimoine matériel — ordinateurs, mobilier, "
         "matériel de bureau — et c'est justement là qu'est née l'idée de ce projet."),

        (3, "Contexte et besoin",
         "Avant ce projet, le suivi de l'inventaire se faisait manuellement, sur papier ou via des fichiers Excel. "
         "Cette méthode posait plusieurs limites : risques d'erreurs de saisie, pas de traçabilité en temps réel, "
         "et impossibilité d'accéder aux données depuis le terrain. "
         "L'objectif était de moderniser ce processus en passant à une solution mobile, rapide et fiable. "
         "Il ne s'agissait pas d'un problème bloquant, mais d'une vraie opportunité de digitalisation."),

        (4, "Objectifs du projet",
         "Trois objectifs principaux : "
         "(1) Centraliser toutes les données d'inventaire dans une base de données structurée. "
         "(2) Offrir une interface mobile intuitive pour saisir, modifier et consulter les équipements depuis le terrain. "
         "(3) Intégrer des fonctionnalités avancées : scan de codes-barres et reconnaissance IA."),

        (5, "Planification — Diagramme de Gantt",
         "Le projet s'est déroulé sur environ deux mois : analyse des besoins et cahier des charges, "
         "puis conception des diagrammes UML (cas d'utilisation, classes, séquences), "
         "développement du backend Spring Boot, puis de l'application Android, "
         "et enfin deux semaines de tests et corrections. "
         "Cette planification m'a permis de livrer un produit fonctionnel dans les délais."),

        (6, "Architecture globale — 3 tiers",
         "J'ai choisi une architecture trois tiers, standard pour les applications client-serveur :\n"
         "• Tier 1 — Présentation : l'application Android (Java natif) — affichage et interactions.\n"
         "• Tier 2 — Métier : le backend Spring Boot — logique applicative, sécurité JWT, API REST.\n"
         "• Tier 3 — Données : base de données PostgreSQL — stockage persistant.\n"
         "Cette séparation permet de réutiliser le même backend pour une future application web sans le modifier."),

        (7, "Backend Spring Boot",
         "Le backend suit les couches classiques de Spring Boot :\n"
         "Controllers REST → reçoivent les requêtes HTTP, retournent du JSON.\n"
         "Services → logique métier (validation, règles de gestion).\n"
         "Repositories → interface avec PostgreSQL via Spring Data JPA.\n"
         "Entités → classes Java mappées sur les tables BD avec annotations Hibernate.\n"
         "La sécurité : Spring Security + JWT. Le token encode rôle et identité, "
         "vérifié par un filtre à chaque requête sans interroger la BD (stateless)."),

        (8, "Application Android",
         "Développée en Java natif — contrôle total sur les performances et APIs Android. "
         "Architecture MVC : Activities (contrôleurs), Layouts XML (vues), Modèles (entités). "
         "Communication backend via Retrofit2 qui désérialise automatiquement le JSON via GSON. "
         "Session utilisateur en SharedPreferences : token JWT, rôle, nom sauvegardés localement."),

        (9, "Authentification JWT — flux complet",
         "1. Utilisateur saisit login/mot de passe → POST JSON vers /auth/login.\n"
         "2. Backend vérifie dans PostgreSQL (mdp haché BCrypt).\n"
         "3. Si OK → génère JWT signé (clé secrète) → renvoyé à l'app.\n"
         "4. App stocke le token en SharedPreferences.\n"
         "5. Chaque requête suivante : header Authorization: Bearer <token>.\n"
         "6. Filtre Spring Security décode et vérifie le token avant chaque contrôleur."),

        (10, "Scan de codes-barres — ZXing",
         "ZXing (Zebra Crossing) = référence open source pour codes-barres et QR codes sur Android. "
         "Intégration via IntentIntegrator : on lance l'Intent vers l'Activity ZXing, "
         "elle ouvre la caméra, détecte le code, renvoie le résultat via onActivityResult. "
         "Le numéro de série est ensuite utilisé pour rechercher l'équipement via Retrofit."),

        (11, "Reconnaissance IA — Google Gemini 2.5 Flash",
         "Fonctionnalité la plus avancée. Flux complet :\n"
         "1. Agent prend une photo → image encodée en Base64.\n"
         "2. Requête HTTP POST vers l'API Gemini (sans passer par notre backend).\n"
         "3. Prompt : répondre uniquement en JSON {designation, type, marque, etat, description}.\n"
         "4. App parse le JSON → pré-remplit le formulaire automatiquement.\n"
         "5. Agent vérifie et valide. Quelques secondes vs plusieurs minutes manuellement."),

        (12, "Fonctionnalités principales",
         "• Équipements informatiques : créer, consulter, rechercher, modifier, supprimer (désignation, marque, N° série, état, localisation, responsable).\n"
         "• Autres actifs (mobilier) : module séparé adapté.\n"
         "• Export Excel / PDF de l'inventaire complet.\n"
         "• Gestion des droits : utilisateur (créer/consulter) vs administrateur (supprimer/admin)."),

        (13, "Base de données PostgreSQL",
         "SGBD relationnel robuste et open source. Tables principales :\n"
         "• utilisateurs (login, password BCrypt, rôle, nom, prénom)\n"
         "• equipements (toutes caractéristiques matérielles)\n"
         "• autres_actifs (mobilier)\n"
         "Relations via clés étrangères. Hibernate génère le SQL automatiquement depuis les annotations Java. "
         "ddl-auto=update : schéma mis à jour au démarrage sans SQL manuel."),

        (14, "Technologies utilisées",
         "Backend : Java 17, Spring Boot 3, Spring Security, Spring Data JPA / Hibernate, PostgreSQL, Maven.\n"
         "Mobile : Android Java, Retrofit2, OkHttp, ZXing, Material Design 3.\n"
         "Outils : Android Studio, IntelliJ IDEA, Postman."),

        (15, "Démonstration — Résultats",
         "Application entièrement fonctionnelle : connexion → navigation → scan code-barres "
         "(retrouve l'équipement instantanément) → photo IA (identification automatique) "
         "→ validation → enregistrement. "
         "Quelques secondes au lieu de plusieurs minutes, sans risque d'erreur de saisie."),

        (16, "Conclusion & Perspectives d'évolution",
         "Solution full-stack complète : de la BD jusqu'à l'interface mobile, avec API REST sécurisée JWT, IA Gemini, scan ZXing.\n"
         "Perspectives d'évolution :\n"
         "1. Notifications push — Firebase Cloud Messaging pour alerter les responsables.\n"
         "2. Mode hors-ligne — Room Database (SQLite) + synchronisation différée.\n"
         "3. Migration Kotlin — syntaxe concise et coroutines pour l'asynchrone.\n"
         "4. Tests unitaires — JUnit (backend) et Espresso (UI Android)."),
    ]

    for num, title, text in slides:
        story.append(Paragraph(f"SLIDE {num}", SLNUM_S))
        story.append(Paragraph(title, SLTIT_S))
        story.append(HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=4))
        for line in text.split('\n'):
            line = line.strip()
            if line:
                story.append(Paragraph(line, BODY_S))
        story.append(Spacer(1, 0.4*cm))

    # ─── SECTION 2 : QUESTIONS / RÉPONSES ────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("PARTIE 2 — QUESTIONS DU JURY & RÉPONSES", SECHEAD))
    story.append(Spacer(1, 0.3*cm))

    categories = [
        ("ARCHITECTURE", [
            ("Pourquoi une architecture 3 tiers plutôt que 2 tiers ?",
             "Une architecture 2 tiers — Android connecté directement à PostgreSQL — exposerait les credentials de la BD dans l'APK, extractibles par décompilation. "
             "Avec 3 tiers, seul le backend accède à la BD. La logique métier est centralisée : une modification backend s'applique à tous les clients sans re-déployer l'app."),

            ("Pourquoi Spring Boot pour le backend ?",
             "Auto-configuration (peu de boilerplate), Spring Security complet pour l'authentification, "
             "Spring Data JPA pour l'ORM, Tomcat embarqué sans serveur externe. Standard industriel très utilisé en entreprise."),

            ("Pourquoi PostgreSQL plutôt que MySQL ou SQLite ?",
             "SQLite = fichier local, non adapté au multi-utilisateurs. PostgreSQL gère mieux les transactions concurrentes que MySQL "
             "— important quand plusieurs agents modifient l'inventaire simultanément. Meilleure conformité aux standards SQL."),
        ]),
        ("SECURITE & AUTHENTIFICATION", [
            ("Expliquez précisément comment fonctionne JWT.",
             "JWT (JSON Web Token) = 3 parties en Base64 séparées par des points : "
             "(1) Header : algorithme de signature (HS256). "
             "(2) Payload : claims — userId, role, date d'expiration. "
             "(3) Signature : calculée avec une clé secrète côté serveur. "
             "À chaque requête, le backend recalcule la signature et compare. C'est stateless : pas de session stockée côté serveur."),

            ("Comment les mots de passe sont-ils stockés ?",
             "Jamais en clair. BCrypt = algorithme de hachage adaptatif avec salt aléatoire par mot de passe. "
             "Deux utilisateurs avec le même mot de passe auront des hashes différents. "
             "Le facteur de coût peut être augmenté pour résister au brute force. Spring Security gère via BCryptPasswordEncoder."),

            ("Que se passe-t-il si le token JWT expire ?",
             "Erreur 401 Unauthorized → l'app redirige vers l'écran de connexion. "
             "Amélioration possible : refresh token (longue durée) permettant de renouveler le token d'accès sans redemander les credentials."),
        ]),
        ("IA GEMINI", [
            ("Comment fonctionne l'intégration de Gemini techniquement ?",
             "Image lue via ContentResolver.openInputStream() → encodée en Base64. "
             "JSON construit avec tableau 'contents' > 'parts' : prompt texte + image inline (type MIME + data Base64). "
             "POST via OkHttp vers l'API Gemini. Réponse JSON parsée → extraction du texte du premier candidat → "
             "parsé à son tour en JSON pour récupérer désignation, type, marque, état, description."),

            ("Pourquoi Gemini 2.5 Flash et pas ChatGPT ?",
             "Multimodal natif (conçu images + texte dès le départ), très rapide (suffixe Flash), "
             "quota gratuit suffisant pour une démo, et s'intègre via HTTP standard sans SDK obligatoire."),

            ("Quels risques liés à la clé API dans l'app Android ?",
             "L'APK peut être décompilé, exposant la clé. En production : faire passer les appels Gemini par notre backend "
             "qui détient la clé en variable d'environnement, et exposer un endpoint /ai/analyze. La clé n'est jamais côté client."),
        ]),
        ("ANDROID & TECHNIQUE", [
            ("Pourquoi Java Android natif et pas Flutter ou React Native ?",
             "Accès direct à toutes les APIs Android sans couche d'abstraction — plus fiable pour caméra, FileProvider, permissions. "
             "C'est aussi le langage maîtrisé en cours."),

            ("Comment fonctionne le scan de codes-barres techniquement ?",
             "ZXing analyse les frames vidéo en continu, détecte les patterns (barres verticales pour code 1D, carrés pour QR). "
             "L'algorithme Reed-Solomon corrige les erreurs de lecture et extrait la chaîne encodée. "
             "IntentIntegrator délègue tout ce traitement à l'Activity ZXing."),

            ("Différence entre Retrofit et OkHttp dans votre code ?",
             "OkHttp = couche HTTP bas niveau (connexions TCP, timeouts, intercepteurs). "
             "Retrofit = abstraction au-dessus transformant des interfaces Java annotées en appels HTTP. "
             "J'utilise Retrofit pour mon backend (plus propre et maintenable), "
             "OkHttp direct pour Gemini car le JSON multimodal doit être construit manuellement."),

            ("Comment gérez-vous les erreurs réseau ?",
             "Callbacks Retrofit : onFailure (réseau/timeout) et onResponse (HTTP reçu). "
             "Je vérifie response.isSuccessful() pour distinguer succès et erreurs HTTP, "
             "et affiche des Toasts appropriés. En mode démo (admin/admin), l'app fonctionne hors ligne."),

            ("Perspectives d'évolution ?",
             "1. Notifications push via Firebase Cloud Messaging pour alerter les responsables.\n"
             "2. Mode hors-ligne complet avec Room Database et synchronisation différée.\n"
             "3. Migration vers Kotlin — syntaxe concise et coroutines pour l'asynchrone.\n"
             "4. Tests unitaires avec JUnit (backend) et Espresso (UI Android)."),
        ]),
    ]

    for cat, qas in categories:
        story.append(Paragraph(cat, CAT_S))
        story.append(HRFlowable(width="100%", thickness=0.5, color=TEAL, spaceAfter=4))
        for q, a in qas:
            story.append(Paragraph(f"Q : {q}", Q_S))
            for line in a.split('\n'):
                line = line.strip()
                if line:
                    story.append(Paragraph(line, A_S))
            story.append(Spacer(1, 0.2*cm))
        story.append(Spacer(1, 0.3*cm))

    # ─── SECTION 3 : ABREVIATIONS ────────────────────────────────────────────
    story.append(PageBreak())
    story.append(Paragraph("PARTIE 3 — ABREVIATIONS & GLOSSAIRE", SECHEAD))
    story.append(Spacer(1, 0.3*cm))

    abbrevs = [
        ("JWT",           "JSON Web Token — jeton d'authentification signé encodé en Base64, stateless, sécurise les API REST."),
        ("API",           "Application Programming Interface — interface de communication entre logiciels via requêtes HTTP JSON."),
        ("REST",          "Representational State Transfer — style d'architecture pour API web basé sur HTTP (GET, POST, PUT, DELETE)."),
        ("HTTP/HTTPS",    "Protocole de communication web. HTTPS = version chiffrée via SSL/TLS."),
        ("JSON",          "JavaScript Object Notation — format léger d'échange de données textuelles : {\"cle\":\"valeur\"}."),
        ("MVC",           "Modèle-Vue-Contrôleur — pattern séparant logique (Modèle), affichage (Vue) et contrôle (Contrôleur)."),
        ("ORM",           "Object-Relational Mapping — fait correspondre classes Java et tables SQL automatiquement (ex: Hibernate)."),
        ("JPA",           "Java Persistence API — spécification Java pour la persistance relationnelle. Impl: Spring Data JPA/Hibernate."),
        ("APK",           "Android Package Kit — fichier d'installation Android, peut être décompilé (d'où le risque clé API)."),
        ("SDK",           "Software Development Kit — ensemble d'outils pour développer sur une plateforme donnée."),
        ("UI",            "User Interface — interface utilisateur, ce que l'utilisateur voit et avec quoi il interagit."),
        ("UML",           "Unified Modeling Language — langage de modélisation (diagrammes classes, séquences, cas d'utilisation...)."),
        ("SGBD",          "Système de Gestion de Bases de Données — logiciel gérant stockage et accès aux données (PostgreSQL...)."),
        ("SQL",           "Structured Query Language — langage de requête pour bases de données relationnelles."),
        ("BCrypt",        "Algorithme de hachage de mots de passe avec salt aléatoire, résistant aux attaques brute force."),
        ("Base64",        "Encodage transformant des données binaires (image) en texte transportable en JSON."),
        ("OkHttp",        "Bibliothèque HTTP bas niveau pour Android/Java — gère connexions TCP, timeouts. Utilisée par Retrofit."),
        ("Retrofit2",     "Bibliothèque Android transformant des interfaces Java annotées en appels HTTP (couche au-dessus d'OkHttp)."),
        ("GSON",          "Bibliothèque Google convertissant automatiquement objets Java ↔ JSON."),
        ("ZXing",         "Zebra Crossing — bibliothèque open source de lecture codes-barres et QR codes sur Android."),
        ("Room",          "Bibliothèque Android (SQLite) pour persistance locale avec synchronisation possible."),
        ("FCM",           "Firebase Cloud Messaging — service Google d'envoi de notifications push vers mobiles."),
        ("JUnit",         "Framework de tests unitaires Java — vérifie le bon fonctionnement des méthodes backend."),
        ("Espresso",      "Framework de tests UI Android — simule les interactions de l'utilisateur sur l'interface."),
        ("Gemini",        "Modèle d'IA multimodal de Google (texte + image). 2.5 Flash = version rapide, gratuite, via API HTTP."),
        ("Spring Boot",   "Framework Java pour créer des applications web et API REST avec configuration automatique."),
        ("Hibernate",     "Implémentation de JPA — génère automatiquement les requêtes SQL depuis les annotations Java."),
        ("Maven",         "Outil de gestion des dépendances et de build pour projets Java (fichier pom.xml)."),
        ("Postman",       "Outil graphique pour tester manuellement les endpoints d'une API REST."),
        ("Material Design 3", "Système de design Google pour Android — composants UI modernes (boutons, cartes, champs...)."),
        ("FileProvider",  "Mécanisme Android sécurisé pour partager des fichiers entre applications (ex: photo → caméra)."),
        ("SharedPreferences", "Stockage clé-valeur persistant et léger sur Android — utilisé pour la session utilisateur."),
        ("Intent",        "Objet Android représentant une action (ouvrir une Activity, lancer la caméra...)."),
        ("Activity",      "Composant Android représentant un écran de l'application avec son cycle de vie."),
        ("3 tiers",       "Architecture logicielle : Présentation (Android) → Métier (Spring Boot) → Données (PostgreSQL)."),
        ("Stateless",     "Sans état : le serveur ne stocke pas de session. JWT est stateless — token vérifié à chaque requête."),
        ("Salt (BCrypt)", "Valeur aléatoire ajoutée au mot de passe avant hachage, rendant chaque hash unique."),
        ("Reed-Solomon",  "Algorithme de correction d'erreurs utilisé par ZXing pour décoder les codes-barres même partiellement lisibles."),
    ]

    # Tableau 2 colonnes
    data = [["Terme", "Définition"]]
    for term, defn in abbrevs:
        data.append([
            Paragraph(term, TERM_S),
            Paragraph(defn, DEF_S)
        ])

    tbl = Table(data, colWidths=[4*cm, 22*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), TEAL),
        ("TEXTCOLOR",   (0,0), (-1,0), WHITE),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,0), 11),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGREY]),
        ("VALIGN",      (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING",(0,0), (-1,-1), 6),
        ("TOPPADDING",  (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0),(-1,-1), 4),
        ("LINEBELOW",   (0,0), (-1,0), 1, TEAL),
        ("GRID",        (0,0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
    ]))
    story.append(tbl)

    doc.build(story, onFirstPage=cover_page, onLaterPages=on_page)
    print("PDF généré :", path)

doc_build("/home/user/inventaire-android/script_soutenance_kenza.pdf")
