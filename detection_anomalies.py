import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# --- Chargement des données ---
chemin = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_enrichi.csv"
df = pd.read_csv(chemin)

# ============================================
# PARTIE 1 — Moyennes mobiles
# ============================================
print("=" * 50)
print("📈 PARTIE 1 — MOYENNES MOBILES")
print("=" * 50)

# Calculer la moyenne mobile sur 20 mesures
df["temp_moyenne_mobile"] = df["temperature_C"].rolling(window=20).mean()

# Visualiser
plt.figure(figsize=(12, 5))
plt.plot(df["id"], df["temperature_C"],
         color="orange", linewidth=0.6, alpha=0.7, label="Température brute")
plt.plot(df["id"], df["temp_moyenne_mobile"],
         color="red", linewidth=2, label="Moyenne mobile (20 mesures)")
plt.axhline(y=150, color="black", linestyle="--", label="Seuil critique")
plt.title("Température brute vs Moyenne mobile")
plt.xlabel("Numéro de mesure")
plt.ylabel("Température (°C)")
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\moyenne_mobile.png")
plt.show()
print("✅ Graphique moyenne mobile sauvegardé !")

# ============================================
# PARTIE 2 — Détection par Z-score
# ============================================
print("\n" + "=" * 50)
print("📊 PARTIE 2 — DÉTECTION PAR Z-SCORE")
print("=" * 50)

# Calculer le Z-score pour chaque capteur
df["zscore_temp"] = np.abs(stats.zscore(df["temperature_C"]))
df["zscore_vib"]  = np.abs(stats.zscore(df["vibration_mm_s"]))
df["zscore_pres"] = np.abs(stats.zscore(df["pression_bar"]))

# Un Z-score > 3 = anomalie statistique
SEUIL_ZSCORE = 3

anomalies_zscore = df[
    (df["zscore_temp"] > SEUIL_ZSCORE) |
    (df["zscore_vib"]  > SEUIL_ZSCORE) |
    (df["zscore_pres"] > SEUIL_ZSCORE)
]

print(f"Anomalies détectées par Z-score : {len(anomalies_zscore)} mesures")
print(anomalies_zscore[["id", "date_heure", "temperature_C",
                          "vibration_mm_s", "pression_bar"]].head(10))

# ============================================
# PARTIE 3 — Classification NORMAL/ATTENTION/CRITIQUE
# ============================================
print("\n" + "=" * 50)
print("🏷️  PARTIE 3 — CLASSIFICATION AVANCÉE")
print("=" * 50)

def classifier_mesure(row):
    """
    Classifie une mesure selon le Z-score et les seuils fixes.
    """
    # Critique si Z-score > 3 ou seuils dépassés
    if (row["zscore_temp"] > SEUIL_ZSCORE or
        row["zscore_vib"]  > SEUIL_ZSCORE or
        row["zscore_pres"] > SEUIL_ZSCORE):
        return "CRITIQUE"
    # Attention si Z-score entre 2 et 3
    elif (row["zscore_temp"] > 2 or
          row["zscore_vib"]  > 2 or
          row["zscore_pres"] > 2):
        return "ATTENTION"
    else:
        return "NORMAL"

df["etat_zscore"] = df.apply(classifier_mesure, axis=1)

# Résumé
print(df["etat_zscore"].value_counts())

# Visualiser les anomalies détectées
plt.figure(figsize=(12, 5))
normales   = df[df["etat_zscore"] == "NORMAL"]
attention  = df[df["etat_zscore"] == "ATTENTION"]
critiques  = df[df["etat_zscore"] == "CRITIQUE"]

plt.scatter(normales["id"],  normales["temperature_C"],
            color="green", s=5, label="Normal", alpha=0.5)
plt.scatter(attention["id"], attention["temperature_C"],
            color="orange", s=15, label="Attention", alpha=0.8)
plt.scatter(critiques["id"], critiques["temperature_C"],
            color="red", s=20, label="Critique", alpha=0.9)
plt.axhline(y=150, color="black", linestyle="--", label="Seuil critique")
plt.title("Classification des mesures par Z-score")
plt.xlabel("Numéro de mesure")
plt.ylabel("Température (°C)")
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\zscore_classification.png")
plt.show()
print("✅ Graphique Z-score sauvegardé !")

# Sauvegarder le DataFrame enrichi
chemin_final = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_final.csv"
df.to_csv(chemin_final, index=False)
print("\n✅ Fichier final sauvegardé !")
print(f"\n📊 Résumé final :")
print(f"   NORMAL    : {len(normales)} mesures")
print(f"   ATTENTION : {len(attention)} mesures")
print(f"   CRITIQUE  : {len(critiques)} mesures")