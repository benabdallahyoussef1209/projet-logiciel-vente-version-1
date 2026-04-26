import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import random

# =========================
# Configuration
# =========================
st.set_page_config(page_title="Dashboard Ventes", layout="wide")
st.title("Dashboard Analyse des Ventes")

# =========================
# Choix source
# =========================
st.sidebar.header("Source des données")

option = st.sidebar.radio(
    "Choisir la source :",
    ["Générer un dataset", "Uploader un fichier"]
)


# =========================
# 1. Demander nombre de produits
# =========================
n = int(input("Combien de produits ? "))


# =========================
# Génération dataset
# =========================
def generate_data(n):
    data = []
    for i in range(1, n + 1):
        data.append([
            f"{i}",
            random.randint(10, 10000),
            random.randint(1, 10000),
            random.randint(0, 80)
        ])
    return pd.DataFrame(data, columns=["ID", "Prix", "Quantite", "Remise"])

# =========================
# Chargement données
# =========================
if option == "Générer un dataset":
    n = st.number_input("Nombre de produits", min_value=1, max_value=100, value=10)

    df = generate_data(n)

    st.subheader("Dataset généré")
    st.dataframe(df, use_container_width=True)

else:
    uploaded_file = st.file_uploader("Uploader votre fichier CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.subheader("Dataset uploadé")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Veuillez uploader un fichier CSV")
        st.stop()

# =========================
# Vérification colonnes
# =========================
required = {"ID", "Prix", "Quantite", "Remise"}
if not required.issubset(df.columns):
    st.error("Le fichier doit contenir : ID, Prix, Quantite, Remise")
    st.stop()

# =========================
# Calculs
# =========================
df["CA_Brut"] = df["Prix"] * df["Quantite"]
df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise"] / 100)
df["TVA"] = df["CA_Net"] * 0.2

st.markdown("---")

# =========================
# Dataset final
# =========================
st.subheader("Dataset après calculs")
st.dataframe(df, use_container_width=True)

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("CA Total", f"{df['CA_Net'].sum():,.2f}")
col2.metric("Nombre de produits", len(df))
col3.metric("Meilleur produit", df.loc[df["CA_Net"].idxmax(), "ID"])

st.markdown("---")

# =========================
# =========================
# Graphique
# =========================
st.subheader("Chiffre d'affaires par produit")

# 1. On trie les données et on réinitialise l'index pour que le calcul du step soit juste
df_sorted = df.sort_values(by="CA_Net", ascending=False).reset_index(drop=True)

# 2. Calcul du nombre de produits et du pas (step)
n = len(df_sorted)
step = max(1, n // 10)  # Affiche environ 10 labels maximum

# 3. Création de la figure
fig, ax = plt.subplots(figsize=(12, 6))

# 4. Tracé des barres (on utilise range(n) pour s'assurer que les barres sont bien alignées)
ax.bar(range(n), df_sorted["CA_Net"], color="skyblue", edgecolor="navy")

# 5. Application de ton échelle dynamique
ax.set_xticks(range(0, n, step))
ax.set_xticklabels(df_sorted["ID"].iloc[::step], rotation=45, ha='right')

# 6. Habillage
ax.set_xlabel("ID Produit")
ax.set_ylabel("CA Net")
ax.set_title(f"CA Net par produit (Échelle d'affichage : 1/{step})")
ax.grid(axis='y', linestyle='--', alpha=0.7)

# 7. Affichage dans Streamlit
st.pyplot(fig)
# =========================
# Download
# =========================
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Télécharger le dataset final", csv, "resultats.csv", "text/csv")
