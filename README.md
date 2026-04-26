# Dashboard Analyse des Ventes (Streamlit)

Ce projet est une application web développée avec Streamlit permettant d’analyser des données de ventes, de calculer des indicateurs clés et de visualiser les performances commerciales.

---

## Objectif du projet

Le projet répond à l’énoncé du PFA en intégrant :

- Génération automatique du fichier `vente.csv` à partir d’un script Python
- Traitement des données (calculs financiers)
- Visualisation des résultats
- Export des données finales

---

## Fonctionnalités

### 1. Génération automatique des données
- Création d’un fichier `vente.csv` contenant :
  - ID
  - Prix
  - Quantite
  - Remise

### 2. Chargement des données
- Utilisation du fichier généré automatiquement
- Possibilité d’uploader un fichier CSV (fonctionnalité bonus)

### 3. Calculs effectués
- Chiffre d’affaires brut (CA_Brut)
- Chiffre d’affaires net (CA_Net)
- TVA

### 4. Affichage des résultats
- Dataset initial
- Dataset après calculs
- Indicateurs clés (KPI) :
  - CA total
  - Nombre de produits
  - Produit le plus rentable

### 5. Visualisation
- Graphique du chiffre d’affaires par produit (Matplotlib)

## Technologies utilisées

- Python
- Streamlit
- Pandas
- Matplotlib
## Lancer le projet en local

### Installer les dépendances

```bash id="inst1"
pip install -r requirements.txt
### Installer les dépendances

```bash
pip install -r requirements.txt
```
Lancer l’application
```` bash
streamlit run app.py
`````
Application en ligne

Lien vers l’application Streamlit : https://projet-logiciel-vente-version-1-suyt238tasusiyj4gncgen.streamlit.app/
