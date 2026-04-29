# ============================================
# PROJET : Surveillance Ligne de Production
# Script : Génération des données capteurs
# Semaine 1
# ============================================

import random
import csv
from datetime import datetime, timedelta

# --- Paramètres de la simulation ---
NOMBRE_MESURES = 1000        # Nombre de lignes de données
INTERVALLE_SECONDES = 30     # Une mesure toutes les 30 secondes

# --- Date de départ de la simulation ---
date_depart = datetime(2026, 3, 30, 6, 0, 0)  # 30 mars 2026 à 6h00

# --- Fonction qui simule les capteurs ---
def generer_mesure(date_heure, numero):
    
    # Température normale entre 60°C et 120°C
    # Parfois une anomalie au-dessus de 150°C
    if random.random() < 0.05:  # 5% de chances d'anomalie
        temperature = round(random.uniform(150, 200), 2) # ANOMALIE !
    else:
        temperature = round(random.uniform(60, 120), 2) # Normal
    
    # Vibration normale entre 0.5 et 3.0 mm/s
    if random.random() < 0.05:
        vibration = round(random.uniform(5, 10), 2)
    else:
        vibration = round(random.uniform(0.5, 3.0), 2)
    
    # Pression normale entre 4 et 8 bars
    if random.random() < 0.05:
        pression = round(random.uniform(10, 15), 2)
    else:
        pression = round(random.uniform(4, 8), 2)
    
    return {
        "id": numero,
        "date_heure": date_heure.strftime("%Y-%m-%d %H:%M:%S"),
        "temperature_C": temperature,
        "vibration_mm_s": vibration,
        "pression_bar": pression
    }

# --- Génération des 1000 mesures ---
mesures = []
for i in range(NOMBRE_MESURES):
    date_mesure = date_depart + timedelta(seconds=i * INTERVALLE_SECONDES)
    mesure = generer_mesure(date_mesure, i + 1)
    mesures.append(mesure)

# --- Sauvegarde dans le fichier CSV ---
chemin_fichier = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs.csv"

with open(chemin_fichier, mode='w', newline='', encoding='utf-8') as fichier_csv:
    colonnes = ["id", "date_heure", "temperature_C", "vibration_mm_s", "pression_bar"]
    writer = csv.DictWriter(fichier_csv, fieldnames=colonnes)
    
    writer.writeheader()        # Écrit les titres des colonnes
    writer.writerows(mesures)   # Écrit toutes les mesures

print(f"✅ Fichier généré avec succès !")
print(f"📊 {NOMBRE_MESURES} mesures enregistrées")
print(f"📁 Fichier sauvegardé ici : {chemin_fichier}")