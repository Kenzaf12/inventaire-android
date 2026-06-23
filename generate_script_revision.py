from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

W, H = landscape(A4)
# Palette pastel
ACCENT = colors.HexColor("#A78BFA")   # lavande pastel
ACCENT2= colors.HexColor("#7C6FD4")   # lavande un peu plus soutenu (titres)
SOFT   = colors.HexColor("#F3EFFF")   # fond pastel tres clair
DARK   = colors.HexColor("#4B4453")   # texte titre doux
GREY   = colors.HexColor("#3A3A3A")   # corps de texte lisible

styles = getSampleStyleSheet()
def S(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

SLNUM = S("slnum", fontSize=12, textColor=ACCENT2, fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=1)
SLTIT = S("sltit", fontSize=16, textColor=DARK,    fontName="Helvetica-Bold", spaceBefore=1, spaceAfter=6)
BODY  = S("body",  fontSize=13, textColor=GREY,    leading=20, spaceAfter=7, firstLineIndent=8)

doc = SimpleDocTemplate(
    "/home/user/inventaire-android/script_revision.pdf",
    pagesize=landscape(A4),
    leftMargin=1.8*cm, rightMargin=1.8*cm, topMargin=1.2*cm, bottomMargin=1.3*cm,
    title="Script de revision - Kenza FOUDALI"
)
story = []

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#9A9A9A")); canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(W/2, 0.5*cm, f"Page {doc.page}")
    canvas.restoreState()

slides = [
 (1, "Page de titre",
  ["Bonjour, je suis Kenza FOUDALI, stagiaire au sein de CF Consult a Casablanca. Durant ce stage, j'ai eu l'opportunite de concevoir et developper une application mobile Android pour la gestion de l'inventaire physique de l'entreprise. C'est ce projet que je vais vous presenter aujourd'hui."]),
 (2, "Presentation de l'organisme d'accueil",
  ["CF Consult est un cabinet de conseil et d'expertise comptable base a Casablanca. L'entreprise accompagne ses clients dans la gestion administrative, financiere et organisationnelle. Comme toute structure serieuse, elle doit tenir a jour un inventaire precis de son patrimoine materiel — ordinateurs, mobilier, materiel de bureau — et c'est justement la qu'est nee l'idee de ce projet."]),
 (3, "Contexte et besoin",
  ["Avant ce projet, le suivi de l'inventaire se faisait manuellement, sur papier ou via des fichiers Excel. Cette methode posait plusieurs limites : risques d'erreurs de saisie, pas de tracabilite en temps reel, et impossibilite d'acceder aux donnees depuis le terrain. L'objectif etait donc de moderniser ce processus en passant a une solution mobile, rapide et fiable. Il ne s'agissait pas d'un probleme bloquant, mais d'une vraie opportunite de digitalisation."]),
 (4, "Objectifs du projet",
  ["Le projet avait trois objectifs principaux. Premierement, centraliser toutes les donnees d'inventaire dans une base de donnees structuree. Deuxiemement, offrir une interface mobile intuitive permettant aux agents de terrain de saisir, modifier et consulter les equipements directement depuis leur telephone. Troisiemement, integrer des fonctionnalites avancees comme le scan de codes-barres et la reconnaissance d'equipements par intelligence artificielle."]),
 (5, "Planification (Gantt)",
  ["Le projet s'est deroule sur environ deux mois. La premiere semaine etait dediee a l'analyse des besoins et a la redaction du cahier des charges. Ensuite j'ai concu les diagrammes UML — cas d'utilisation, diagramme de classes, sequences. La phase de developpement a occupe la majorite du stage : backend Spring Boot, puis application Android. Les deux dernieres semaines ont servi aux tests et aux corrections. Cette planification m'a permis de livrer un produit fonctionnel dans les delais."]),
 (6, "Architecture globale (3 tiers)",
  ["L'architecture que j'ai choisie est une architecture trois tiers, qui est le standard pour les applications client-serveur modernes.",
   "Le premier tier est la couche presentation : c'est l'application Android, developpee en Java natif. Elle s'occupe uniquement de l'affichage et des interactions utilisateur.",
   "Le deuxieme tier est la couche metier : c'est le backend Spring Boot, qui tourne sur le serveur. Il contient toute la logique applicative — les regles de gestion, la securite, l'authentification JWT, et l'exposition des API REST.",
   "Le troisieme tier est la couche donnees : une base de donnees PostgreSQL qui stocke de facon persistante tous les equipements, utilisateurs et mouvements.",
   "Cette separation est fondamentale : si demain on veut creer une application web en plus de l'application Android, on reutilise exactement le meme backend sans y toucher."]),
 (7, "Backend Spring Boot",
  ["Le backend est structure selon les couches classiques de Spring Boot. On a les Controllers REST qui recoivent les requetes HTTP et retournent des reponses JSON. En dessous, les Services qui contiennent la logique metier — par exemple, verifier qu'un equipement n'est pas en doublon avant de l'enregistrer. Ensuite les Repositories qui font l'interface avec la base de donnees via Spring Data JPA. Et enfin les Entites qui sont les classes Java mappees directement sur les tables PostgreSQL grace aux annotations Hibernate comme @Entity, @Table, @Column.",
   "La securite est geree par Spring Security avec JWT — JSON Web Token. Quand l'utilisateur se connecte, le backend genere un token signe qui encode son role et son identite. Ce token est ensuite envoye dans chaque requete dans le header HTTP Authorization: Bearer <token>. Le backend le verifie a chaque appel sans avoir besoin d'interroger la base de donnees, ce qui est tres efficace."]),
 (8, "Application Android",
  ["L'application Android est developpee en Java natif, sans framework tiers comme Flutter ou React Native. J'ai fait ce choix pour avoir un controle total sur les performances et l'acces aux APIs Android.",
   "L'architecture cote Android suit le pattern MVC — Modele Vue Controleur. Les Activities jouent le role de controleurs, les layouts XML sont les vues, et les modeles de donnees representent les entites metier.",
   "Pour communiquer avec le backend, j'utilise Retrofit2, une librairie qui transforme automatiquement les appels API en requetes HTTP et deserialise les reponses JSON en objets Java grace a GSON.",
   "La session utilisateur est geree via SharedPreferences — un stockage cle-valeur local sur le telephone — ou je sauvegarde le token JWT, le role et le nom de l'utilisateur apres connexion."]),
 (9, "Authentification JWT (flux complet)",
  ["Laissez-moi vous expliquer precisement le flux d'authentification. L'utilisateur saisit son login et son mot de passe dans l'application. L'app envoie ces credentials en POST JSON vers l'endpoint /auth/login du backend. Le backend verifie les credentials dans PostgreSQL — le mot de passe est hache en BCrypt pour la securite. Si c'est correct, il genere un JWT signe avec une cle secrete, et le renvoie a l'application. L'application stocke ce token en SharedPreferences. A partir de la, chaque requete suivante inclut ce token dans le header HTTP. Le backend decode et verifie le token a chaque appel grace a un filtre Spring Security qui s'execute avant chaque controleur."]),
 (10, "Scan de codes-barres (ZXing)",
  ["Pour le scan de codes-barres, j'utilise la librairie ZXing — Zebra Crossing — qui est la reference open source pour la lecture de codes-barres et QR codes sur Android. L'integration se fait via IntentIntegrator : on lance une Intent vers l'activite de scan ZXing, elle ouvre la camera, detecte le code, et renvoie le resultat a notre Activity via onActivityResult. Ce numero de serie ou code d'inventaire est ensuite utilise pour rechercher l'equipement correspondant dans la base de donnees via un appel Retrofit vers le backend."]),
 (11, "IA Gemini (reconnaissance d'equipements)",
  ["La fonctionnalite la plus avancee de cette application est la reconnaissance d'equipements par intelligence artificielle. J'ai integre l'API Google Gemini 2.5 Flash — le modele multimodal de Google.",
   "Le flux fonctionne ainsi : l'agent prend une photo d'un equipement avec son telephone, ou en selectionne une depuis la galerie. L'application encode l'image en Base64 et envoie une requete HTTP directement a l'API Gemini — sans passer par notre backend, ce qui simplifie l'architecture. Le prompt que j'envoie a Gemini lui demande d'identifier l'objet et de repondre uniquement en JSON avec les champs : designation, type, marque, etat et description.",
   "Gemini analyse l'image et retourne ces informations. L'application parse le JSON et pre-remplit automatiquement le formulaire d'ajout d'equipement. L'agent n'a plus qu'a verifier et valider. Cette fonctionnalite reduit considerablement le temps de saisie."]),
 (12, "Fonctionnalites principales",
  ["L'application couvre tout le cycle de vie d'un inventaire. Pour les equipements informatiques, on peut creer une fiche avec designation, marque, numero de serie, etat, localisation et responsable. Pour les autres actifs — mobilier, materiel divers — il y a un module separe adapte. On peut consulter la liste, rechercher par mot-cle, modifier une fiche, et la supprimer.",
   "Il y a aussi un module d'export : on peut generer un fichier Excel ou PDF de l'inventaire complet depuis l'application.",
   "La gestion des droits est implementee : un utilisateur simple peut consulter et creer, mais seul un administrateur peut supprimer ou acceder au module d'administration des comptes utilisateurs."]),
 (13, "Base de donnees PostgreSQL",
  ["La base de donnees est PostgreSQL, un SGBD relationnel robuste et open source. Le schema comporte plusieurs tables principales : utilisateurs avec les colonnes login, password hashe, role, nom, prenom ; equipements avec toutes les caracteristiques materielles ; autres_actifs pour le mobilier. Les relations sont modelisees avec des cles etrangeres — par exemple un equipement peut etre lie a un responsable dans la table utilisateurs.",
   "Grace a Spring Data JPA et Hibernate, je n'ecris quasiment pas de SQL a la main. Hibernate genere les requetes automatiquement a partir des annotations sur mes classes Java. Et au demarrage de l'application Spring Boot, avec spring.jpa.hibernate.ddl-auto=update, le schema se met a jour automatiquement si je modifie mes entites."]),
 (14, "Technologies utilisees",
  ["Pour resumer la stack technique : cote backend, Java 17 avec Spring Boot 3, Spring Security pour l'authentification, Spring Data JPA / Hibernate pour l'ORM, PostgreSQL comme base de donnees, et Maven pour la gestion des dependances. Cote mobile, Android Java avec Retrofit2 pour les appels API, OkHttp pour les requetes directes vers Gemini, ZXing pour le scan, et Material Design 3 pour l'interface. Pour le developpement j'ai utilise Android Studio, IntelliJ IDEA, et Postman pour tester les endpoints REST."]),
 (15, "Demonstration / Resultats",
  ["Concretement, l'application est entierement fonctionnelle. On peut se connecter, naviguer dans l'inventaire, scanner un code-barres pour retrouver un equipement instantanement, prendre une photo et laisser l'IA l'identifier automatiquement, puis valider et enregistrer. Le tout en quelques secondes, la ou la saisie manuelle prenait plusieurs minutes et comportait des risques d'erreurs."]),
 (16, "Conclusion et perspectives d'evolution",
  ["Ce stage m'a permis de travailler sur une solution full-stack complete, de la conception de la base de donnees jusqu'a l'interface mobile, en passant par la mise en place d'une API REST securisee. J'ai eu l'occasion d'appliquer des technologies modernes comme JWT, l'IA generative avec Gemini, et le scan de codes-barres.",
   "Plusieurs perspectives d'evolution sont envisageables. Premierement, implementer des notifications push via Firebase Cloud Messaging pour alerter les responsables lors d'ajouts ou de modifications. Deuxiemement, ajouter un mode hors ligne complet avec Room Database — la base de donnees SQLite Android — et une synchronisation differee quand le reseau revient. Troisiemement, migrer vers Kotlin, le langage moderne recommande par Google pour Android, qui offre une syntaxe plus concise et une meilleure gestion des coroutines pour l'asynchrone. Quatriemement, ajouter des tests unitaires avec JUnit pour le backend et Espresso pour l'UI Android.",
   "C'est un projet concret qui a une vraie valeur ajoutee pour l'entreprise. Je suis disponible pour vos questions."]),
]

for num, title, paras in slides:
    story.append(Paragraph(f"SLIDE {num}", SLNUM))
    story.append(Paragraph(title, SLTIT))
    story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=6))
    for p in paras:
        story.append(Paragraph(p, BODY))
    story.append(Spacer(1, 0.4*cm))

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("PDF genere : script_revision.pdf")
