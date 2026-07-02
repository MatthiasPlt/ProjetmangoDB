import streamlit as st
import requests
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Talabat Advanced Analytics", layout="wide")

st.title("🚴 Tableau de Bord Analytique Avancé - Talabat Logistics")
st.markdown("---")

API_URL = "http://localhost:5000/api/kpi"

# =========================================================
# SECTION 1 : LES COMPTEURS GLOBAUX (KPI Cards)
# =========================================================
try:
    stats_resp = requests.get(f"{API_URL}/global-stats")
    if stats_resp.status_code == 200:
        stats = stats_resp.json()
        
        # Création de 3 colonnes pour afficher des cartes de scores
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="💰 Chiffre d'Affaires Cumulé", value=f"{stats.get('total_ca', 0):,.2f} EGP")
        kpi2.metric(label="📦 Commandes Traitées", value=f"{stats.get('total_commandes', 0):,}")
        kpi3.metric(label="🛣️ Distance Totale Parcourue", value=f"{stats.get('total_distance', 0):,.2f} km")
except Exception as e:
    st.error("Impossible de charger les statistiques globales.")

st.markdown("---")

# =========================================================
# SECTION 2 : REQUÊTE GÉOGRAPHIQUE (Chiffre d'affaires par ville)
# =========================================================
st.subheader("🏙️ Performance Commerciale par Ville")
try:
    response = requests.get(f"{API_URL}/revenue-by-city")
    if response.status_code == 200:
        df_city = pd.DataFrame(response.json())
        df_city = df_city.rename(columns={
            "_id": "Ville", 
            "chiffre_affaires": "Chiffre d'Affaires (EGP)",
            "panier_moyen": "Panier Moyen (EGP)",
            "nombre_commandes": "Volume"
        })
        
        # Affichage côte à côte : Graphique et Tableau de données brut (NoSQL)
        c_left, c_right = st.columns([2, 1])
        with c_left:
            st.bar_chart(data=df_city, x="Ville", y="Chiffre d'Affaires (EGP)", color="#FF5733")
        with c_right:
            st.dataframe(df_city[["Ville", "Volume", "Panier Moyen (EGP)"]], use_container_width=True)
except Exception as e:
    st.error("Erreur lors du chargement des données par ville.")

st.markdown("---")

# =========================================================
# SECTION 3 : ANALYSE TEMPORELLE & LOGISTIQUE
# =========================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Impact du trafic sur la durée de livraison")
    try:
        response = requests.get(f"{API_URL}/traffic-impact")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = df.rename(columns={"_id": "Niveau de Trafic", "duree_moyenne_minutes": "Minutes"})
            st.bar_chart(data=df, x="Niveau de Trafic", y="Minutes", color="#FF4B4B")
    except Exception as e:
        st.error("Erreur trafic.")

with col2:
    st.subheader("🚗 Véhicule le plus rapide (Trafic Intense)")
    try:
        response = requests.get(f"{API_URL}/best-vehicles-high-traffic")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = df.rename(columns={"_id": "Type de Véhicule", "temps_moyen_minutes": "Minutes"})
            st.bar_chart(data=df, x="Type de Véhicule", y="Minutes", color="#00C0F2")
    except Exception as e:
        st.error("Erreur véhicules.")

st.markdown("---")

# =========================================================
# SECTION 4 : ARTICLES & MAINTENANCE
# =========================================================
col3, col4 = st.columns(2)

with col3:
    st.subheader("🍗 Top 5 des articles les plus vendus")
    try:
        response = requests.get(f"{API_URL}/top-items")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = df.rename(columns={"_id": "Article", "quantite_totale": "Quantité"})
            st.bar_chart(data=df, x="Article", y="Quantité", color="#29B094")
    except Exception as e:
        st.error("Erreur articles.")

with col4:
    st.subheader("🔧 Coût de maintenance total par type de flotte")
    try:
        response = requests.get(f"{API_URL}/maintenance-costs")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df = df.rename(columns={"_id": "Véhicule", "cout_total_reparations": "Frais de Maintenance (EGP)"})
            st.bar_chart(data=df, x="Véhicule", y="Frais de Maintenance (EGP)", color="#FFA500")
    except Exception as e:
        st.error("Erreur maintenance.")

st.markdown("---")

# =========================================================
# SECTION 5 : REQUÊTE TEMPORELLE (Heures de pointe)
# =========================================================
st.subheader("⏰ Analyse des heures de pointe (Volume de commandes par heure)")
try:
    response = requests.get(f"{API_URL}/hourly-activity")
    if response.status_code == 200:
        df_hours = pd.DataFrame(response.json())
        df_hours = df_hours.rename(columns={"_id": "Heure de la journée", "total_commandes": "Nombre de commandes"})
        # Trier par heure pour avoir une courbe logique de 0h à 23h
        df_hours = df_hours.sort_values(by="Heure de la journée")
        
        # Utilisation d'un graphique linéaire (line_chart) parfait pour le temps !
        st.line_chart(data=df_hours, x="Heure de la journée", y="Nombre de commandes", color="#7A1FA2")
except Exception as e:
    st.error("Erreur lors du chargement de l'activité horaire.")