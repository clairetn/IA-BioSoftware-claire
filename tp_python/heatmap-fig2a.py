import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Load the data from the Excel file ---
file_path = "../data/pgen.1006453.s002.xlsx"  # Remplace par le chemin de ton fichier
try:
    # Lire le fichier en ignorant les extensions non supportées
    data = pd.read_excel(file_path, engine="openpyxl")
except Exception as e:
    print(f"Erreur lors de la lecture du fichier Excel : {e}")
    exit(1)

# --- 2. Extraire les colonnes temporelles (0, 5, 10, ..., 245) ---
# Filtrer les colonnes qui sont des entiers (temps en minutes)
time_columns = []
for col in data.columns:
    try:
        # Vérifier si la colonne est un entier (ex: 0, 5, 10, ...)
        int(col)
        time_columns.append(col)
    except (ValueError, TypeError):
        continue

# Si aucune colonne temporelle n'est trouvée, essayer une autre approche
if not time_columns:
    # Supposer que les colonnes temporelles sont les dernières colonnes numériques
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    time_columns = sorted([int(col) for col in numeric_cols if str(col).isdigit()])

if not time_columns:
    print("Aucune colonne temporelle trouvée. Vérifie le format du fichier.")
    exit(1)

# Extraire la matrice d'expression (gènes x temps)
expression_matrix = data[time_columns].values

# Vérifier que la matrice n'est pas vide
if expression_matrix.size == 0:
    print("La matrice d'expression est vide. Vérifie les colonnes temporelles.")
    exit(1)

# --- 3. Sort genes by peak expression time ---
# Utiliser la colonne 'Figure2A_order_peaktime' si elle existe
if 'Figure2A_order_peaktime' in data.columns:
    peak_times = data['Figure2A_order_peaktime'].values
    sorted_indices = np.argsort(peak_times)
else:
    # Sinon, calculer le temps de pic à partir de la matrice
    peak_indices = np.argmax(expression_matrix, axis=1)
    timepoints = sorted([int(col) for col in time_columns])
    peak_times = np.array(timepoints)[peak_indices]
    sorted_indices = np.argsort(peak_times)

expression_sorted = expression_matrix[sorted_indices, :]

# --- 4. Plot the heatmap with blue to yellow colormap ---
plt.figure(figsize=(12, 8))
sns.heatmap(
    expression_sorted,
    cmap="YlOrBr_r",  # Bleu à jaune
    center=0,
    vmin=-3,
    vmax=3,
    xticklabels=5,  # Affiche un label tous les 5 points temporels
    yticklabels=False,
    cbar_kws={"label": "Expression (Normalized)"}
)

# --- 5. Customize the plot ---
plt.title("Figure 2A: Periodic Genes in S. cerevisiae\n(Sorted by Peak Expression Time)", pad=20)
plt.xlabel("Time (min)")
plt.xticks(np.arange(0, len(time_columns), 5), time_columns[::5])
plt.tight_layout()
plt.show()
