import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore

# --- 1. Simulation de données (à remplacer par vos données réelles) ---
np.random.seed(42)
n_genes = 1246
n_timepoints = 30  # Exemple : 30 points temporels (0 à 150 min, pas de 5 min)
timepoints = np.arange(0, n_timepoints * 5, 5)  # 0, 5, 10, ..., 145 min

# Simulation d'une matrice d'expression (1246 gènes × 30 temps)
expression_matrix = np.random.randn(n_genes, n_timepoints) * 0.5 + 1.0  # Bruit gaussien + offset

# Ajout d'un motif périodique (exemple : pic à t=20, 40, 60, ... min)
for i in range(n_genes):
    peak_time = np.random.choice([10, 20, 30, 40, 50, 60])  # Pic aléatoire entre 10 et 60 min
    expression_matrix[i, :] += 2.0 * np.exp(-(timepoints - peak_time)**2 / (2 * 10**2))  # Pic gaussien

# --- 2. Normalisation en z-score (par gène) ---
expression_zscore = zscore(expression_matrix, axis=1)

# --- 3. Tri des gènes par temps de pic d'expression ---
peak_times = timepoints[np.argmax(expression_zscore, axis=1)]  # Temps du pic pour chaque gène
sorted_indices = np.argsort(peak_times)  # Tri par temps de pic croissant
expression_sorted = expression_zscore[sorted_indices, :]

# --- 4. Création de la heatmap ---
plt.figure(figsize=(12, 8))
sns.heatmap(
    expression_sorted,
    cmap="RdBu_r",  # Colormap rouge-bleu (comme dans l'article)
    center=0,
    vmin=-3,
    vmax=3,
    xticklabels=5,  # Affiche un label tous les 5 points temporels
    yticklabels=False,  # Masque les labels des gènes (trop nombreux)
    cbar_kws={"label": "Z-score (expression)"}
)

# --- 5. Personnalisation ---
plt.title("Figure 2A : 1246 gènes périodiques chez S. cerevisiae\n(Ordonnés par temps de pic d'expression)", pad=20)
plt.xlabel("Temps (min)")
plt.xticks(np.arange(0, n_timepoints, 5), timepoints[::5])  # Labels des temps
plt.tight_layout()
plt.show()
