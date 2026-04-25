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
# Génération automatique (exigée)
# =========================
def generate_data():
    data = []
    for i in range(1, 11):
        data.append([
            f"A{i}",
            random.randint(5, 50),
            random.randint(1, 10),
            random.randint(0, 20)
        ])
    df = pd.DataFrame(data, columns=["ID", "Prix", "Quantite", "Remise"])
    df.to_csv("vente.csv", index=False)
    return df

# =========================
# Choix utilisateur
# =========================
st.sidebar.header("Source des données")
option = st.sidebar.radio(
    "Choisir la source :",
    ["Fichier généré automatiquement", "Uploader un fichier"]
)

# =========================
# Chargement des données
# =========================
if option == "Fichier généré automatiquement":
    df = generate_data()
    st.success("Fichier vente.csv généré automatiquement")

    # 🔥 Affichage dataset généré
    st.subheader("Dataset généré automatiquement")
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
required_columns = {"ID", "Prix", "Quantite", "Remise"}
if not required_columns.issubset(df.columns):
    st.error("Le fichier doit contenir : ID, Prix, Quantite, Remise")
    st.stop()

# =========================
# Calculs
# =========================
df["CA_Brut"] = df["Prix"] * df["Quantite"]
df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise"] / 100)
df["TVA"] = df["CA_Net"] * 0.2

st.markdown("---")

# 🔥 Dataset après calculs
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
# Graphique
# =========================
st.subheader("Chiffre d'affaires par produit")

df_sorted = df.sort_values(by="CA_Net", ascending=False)

fig, ax = plt.subplots()
ax.bar(df_sorted["ID"], df_sorted["CA_Net"])
ax.set_xlabel("ID Produit")
ax.set_ylabel("CA Net")
ax.set_title("CA Net par produit")

st.pyplot(fig)

# =========================
# Téléchargement CSV
# =========================
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Télécharger le dataset final", csv, "resultats.csv", "text/csv")