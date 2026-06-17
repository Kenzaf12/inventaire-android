"""
Serveur mock pour tester l'app Inventaire CFC sans connexion au réseau de l'entreprise.

INSTALLATION (une seule fois) :
    pip install flask flask-cors

LANCER :
    python mock_server.py

L'app Android doit pointer vers 10.0.2.2:8080 (émulateur) ou <ton-IP-local>:8080 (vrai téléphone).
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import time

app = Flask(__name__)
CORS(app)

# ---------------------------------------------------------------------------
# Données de démo
# ---------------------------------------------------------------------------

EQUIPEMENTS = [
    {"id": 1, "refImmo": "IMM-001", "cab": "CAB001", "station": "Casablanca", "article": "ART-001",
     "equipement": "Ordinateur Portable", "designation": "Dell Latitude 5520", "modele": "5520",
     "marque": "Dell", "nserie": "SN123456", "qte": 1.0, "etat": "En activité", "valide": "OUI",
     "descTech": "Intel Core i7, 16GB RAM, 512GB SSD", "observation": "RAS",
     "dateInvent": "2025-06-01", "heureInvent": "09:00:00", "agent": "Ahmed Benali", "photo": None},
    {"id": 2, "refImmo": "IMM-002", "cab": "CAB002", "station": "Casablanca", "article": "ART-002",
     "equipement": "Imprimante", "designation": "HP LaserJet Pro M404dn", "modele": "M404dn",
     "marque": "HP", "nserie": "SN654321", "qte": 1.0, "etat": "En activité", "valide": "OUI",
     "descTech": "Laser monochrome, 38ppm", "observation": "",
     "dateInvent": "2025-06-01", "heureInvent": "09:30:00", "agent": "Ahmed Benali", "photo": None},
    {"id": 3, "refImmo": "IMM-003", "cab": "CAB003", "station": "Rabat", "article": "ART-003",
     "equipement": "Écran", "designation": "LG 27UL500 4K", "modele": "27UL500",
     "marque": "LG", "nserie": "SN789012", "qte": 2.0, "etat": "En activité", "valide": "OUI",
     "descTech": "27 pouces, 4K UHD, IPS", "observation": "",
     "dateInvent": "2025-06-02", "heureInvent": "10:00:00", "agent": "Fatima Zahra", "photo": None},
    {"id": 4, "refImmo": "IMM-004", "cab": "CAB004", "station": "Casablanca", "article": "ART-004",
     "equipement": "Serveur", "designation": "Dell PowerEdge R740", "modele": "R740",
     "marque": "Dell", "nserie": "SN345678", "qte": 1.0, "etat": "Hors service", "valide": "NON",
     "descTech": "2x Xeon Gold, 128GB RAM, 4TB", "observation": "En panne depuis mars 2025",
     "dateInvent": "2025-06-03", "heureInvent": "11:00:00", "agent": "Ahmed Benali", "photo": None},
    {"id": 5, "refImmo": "IMM-005", "cab": "CAB005", "station": "Rabat", "article": "ART-005",
     "equipement": "Switch réseau", "designation": "Cisco Catalyst 2960", "modele": "2960",
     "marque": "Cisco", "nserie": "SN901234", "qte": 1.0, "etat": "En activité", "valide": "OUI",
     "descTech": "24 ports Gigabit", "observation": "",
     "dateInvent": "2025-06-04", "heureInvent": "14:00:00", "agent": "Fatima Zahra", "photo": None},
]

AUTRES = [
    {"id": 1, "cab": "CAB-A001", "nlocal": "Bureau 101", "designation": "Chaise de bureau",
     "marque": "Steelcase", "qte": 5.0, "etat": "En activité", "valide": "OUI",
     "observation": "", "dateInvent": "2025-06-01", "heureInvent": "09:00:00", "agent": "Ahmed Benali"},
    {"id": 2, "cab": "CAB-A002", "nlocal": "Bureau 101", "designation": "Table de réunion",
     "marque": "Ikea", "qte": 1.0, "etat": "En activité", "valide": "OUI",
     "observation": "", "dateInvent": "2025-06-01", "heureInvent": "10:00:00", "agent": "Ahmed Benali"},
    {"id": 3, "cab": "CAB-A003", "nlocal": "Salle serveur", "designation": "Armoire réseau",
     "marque": "APC", "qte": 2.0, "etat": "En activité", "valide": "OUI",
     "observation": "19 pouces, 42U", "dateInvent": "2025-06-02", "heureInvent": "11:00:00", "agent": "Fatima Zahra"},
]

AGENTS = [
    {"id": 1, "nom": "Benali", "prenom": "Ahmed", "login": "ahmed.benali", "role": "ADMIN"},
    {"id": 2, "nom": "Zahra", "prenom": "Fatima", "login": "fatima.zahra", "role": "AGENT"},
    {"id": 3, "nom": "Karim", "prenom": "Youssef", "login": "youssef.karim", "role": "AGENT"},
]

ACTIVITES = [
    {"id": 1, "agentId": 1, "action": "LOGIN",  "detail": "Connexion au système",              "dateHeure": "2025-06-17T08:55:00"},
    {"id": 2, "agentId": 1, "action": "CREATE", "detail": "Création équipement CAB001",         "dateHeure": "2025-06-17T09:05:00"},
    {"id": 3, "agentId": 1, "action": "CREATE", "detail": "Création équipement CAB002",         "dateHeure": "2025-06-17T09:20:00"},
    {"id": 4, "agentId": 1, "action": "UPDATE", "detail": "Modification équipement CAB001",     "dateHeure": "2025-06-17T09:45:00"},
    {"id": 5, "agentId": 1, "action": "CREATE", "detail": "Création équipement CAB004",         "dateHeure": "2025-06-17T10:10:00"},
    {"id": 6, "agentId": 2, "action": "LOGIN",  "detail": "Connexion au système",              "dateHeure": "2025-06-17T10:00:00"},
    {"id": 7, "agentId": 2, "action": "CREATE", "detail": "Création équipement CAB003",         "dateHeure": "2025-06-17T10:15:00"},
    {"id": 8, "agentId": 2, "action": "UPDATE", "detail": "Modification équipement CAB003",     "dateHeure": "2025-06-17T10:30:00"},
    {"id": 9, "agentId": 2, "action": "CREATE", "detail": "Création équipement CAB005",         "dateHeure": "2025-06-17T11:00:00"},
    {"id":10, "agentId": 3, "action": "LOGIN",  "detail": "Connexion au système",              "dateHeure": "2025-06-17T14:00:00"},
    {"id":11, "agentId": 3, "action": "CREATE", "detail": "Création autre CAB-A001",            "dateHeure": "2025-06-17T14:10:00"},
    {"id":12, "agentId": 3, "action": "CREATE", "detail": "Création autre CAB-A002",            "dateHeure": "2025-06-17T14:25:00"},
]

LOCALISATIONS = [
    {"id": 1, "site": "Casablanca", "batiment": "Bâtiment A", "etage": "RDC"},
    {"id": 2, "site": "Rabat", "batiment": "Siège", "etage": "1er"},
]

next_id = {"equip": 6, "autres": 4, "agent": 4, "local": 3}

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json or {}
    login_val = data.get("login", "")
    password = data.get("password", "")
    # Accepte n'importe quel login/mdp pour la démo
    agent = next((a for a in AGENTS if a["login"] == login_val), AGENTS[0])
    return jsonify({
        "token": "demo-token-1234567890",
        "role": agent["role"],
        "nom": agent["nom"],
        "prenom": agent["prenom"],
        "agentId": agent["id"]
    })

# ---------------------------------------------------------------------------
# Equipements
# ---------------------------------------------------------------------------

@app.route("/api/equipements", methods=["GET"])
def get_equipements():
    return jsonify(EQUIPEMENTS)

@app.route("/api/equipements/cab/<cab>", methods=["GET"])
def get_equipement_by_cab(cab):
    item = next((e for e in EQUIPEMENTS if e["cab"] == cab), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Non trouvé"}), 404

@app.route("/api/equipements/station/<station>", methods=["GET"])
def get_equipements_by_station(station):
    return jsonify([e for e in EQUIPEMENTS if e["station"].lower() == station.lower()])

@app.route("/api/equipements", methods=["POST"])
def create_equipement():
    data = request.json or {}
    data["id"] = next_id["equip"]
    next_id["equip"] += 1
    EQUIPEMENTS.append(data)
    return jsonify(data), 201

@app.route("/api/equipements/<int:item_id>", methods=["PUT"])
def update_equipement(item_id):
    data = request.json or {}
    for i, e in enumerate(EQUIPEMENTS):
        if e["id"] == item_id:
            data["id"] = item_id
            EQUIPEMENTS[i] = data
            return jsonify(data)
    return jsonify({"error": "Non trouvé"}), 404

@app.route("/api/equipements/<int:item_id>", methods=["DELETE"])
def delete_equipement(item_id):
    global EQUIPEMENTS
    EQUIPEMENTS = [e for e in EQUIPEMENTS if e["id"] != item_id]
    return "", 204

# ---------------------------------------------------------------------------
# Autres
# ---------------------------------------------------------------------------

@app.route("/api/autres", methods=["GET"])
def get_autres():
    return jsonify(AUTRES)

@app.route("/api/autres/cab/<cab>", methods=["GET"])
def get_autres_by_cab(cab):
    item = next((a for a in AUTRES if a["cab"] == cab), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Non trouvé"}), 404

@app.route("/api/autres/local/<nlocal>", methods=["GET"])
def get_autres_by_local(nlocal):
    return jsonify([a for a in AUTRES if a["nlocal"].lower() == nlocal.lower()])

@app.route("/api/autres", methods=["POST"])
def create_autres():
    data = request.json or {}
    data["id"] = next_id["autres"]
    next_id["autres"] += 1
    AUTRES.append(data)
    return jsonify(data), 201

@app.route("/api/autres/<int:item_id>", methods=["PUT"])
def update_autres(item_id):
    data = request.json or {}
    for i, a in enumerate(AUTRES):
        if a["id"] == item_id:
            data["id"] = item_id
            AUTRES[i] = data
            return jsonify(data)
    return jsonify({"error": "Non trouvé"}), 404

@app.route("/api/autres/<int:item_id>", methods=["DELETE"])
def delete_autres(item_id):
    global AUTRES
    AUTRES = [a for a in AUTRES if a["id"] != item_id]
    return "", 204

# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

@app.route("/api/search/equipements", methods=["GET"])
def search_equipements():
    q = (request.args.get("q") or "").lower()
    results = [e for e in EQUIPEMENTS if q in str(e).lower()] if q else EQUIPEMENTS
    return jsonify(results)

@app.route("/api/search/autres", methods=["GET"])
def search_autres():
    q = (request.args.get("q") or "").lower()
    results = [a for a in AUTRES if q in str(a).lower()] if q else AUTRES
    return jsonify(results)

@app.route("/api/search/equipements/non-inventories", methods=["GET"])
def non_inventories_equip():
    return jsonify([e for e in EQUIPEMENTS if e["valide"] == "NON"])

@app.route("/api/search/autres/non-inventories", methods=["GET"])
def non_inventories_autres():
    return jsonify([a for a in AUTRES if a.get("valide") == "NON"])

# ---------------------------------------------------------------------------
# Photos
# ---------------------------------------------------------------------------

@app.route("/api/photos/upload", methods=["POST"])
def upload_photo():
    return jsonify({"url": "demo_photo.jpg", "message": "Photo uploadée (démo)"})

@app.route("/api/photos/<filename>", methods=["GET"])
def get_photo(filename):
    # Retourne une image PNG grise de 1x1 pixel
    pixel = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D,
        0x49, 0x48, 0x44, 0x52, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53, 0xDE, 0x00, 0x00, 0x00,
        0x0C, 0x49, 0x44, 0x41, 0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
        0x00, 0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC, 0x33, 0x00, 0x00, 0x00,
        0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82
    ])
    return send_file(io.BytesIO(pixel), mimetype="image/png")

@app.route("/api/photos/<filename>", methods=["DELETE"])
def delete_photo(filename):
    return jsonify({"success": True})

# ---------------------------------------------------------------------------
# QR Code
# ---------------------------------------------------------------------------

@app.route("/api/qrcode/equipement/<int:item_id>", methods=["GET"])
def qr_equipement(item_id):
    # Retourne un PNG 1x1 pixel (démo)
    pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82'
    return send_file(io.BytesIO(pixel), mimetype="image/png")

@app.route("/api/qrcode/autres/<int:item_id>", methods=["GET"])
def qr_autres(item_id):
    pixel = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82'
    return send_file(io.BytesIO(pixel), mimetype="image/png")

# ---------------------------------------------------------------------------
# Export Excel / PDF
# ---------------------------------------------------------------------------

def make_dummy_xlsx():
    # Fichier XLSX minimal valide (en-têtes seulement)
    # (vrai fichier ZIP/XML — suffisant pour déclencher le download)
    import zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml",
            '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '</Types>')
        zf.writestr("_rels/.rels",
            '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>')
        zf.writestr("xl/workbook.xml",
            '<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheets><sheet name="Inventaire" sheetId="1" r:id="rId1" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
            '</sheets></workbook>')
    buf.seek(0)
    return buf

@app.route("/api/export/equipements", methods=["GET"])
def export_equipements():
    return send_file(make_dummy_xlsx(),
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     download_name="equipements.xlsx")

@app.route("/api/export/autres", methods=["GET"])
def export_autres():
    return send_file(make_dummy_xlsx(),
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     download_name="autres.xlsx")

@app.route("/api/export/etat", methods=["GET"])
def export_etat():
    return send_file(make_dummy_xlsx(),
                     mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                     download_name="etat.xlsx")

@app.route("/api/export/pdf/equipements", methods=["GET"])
def export_pdf_equip():
    pdf = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n0\n%%EOF"
    return send_file(io.BytesIO(pdf), mimetype="application/pdf", download_name="equipements.pdf")

@app.route("/api/export/pdf/autres", methods=["GET"])
def export_pdf_autres():
    pdf = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n0\n%%EOF"
    return send_file(io.BytesIO(pdf), mimetype="application/pdf", download_name="autres.pdf")

@app.route("/api/export/pdf/global", methods=["GET"])
def export_pdf_global():
    pdf = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R>>endobj\nxref\n0 4\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n0\n%%EOF"
    return send_file(io.BytesIO(pdf), mimetype="application/pdf", download_name="rapport_global.pdf")

# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@app.route("/api/admin/agents", methods=["GET"])
def get_agents():
    return jsonify(AGENTS)

@app.route("/api/admin/agents", methods=["POST"])
def create_agent():
    data = request.json or {}
    data["id"] = next_id["agent"]
    next_id["agent"] += 1
    AGENTS.append(data)
    return jsonify(data), 201

@app.route("/api/admin/agents/<int:agent_id>", methods=["DELETE"])
def delete_agent(agent_id):
    global AGENTS
    AGENTS = [a for a in AGENTS if a["id"] != agent_id]
    return "", 204

@app.route("/api/admin/activites", methods=["GET"])
def get_activites():
    return jsonify(ACTIVITES)

@app.route("/api/admin/activites/<int:agent_id>", methods=["GET"])
def get_activites_by_agent(agent_id):
    return jsonify([a for a in ACTIVITES if a["agentId"] == agent_id])

# ---------------------------------------------------------------------------
# Localisations
# ---------------------------------------------------------------------------

@app.route("/api/localisations", methods=["GET"])
def get_localisations():
    return jsonify(LOCALISATIONS)

@app.route("/api/localisations", methods=["POST"])
def create_localisation():
    data = request.json or {}
    data["id"] = next_id["local"]
    next_id["local"] += 1
    LOCALISATIONS.append(data)
    return jsonify(data), 201

@app.route("/api/localisations/<int:loc_id>", methods=["DELETE"])
def delete_localisation(loc_id):
    global LOCALISATIONS
    LOCALISATIONS = [l for l in LOCALISATIONS if l["id"] != loc_id]
    return "", 204

# ---------------------------------------------------------------------------
# Gemini AI (mock)
# ---------------------------------------------------------------------------

@app.route("/api/gemini/identify", methods=["POST"])
def identify_object():
    # Simule une réponse IA — en vrai le backend analyserait l'image
    return jsonify({
        "type": "Ordinateur Portable",
        "designation": "Ordinateur Portable",
        "description": "Appareil électronique portable de type laptop. Marque probable : Dell ou HP. Écran 15 pouces. Idéal pour usage bureautique.",
        "marque": "Dell",
        "categorie": "Informatique"
    })

# ---------------------------------------------------------------------------
# Import Excel (upload)
# ---------------------------------------------------------------------------

@app.route("/api/import/equipements", methods=["POST"])
def import_equipements():
    return jsonify({"message": "Import réussi (démo)", "count": 3})

@app.route("/api/import/autres", methods=["POST"])
def import_autres():
    return jsonify({"message": "Import réussi (démo)", "count": 2})

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("  Serveur Mock Inventaire CFC — MODE DÉMO")
    print("=" * 60)
    print("  Comptes de test :")
    print("    admin  → login: ahmed.benali  / mdp: n'importe quoi")
    print("    agent  → login: fatima.zahra  / mdp: n'importe quoi")
    print()
    print("  Dans l'émulateur Android, utilise l'IP : 10.0.2.2:8080")
    print("  Sur vrai téléphone (même WiFi), utilise ton IP locale")
    print("=" * 60)
    app.run(host="0.0.0.0", port=8080, debug=True)
