# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:50:12 2024

@author: druar
"""

import streamlit as st
# numpy and pandas for data manipulation
import pandas as pd
# Model load
import joblib
import requests
# sklearn methods
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

st.write("# ➤ Informations du client")

st.sidebar.success("Naviguez dans les sections du dashboard.")

# Charger les données des clients et les prédictions
@st.cache_data
def load_data():
    return pd.read_csv("./clients_dashboard.csv")

# Page d'accueil
st.subheader("➡️ Selectionnez un client dans la liste déroulante")

# Charger les données clients
clients_dashboard = load_data()
# renommer la colonne SK_ID_CURR en id client
clients_dashboard.rename(columns={'SK_ID_CURR': 'client_id'}, inplace=True)
st.session_state.clients_dashboard = clients_dashboard

# Transformer les colonnes DAYS_BIRTH et DAYS_EMPLOYED pour qu'elles soient plus lisibles
clients_dashboard_modif = clients_dashboard.copy()
clients_dashboard_modif['AGE'] = round(clients_dashboard_modif['DAYS_BIRTH']/365)
clients_dashboard_modif['YEARS_EMPLOYED'] = round(clients_dashboard_modif['DAYS_EMPLOYED']/-365)

# Sélectionner un client dans une liste déroulante
client_id = st.selectbox("Sélectionnez un client :", clients_dashboard['client_id'].unique())

# Stocker l'ID client dans session_state et le dashboard modifié
st.session_state.client_id = client_id
st.session_state.clients_dashboard_modif = clients_dashboard_modif

# Afficher les informations du client
client_info = clients_dashboard_modif[clients_dashboard_modif['client_id'] == client_id]

colonnes_a_afficher = ['AGE', 'NAME_FAMILY_STATUS_Married', 'CNT_CHILDREN', 'CNT_FAM_MEMBERS', 'AMT_INCOME_TOTAL',
                       'YEARS_EMPLOYED', 'FLAG_OWN_REALTY','NAME_INCOME_TYPE_Working']

# Format fiche d'identité
st.subheader("➡️ Fiche d'identité du client")

for col in colonnes_a_afficher:
    value = client_info[col].values[0] if not client_info[col].isnull().any() else "Non disponible"
    st.markdown(f"**{col}**: {value}")
    

# Calculer la probabilité du modèle pour ce client avec l'API
# URL de ton API
BASE_API_URL = "https://webappscoringcredit-gcbhe8axc2exdfge.francecentral-01.azurewebsites.net/predict"
url = f"{BASE_API_URL}?client_id={client_id}"  # Construire l'URL avec le paramètre client_id
response = requests.get(url)

# Extraire les données JSON de la réponse
response_json = response.json()

reponse_credit = response_json['prediction']
proba_defaut = response_json['probabilite_defaut (seuil=0.5)'][0]
st.session_state.reponse_credit = reponse_credit
st.session_state.proba_defaut = proba_defaut

# Charger le modèle pour l'interprétation du score
logistic_model = joblib.load("C:/Users/druar/OneDrive/Documents/01_Formations/1_Outils_ET_Metier/2024_DataScientist/ProjetsPython/P7/logistic_model.pkl")
st.session_state.logistic_model = logistic_model

X = clients_dashboard.drop(columns=['client_id'])
st.session_state.X = X

# Centrer-réduire
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Imputer les valeurs manquantes
imputer = SimpleImputer(strategy='median')
X_scaled_imputed = imputer.fit_transform(X_scaled)
st.session_state.X_scaled_imputed = X_scaled_imputed

# 
proba = logistic_model.predict_proba(X_scaled_imputed)[:, 1] 
pred = logistic_model.predict(X_scaled_imputed) # 0 ou 1
clients_dashboard_modif['proba_defaut']=proba
clients_dashboard_modif['reponse_credit']=pred
st.session_state.clients_dashboard_modif = clients_dashboard_modif