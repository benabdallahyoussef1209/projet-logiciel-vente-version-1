import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 
import random

# =========================
# Configuration de la page
# =========================
st.set_page_config(page_title="Dashboard Ventes", layout="wide")
st.title("Dashboard Analyse des Ventes")

# =========================
# Fonction de génération de données
# =========================
def generate_data(n_prod):
    data = []
    for i in range(1, n_prod + 1):
        data.append([
            i,                          # ID forme numero
            random.randint(10, 1000),   # Prix entre 10 et 1000
            random.randint(1, 10),      # Quantite entre 1 et 10
            random.randint(10, 50)      # Remise entre 10 et 50
        ])
    return pd.DataFrame(data, columns=["ID", "Prix", "Quantite", "Remise"])

# =========================
# Sidebar - Choix de la source
# =========================
st.sidebar.header("Parametres")
option = st.sidebar.radio(
    "Choisir la source des données :",
    ["Générer un dataset", "Uploader un fichier"]
)

df = pd.DataFrame()

# =========================
# 1. Chargement et Validation des données
# =========================
if option == "Générer un dataset":
    n_input = st.sidebar.number_input("Nombre de produits", min_value=1, max_value=500, value=50)
    df = generate_data(n_input)
    
    st.subheader("1. Dataset genere automatiquement")
    st.write("Ce tableau contient les donnees de base (ID, Prix, Quantite, Remise) :")
    st.dataframe(df, use_container_width=True)

else:
    # Message d'instruction pour l'utilisateur
    st.sidebar.info("Le fichier CSV doit contenir les colonnes : ID, Prix, Quantite, Remise")
    
    uploaded_file = st.sidebar.file_uploader("Uploader votre fichier CSV", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Vérification automatique des colonnes
        colonnes_attendues = {"ID", "Prix", "Quantite", "Remise"}
        if not colonnes_attendues.issubset(set(df.columns)):
            st.error("Erreur : Le format du fichier est incorrect.")
            st.write(f"Colonnes detectees : {list(df.columns)}")
            st.write(f"Colonnes requises : {list(colonnes_attendues)}")
            st.stop() # Bloque l'exécution
            
        st.subheader("1. Dataset uploade")
        st.dataframe(df, use_container_width=True)
    else:
        st.stop()

# =========================
# 2. Calculs et Affichage Dataset Final
# =========================
if not df.empty:
    # On effectue les calculs
    df["CA_Brut"] = df["Prix"] * df["Quantite"]
    df["CA_Net"] = df["CA_Brut"] * (1 - df["Remise"] / 100)
    df["TVA"] = df["CA_Net"] * 0.2

    st.markdown("---")
    st.subheader("2. Dataset apres calculs")
    st.write("Ce tableau inclut maintenant le CA Brut, le CA Net et la TVA :")
    st.dataframe(df, use_container_width=True)

    # =========================
    # 3. Indicateurs Cles (KPIs)
    # =========================
    st.markdown("---")
    st.subheader("3. Indicateurs Cles")
    col1, col2, col3 = st.columns(3)

    ca_total = df["CA_Net"].sum()
    nb_produits = len(df)
    top_produit = df.loc[df["CA_Net"].idxmax(), "ID"]

    col1.metric("CA Total Net", f"{ca_total:,.2f}")
    col2.metric("Nombre de Produits", nb_produits)
    col3.metric("ID Produit le plus rentable", top_produit)

    # =========================
    # 4. Graphique
    # =========================
    st.markdown("---")
    st.subheader("4. Graphique du CA Net par Produit")
    
    df_plot = df.sort_values(by="CA_Net", ascending=False)
    n_rows = len(df_plot)

    fig, ax = plt.subplots(figsize=(16, 8))
    indices = range(n_rows)
    ax.bar(indices, df_plot["CA_Net"], color="skyblue", edgecolor="navy")
    
    # Style dynamique de l'axe X
    if n_rows <= 30:
        step = 1
        rotation = 45
        size = 10
    else:
        step = 1 
        rotation = 90
        size = 8

    ax.set_xticks(indices[::step])
    ax.set_xticklabels(df_plot["ID"].iloc[::step], rotation=rotation, fontsize=size)
    
    ax.set_ylabel("Chiffre d'Affaires Net")
    ax.set_xlabel("ID Produit")
    ax.set_title(f"Performance des {n_rows} produits")
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    st.pyplot(fig)

    # =========================
    # 5. Export
    # =========================
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Telecharger le dataset final (CSV)",
        data=csv_data,
        file_name="resultats_ventes.csv",
        mime="text/csv"
    )