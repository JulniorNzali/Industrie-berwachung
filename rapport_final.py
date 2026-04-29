# ============================================
# PROJET : Surveillance Ligne de Production
# Script : Rapport Final PDF
# Semaine 8
# ============================================

import pandas as pd
from fpdf import FPDF
from datetime import datetime

# --- Chargement des données ---
df_enrichi = pd.read_csv(r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_enrichi.csv")
df_final   = pd.read_csv(r"C:\Users\nzali\Documents\Projet_Surveillance\data\capteurs_final.csv")

# --- Calcul des statistiques ---
stats_temp = df_enrichi["temperature_C"].describe()
stats_vib  = df_enrichi["vibration_mm_s"].describe()
stats_pres = df_enrichi["pression_bar"].describe()

nb_normal    = len(df_final[df_final["etat_zscore"] == "NORMAL"])
nb_attention = len(df_final[df_final["etat_zscore"] == "ATTENTION"])
nb_critique  = len(df_final[df_final["etat_zscore"] == "CRITIQUE"])

# ============================================
# CRÉATION DU PDF
# ============================================

class RapportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(30, 80, 160)
        self.set_text_color(255, 255, 255)
        self.cell(0, 12, "RAPPORT DE SURVEILLANCE - LIGNE DE PRODUCTION", 
                  align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()} | Rapport généré automatiquement par Python",
                  align="C")

pdf = RapportPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# --- Titre principal ---
pdf.set_font("Helvetica", "B", 20)
pdf.set_text_color(30, 80, 160)
pdf.ln(5)
pdf.cell(0, 12, "Système de Surveillance Industrielle", 
         align="C", new_x="LMARGIN", new_y="NEXT")

pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, f"Rapport généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')}",
         align="C", new_x="LMARGIN", new_y="NEXT")
pdf.ln(8)

# --- Section 1 : Résumé exécutif ---
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(30, 80, 160)
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 10, "1. Résumé Exécutif", fill=True,
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(0, 0, 0)
resume = (
    f"Ce rapport présente l'analyse complète de {len(df_enrichi)} mesures "
    f"collectées sur la ligne de production le 30 mars 2026. "
    f"Les données incluent trois capteurs : température, vibration et pression. "
    f"L'analyse a été réalisée avec Python en utilisant Pandas, Matplotlib, "
    f"SciPy et Scikit-learn."
)
pdf.multi_cell(0, 7, resume)
pdf.ln(5)

# --- Section 2 : Statistiques ---
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(30, 80, 160)
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 10, "2. Statistiques des Capteurs", fill=True,
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

# Tableau des statistiques
entetes  = ["Capteur", "Minimum", "Maximum", "Moyenne", "Écart-type"]
largeurs = [50, 30, 30, 35, 35]

pdf.set_font("Helvetica", "B", 10)
pdf.set_fill_color(30, 80, 160)
pdf.set_text_color(255, 255, 255)
for entete, largeur in zip(entetes, largeurs):
    pdf.cell(largeur, 8, entete, border=1, fill=True, align="C")
pdf.ln()

donnees = [
    ["Température (°C)",
     f"{stats_temp['min']:.1f}",
     f"{stats_temp['max']:.1f}",
     f"{stats_temp['mean']:.1f}",
     f"{stats_temp['std']:.1f}"],
    ["Vibration (mm/s)",
     f"{stats_vib['min']:.2f}",
     f"{stats_vib['max']:.2f}",
     f"{stats_vib['mean']:.2f}",
     f"{stats_vib['std']:.2f}"],
    ["Pression (bar)",
     f"{stats_pres['min']:.1f}",
     f"{stats_pres['max']:.1f}",
     f"{stats_pres['mean']:.1f}",
     f"{stats_pres['std']:.1f}"],
]

pdf.set_font("Helvetica", "", 10)
for i, ligne in enumerate(donnees):
    if i % 2 == 0:
        pdf.set_fill_color(245, 248, 255)
    else:
        pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    for valeur, largeur in zip(ligne, largeurs):
        pdf.cell(largeur, 7, valeur, border=1, fill=True, align="C")
    pdf.ln()

