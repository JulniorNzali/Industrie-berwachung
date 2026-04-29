import pandas as pd
import matplotlib.pyplot as plt

# --- Chargement des données ---
chemin = r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_enrichi.csv"
df = pd.read_csv(chemin)

# --- Graphique 1 : Évolution de la température ---
plt.figure(figsize=(12, 4))
plt.plot(df["id"], df["temperature_C"], color="orange", linewidth=0.8)
plt.axhline(y=150, color="red", linestyle="--", label="Seuil critique (150°C)")
plt.axhline(y=120, color="yellow", linestyle="--", label="Seuil attention (120°C)")
plt.title("Évolution de la température dans le temps")
plt.xlabel("Numéro de mesure")
plt.ylabel("Température (°C)")
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\temperature.png")
plt.show()
print("✅ Graphique 1 sauvegardé !")

# --- Graphique 2 : Évolution de la vibration ---
plt.figure(figsize=(12, 4))
plt.plot(df["id"], df["vibration_mm_s"], color="blue", linewidth=0.8)
plt.axhline(y=5, color="red", linestyle="--", label="Seuil critique (5 mm/s)")
plt.axhline(y=3, color="yellow", linestyle="--", label="Seuil attention (3 mm/s)")
plt.title("Évolution de la vibration dans le temps")
plt.xlabel("Numéro de mesure")
plt.ylabel("Vibration (mm/s)")
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\vibration.png")
plt.show()
print("✅ Graphique 2 sauvegardé !")

# --- Graphique 3 : Répartition des états ---
plt.figure(figsize=(6, 6))
etats = df["etat"].value_counts()
couleurs = {"NORMAL": "green", "ATTENTION": "orange", "CRITIQUE": "red"}
plt.pie(etats, labels=etats.index, autopct="%1.1f%%",
        colors=[couleurs.get(e, "gray") for e in etats.index])
plt.title("Répartition des états machine")
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\etats.png")
plt.show()
print("✅ Graphique 3 sauvegardé !")

# --- Graphique 4 : Corrélation température / vibration ---
plt.figure(figsize=(6, 6))
couleurs_points = df["etat"].map({"NORMAL": "green", "ATTENTION": "orange", "CRITIQUE": "red"})
plt.scatter(df["temperature_C"], df["vibration_mm_s"],
            c=couleurs_points, alpha=0.4, s=10)
plt.axvline(x=150, color="red", linestyle="--", label="Seuil T critique")
plt.axhline(y=5, color="blue", linestyle="--", label="Seuil V critique")
plt.title("Corrélation température / vibration")
plt.xlabel("Température (°C)")
plt.ylabel("Vibration (mm/s)")
plt.legend()
plt.tight_layout()
plt.savefig(r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\correlation.png")
plt.show()
print("✅ Graphique 4 sauvegardé !")

print("\n🎉 Tous les graphiques ont été générés !")