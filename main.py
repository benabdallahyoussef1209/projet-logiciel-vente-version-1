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
# =========================
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

n = len(df)

# On définit 'step' pour n'afficher qu'environ 10 à 15 labels max
# Si n=100, step=10. Si n=50, step=5.
step = max(1, n // 10) 

plt.figure(figsize=(12,5))
plt.bar(df["ID"].astype(str), df["CA_Net"])

# On applique le pas dynamique
plt.xticks(range(0, n, step), df["ID"].iloc[::step], rotation=45)

plt.xlabel("Produit ID")
plt.ylabel("CA Net")
plt.title(f"CA Net par Produit (Echelle 1/{step})")

plt.tight_layout()
plt.savefig("graph.png")

# =========================
# 6. Export final
# =========================
df.to_csv("resultats_final.csv", index=False)

print("\nExport terminé : resultats_final.csv")
