import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="Dashboard Ventes", layout="wide")

st.title("Dashboard Analyse des Ventes")

# Upload fichier
uploaded_file = st.file_uploader("Uploader votre fichier CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Vérification des colonnes
    required_columns = {"ID", "Prix", "Quantite", "Remise"}
    if not required_columns.issubset(df.columns):
        st.error("Le fichier doit contenir les colonnes : ID, Prix, Quantite, Remise")
        st.stop()

    # Calculs
    df["CA_Brut"] = df["Prix"] * df["Quantite"]
    df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise"] / 100)
    df["TVA"] = df["CA_Net"] * 0.2

    # KPIs
    col1, col2, col3 = st.columns(3)
    col1.metric("CA Total", f"{df['CA_Net'].sum():,.2f}")
    col2.metric("Nombre de produits", len(df))
    col3.metric("Meilleur produit", df.loc[df["CA_Net"].idxmax(), "ID"])

    st.markdown("---")

    # Nouveau dataset
    st.subheader("Dataset après calculs")
    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # Graphique
    st.subheader("Chiffre d'affaires par produit")

    df_sorted = df.sort_values(by="CA_Net", ascending=False)

    fig, ax = plt.subplots()
    ax.bar(df_sorted["ID"], df_sorted["CA_Net"])
    ax.set_xlabel("ID Produit")
    ax.set_ylabel("CA Net")
    ax.set_title("CA Net par produit")

    st.pyplot(fig)

else:
    st.info("Veuillez uploader un fichier CSV pour commencer.")