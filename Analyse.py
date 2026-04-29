# ============================================
# PROJET : Surveillance Ligne de Production
# Script : Analyse des données capteurs
# Semaine 3
# ============================================

import pandas as pd

# --- Chargement du fichier CSV ---
chemin = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs.csv"
df = pd.read_csv(chemin)

# --- Exploration basique ---
print("=" * 50)
print("📊 APERÇU DES DONNÉES")
print("=" * 50)
print(df.head(10))          # Affiche les 10 premières lignes

print("\n" + "=" * 50)
print("📐 DIMENSIONS DU FICHIER")
print("=" * 50)
print(f"Nombre de lignes    : {df.shape[0]}")
print(f"Nombre de colonnes  : {df.shape[1]}")

print("\n" + "=" * 50)
print("📋 INFORMATIONS GÉNÉRALES")
print("=" * 50)
print(df.info())

print("\n" + "=" * 50)
print("📈 STATISTIQUES PAR CAPTEUR")
print("=" * 50)
print(df.describe())
# --- Filtrage des anomalies ---
print("\n" + "=" * 50)
print("⚠️ ANOMALIES DÉTECTÉES")
print("=" * 50)

# Filtrer les lignes anormales
anomalies_temp = df[df["temperature_C"] > 150]
anomalies_vib  = df[df["vibration_mm_s"] > 5]
anomalies_pres = df[df["pression_bar"] > 10]

print(f"🌡️  Températures critiques (>150°C)  : {len(anomalies_temp)} mesures")
print(f"📳  Vibrations critiques (>5 mm/s)   : {len(anomalies_vib)} mesures")
print(f"🔵  Pressions critiques (>10 bar)    : {len(anomalies_pres)} mesures")

print("\n--- Détail des températures critiques ---")
print(anomalies_temp[["id", "date_heure", "temperature_C"]].to_string())
# --- Statistiques par état ---
print("\n" + "=" * 50)
print("📊 RÉSUMÉ PAR ÉTAT")
print("=" * 50)

# Ajouter une colonne "etat" à chaque ligne
def etat_mesure(row):
    if row["temperature_C"] > 150 or row["vibration_mm_s"] > 5 or row["pression_bar"] > 10:
        return "CRITIQUE"
    elif row["temperature_C"] > 120 or row["vibration_mm_s"] > 3 or row["pression_bar"] > 8:
        return "ATTENTION"
    else:
        return "NORMAL"

df["etat"] = df.apply(etat_mesure, axis=1)

# Compter les états
print(df["etat"].value_counts())

# Sauvegarder le fichier enrichi
chemin_enrichi = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_enrichi.csv"
df.to_csv(chemin_enrichi, index=False)
print(f"\n✅ Fichier enrichi sauvegardé !")