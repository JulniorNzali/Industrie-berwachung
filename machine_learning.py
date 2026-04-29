# ============================================
# PROJET : Surveillance Ligne de Production
# Script : Machine Learning
# Semaine 7
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

# --- Chargement des données ---
chemin = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_final.csv"
df = pd.read_csv(chemin)

print("=" * 50)
print("🤖 MACHINE LEARNING — MAINTENANCE PRÉDICTIVE")
print("=" * 50)

# ============================================
# PARTIE 1 — Préparation des données
# ============================================
print("\n📋 PARTIE 1 — Préparation des données")
print("-" * 50)

# Sélectionner les features (entrées) et la cible (sortie)
features = ["temperature_C", "vibration_mm_s", "pression_bar"]
cible    = "etat_zscore"

X = df[features]   # Les mesures capteurs
y = df[cible]      # L'état de la machine

print(f"Nombre d'échantillons  : {len(X)}")
print(f"Features utilisées     : {features}")
print(f"Distribution des états :\n{y.value_counts()}")

# Diviser en données d'entraînement (80%) et de test (20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nDonnées entraînement   : {len(X_train)} échantillons")
print(f"Données test           : {len(X_test)} échantillons")

# ============================================
# PARTIE 2 — Entraînement du modèle
# ============================================
print("\n🏋️  PARTIE 2 — Entraînement du modèle")
print("-" * 50)

# Créer et entraîner le modèle Random Forest
modele = RandomForestClassifier(n_estimators=100, random_state=42)
modele.fit(X_train, y_train)

print("✅ Modèle entraîné avec succès !")

# ============================================
# PARTIE 3 — Évaluation du modèle
# ============================================
print("\n📊 PARTIE 3 — Évaluation du modèle")
print("-" * 50)

# Prédictions sur les données de test
y_pred = modele.predict(X_test)

# Rapport de classification
print("\n📈 Rapport de classification :")
print(classification_report(y_test, y_pred))

# Score global
score = modele.score(X_test, y_test)
print(f"🎯 Précision globale : {score * 100:.1f}%")

# ============================================
# PARTIE 4 — Matrice de confusion
# ============================================
print("\n🔍 PARTIE 4 — Matrice de confusion")
print("-" * 50)

# Installer seaborn si nécessaire : pip install seaborn
cm = confusion_matrix(y_test, y_pred, labels=["NORMAL", "ATTENTION", "CRITIQUE"])

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["NORMAL", "ATTENTION", "CRITIQUE"],
            yticklabels=["NORMAL", "ATTENTION", "CRITIQUE"])
plt.title("Matrice de confusion")
plt.ylabel("Valeur réelle")
plt.xlabel("Valeur prédite")
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\matrice_confusion.png")
plt.show()
print("✅ Matrice de confusion sauvegardée !")

# ============================================
# PARTIE 5 — Importance des features
# ============================================
print("\n⭐ PARTIE 5 — Importance des features")
print("-" * 50)

importances = modele.feature_importances_
plt.figure(figsize=(8, 5))
plt.bar(features, importances, color=["orange", "blue", "green"])
plt.title("Importance des capteurs pour la prédiction")
plt.xlabel("Capteur")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\importance_features.png")
plt.show()
print("✅ Graphique importance sauvegardé !")

# ============================================
# PARTIE 6 — Prédiction sur nouvelles mesures
# ============================================
print("\n🔮 PARTIE 6 — Prédiction sur nouvelles mesures")
print("-" * 50)

nouvelles_mesures = pd.DataFrame({
    "temperature_C"  : [85,  165,  95,  130],
    "vibration_mm_s" : [1.2,  7.8, 4.5,  2.1],
    "pression_bar"   : [5.5, 12.0, 7.8,  6.0]
})

predictions = modele.predict(nouvelles_mesures)

print("Nouvelles mesures → Prédictions :")
for i, (pred, row) in enumerate(zip(predictions,
                                     nouvelles_mesures.itertuples())):
    print(f"  Mesure {i+1} : "
          f"T={row.temperature_C}°C | "
          f"V={row.vibration_mm_s} mm/s | "
          f"P={row.pression_bar} bar "
          f"→ {pred}")