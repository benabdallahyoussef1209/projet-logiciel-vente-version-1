import matplotlib
matplotlib.use('Agg')  # backend sans interface graphique
import matplotlib.pyplot as plt
import pandas as pd
import random

# =========================
# 1. Demander nombre de produits
# =========================
n = int(input("Combien de produits ? "))

# =========================
# 2. Génération dataset
# =========================
data = []

for i in range(1, n + 1):
    data.append([
        f"{i}",
        random.randint(10, 10000),
        random.randint(1, 10000),
        random.randint(0, 80)
    ])

df = pd.DataFrame(data, columns=["ID", "Prix", "Quantite", "Remise"])

# Sauvegarde CSV
df.to_csv("vente.csv", index=False)

print("\nDataset généré :")
print(df)

# =========================
# 3. Calculs
# =========================
df["CA_Brut"] = df["Prix"] * df["Quantite"]
df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise"] / 100)
df["TVA"] = df["CA_Net"] * 0.2

print("\nDataset après calculs :")
print(df)

# =========================
# 4. KPIs
# =========================
ca_total = df["CA_Net"].sum()
produit_max = df.loc[df["CA_Net"].idxmax(), "ID"]

print("\nCA Total =", ca_total)
print("Produit le plus rentable =", produit_max)

# =========================
# 5. Graphique
# ====================


# On trie les données par CA Net (décroissant) pour une meilleure lecture
df_plot = df.sort_values(by="CA_Net", ascending=False)
n_rows = len(df_plot)

# Création de la figure (Largeur 16 pour bien voir les barres)
fig, ax = plt.subplots(figsize=(16, 8))

indices = range(n_rows)
ax.bar(indices, df_plot["CA_Net"], color="skyblue", edgecolor="navy")

# Gestion de l'affichage des IDs sur l'axe X (La logique que tu voulais)
# Si tu as beaucoup de produits, on réduit la police et on tourne à 90°
if n_rows <= 30:
    step = 1
    rotation = 45
    size = 10
else:
    # Pour 50 produits et plus, on affiche tout mais en petit et vertical
    step = 1 
    rotation = 90
    size = 8

ax.set_xticks(indices[::step])
ax.set_xticklabels(df_plot["ID"].iloc[::step], rotation=rotation, fontsize=size)

ax.set_ylabel("Chiffre d'Affaires Net")
ax.set_xlabel("ID Produit")
ax.set_title(f"Performance des {n_rows} produits")

# Ajout d'une grille pour mieux lire les montants
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Ajustement automatique pour ne pas couper les labels en bas
plt.tight_layout()

# Sauvegarde au lieu de st.pyplot
plt.savefig("graph.png")
print("Graphique genere avec succes dans graph.png")

# =========================
# 6. Export final
# =========================
df.to_csv("resultats_ventes.csv", index=False)
# Sauvegarde du fichier
plt.savefig("graph.png")
print("Graphique sauvegarde sous 'graph.png'")

# =========================
# 6. Export final
# =========================
df.to_csv("resultats_final.csv", index=False)

print("\nExport terminé : resultats_final.csv")
