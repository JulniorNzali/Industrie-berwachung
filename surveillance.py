import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- Paramètres ---
CHEMIN_CSV = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_enrichi.csv"

SEUILS = {
    "temperature_C"  : 150,
    "vibration_mm_s" : 5,
    "pression_bar"   : 10
}

# --- Chargement des données ---
df = pd.read_csv(CHEMIN_CSV)

# --- Analyse des anomalies ---
def analyser_anomalies(df):
    """
    Détecte les anomalies critiques dans le DataFrame.
    Retourne un dictionnaire avec le nombre d'anomalies par capteur.
    """
    anomalies = {}
    for capteur, seuil in SEUILS.items():
        nb = len(df[df[capteur] > seuil])
        anomalies[capteur] = nb
    return anomalies

# --- Génération du rapport texte ---
def generer_rapport(anomalies):
    """
    Génère un rapport texte des anomalies détectées.
    """
    maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    rapport = f"""
╔══════════════════════════════════════╗
   RAPPORT DE SURVEILLANCE AUTOMATIQUE
   Généré le : {maintenant}
╚══════════════════════════════════════╝

📊 ANALYSE DES 1000 DERNIÈRES MESURES :

🌡️  Températures critiques (>{SEUILS['temperature_C']}°C)  : {anomalies['temperature_C']} mesures
📳  Vibrations critiques   (>{SEUILS['vibration_mm_s']} mm/s) : {anomalies['vibration_mm_s']} mesures
🔵  Pressions critiques    (>{SEUILS['pression_bar']} bar)   : {anomalies['pression_bar']} mesures

"""
    total = sum(anomalies.values())
    if total > 0:
        rapport += f"⚠️  TOTAL ANOMALIES DÉTECTÉES : {total}\n"
        rapport += "🔴 ACTION REQUISE — Vérifier la ligne de production !\n"
    else:
        rapport += "✅ Aucune anomalie détectée — Ligne de production OK\n"
    
    return rapport

# --- Sauvegarde du rapport ---
def sauvegarder_rapport(rapport):
    """
    Sauvegarde le rapport dans un fichier texte.
    """
    chemin = r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\rapport.txt"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(rapport)
    print(f"📄 Rapport sauvegardé !")

# --- Envoi email (optionnel) ---
def envoyer_email(rapport, destinataire):
    """
    Envoie le rapport par email.
    Nécessite un compte Gmail avec mot de passe d'application.
    """
    EXPEDITEUR = "konguenjunior@gmail.com"      # ← remplace par ton email
    MOT_DE_PASSE = "Meineliebe1#"   # ← mot de passe d'application Gmail

    msg = MIMEMultipart()
    msg["From"]    = EXPEDITEUR
    msg["To"]      = destinataire
    msg["Subject"] = "⚠️ Rapport de surveillance - Ligne de Production"
    msg.attach(MIMEText(rapport, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as serveur:
            serveur.login(EXPEDITEUR, MOT_DE_PASSE)
            serveur.send_message(msg)
        print("📧 Email envoyé avec succès !")
    except Exception as e:
        print(f"❌ Erreur envoi email : {e}")

# --- Programme principal ---
print("🔍 Analyse en cours...")
anomalies = analyser_anomalies(df)
rapport   = generer_rapport(anomalies)

print(rapport)
sauvegarder_rapport(rapport)