pdf.ln(8)

# --- Section 3 : Classification ---
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(30, 80, 160)
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 10, "3. Classification des Mesures (Z-score)", fill=True,
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

etats = [
    ("NORMAL",    nb_normal,    f"{nb_normal/len(df_final)*100:.1f}%",    (0, 150, 0)),
    ("ATTENTION", nb_attention, f"{nb_attention/len(df_final)*100:.1f}%", (200, 120, 0)),
    ("CRITIQUE",  nb_critique,  f"{nb_critique/len(df_final)*100:.1f}%",  (200, 0, 0)),
]

pdf.set_font("Helvetica", "B", 10)
pdf.set_fill_color(30, 80, 160)
pdf.set_text_color(255, 255, 255)
for entete, largeur in zip(["État", "Nb mesures", "Pourcentage"], [60, 60, 60]):
    pdf.cell(largeur, 8, entete, border=1, fill=True, align="C")
pdf.ln()

pdf.set_font("Helvetica", "B", 10)
for etat, nb, pct, couleur in etats:
    pdf.set_fill_color(*couleur)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 7, etat, border=1, fill=True, align="C")
    pdf.set_fill_color(245, 248, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, str(nb), border=1, fill=True, align="C")
    pdf.cell(60, 7, pct, border=1, fill=True, align="C")
    pdf.ln()

pdf.ln(8)

# --- Section 4 : Graphiques ---
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(30, 80, 160)
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 10, "4. Visualisations", fill=True,
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

graphiques = [
    (r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\temperature.png",
     "Évolution de la température"),
    (r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\moyenne_mobile.png",
     "Moyenne mobile de la température"),
    (r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\zscore_classification.png",
     "Classification par Z-score"),
    (r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\matrice_confusion.png",
     "Matrice de confusion ML"),
]

for chemin_img, titre in graphiques:
    try:
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, titre, new_x="LMARGIN", new_y="NEXT")
        pdf.image(chemin_img, w=170)
        pdf.ln(4)
    except Exception:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 7, f"[Image non disponible : {titre}]",
                 new_x="LMARGIN", new_y="NEXT")

# --- Section 5 : Conclusion ---
pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(30, 80, 160)
pdf.set_fill_color(230, 240, 255)
pdf.cell(0, 10, "5. Conclusion et Recommandations", fill=True,
         new_x="LMARGIN", new_y="NEXT")
pdf.ln(3)

pdf.set_font("Helvetica", "", 11)
pdf.set_text_color(0, 0, 0)
conclusion = (
    f"L'analyse des {len(df_enrichi)} mesures de la ligne de production révèle "
    f"que {nb_normal/len(df_final)*100:.1f}% des mesures sont dans un état normal. "
    f"Cependant, {nb_critique} mesures critiques ({nb_critique/len(df_final)*100:.1f}%) "
    f"ont été détectées, nécessitant une attention immédiate.\n\n"
    f"Le modèle de Machine Learning (Random Forest) a atteint une précision de 100% "
    f"sur les données de test, confirmant la fiabilité du système de détection.\n\n"
    f"Recommandations :\n"
    f"  - Vérifier les capteurs de pression (67 dépassements de seuil)\n"
    f"  - Planifier une maintenance préventive sur la ligne\n"
    f"  - Déployer le script de surveillance automatique\n"
    f"  - Mettre en place des alertes email en temps réel"
)
pdf.multi_cell(0, 7, conclusion)

# --- Sauvegarde ---
chemin_pdf = r"C:\Users\nzali\Documents\Projet_Surveillance\outputs\rapport_final.pdf"
pdf.output(chemin_pdf)
print("=" * 50)
print("✅ Rapport PDF généré avec succès !")
print(f"📁 Sauvegardé ici : {chemin_pdf}")
print("=" * 50)