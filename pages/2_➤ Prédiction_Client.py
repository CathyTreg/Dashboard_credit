# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:50:12 2024

@author: druar
"""

import streamlit as st
# numpy and pandas for data manipulation
import pandas as pd
import numpy as np
# Plots
import shap
import plotly.graph_objects as go
import matplotlib.pyplot as plt


st.write("# ➤ Prédictions pour le client")
st.write("Cette section vous permet de prédire la probabilité de défaut de paiement du client et de savoir si son crédit est accepté au vu de cette probabilité.")


st.sidebar.success("Naviguez dans les sections du dashboard.")

# Accéder à l'ID client stocké dans session_state
client_id = st.session_state.client_id
clients_dashboard = st.session_state.clients_dashboard
clients_dashboard_modif = st.session_state.clients_dashboard_modif
proba_defaut = st.session_state.proba_defaut
reponse_credit = st.session_state.reponse_credit
logistic_model = st.session_state.logistic_model
X_scaled_imputed = st.session_state.X_scaled_imputed
X = st.session_state.X

st.subheader(f"➡️ L'ID client que vous avez sélectionné est : {client_id}")

st.write("Vous pouvez choisir un nouveau client en le sélectionnant dans l'onglet Informations Client.")

st.subheader(f"➡️ Probabilité de défaut de paiement : {proba_defaut * 100:.2f}%")

# Création de la jauge avec Plotly
fig = go.Figure(go.Indicator(
    mode="gauge",
    value=proba_defaut,
    gauge={
        'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "black"},
        'borderwidth': 2,
        'steps': [
            {'range': [0, 0.4], 'color': "green"},
            {'range': [0.4, 0.6], 'color': "orange"},
            {'range': [0.6, 1], 'color': "red"}
        ],
        'threshold': {
            'line': {'color': "black", 'width': 4},  # Seuil en noir
            'thickness': 0.75,
            'value': 0.5
        }
    },
    domain={'x': [0, 1], 'y': [0, 1]}
))

# Ajout du texte "Seuil" au-dessus de la barre du seuil
fig.add_annotation(
    x=0.5,  # Position x (correspond au seuil)
    y=1.0,  # Position y au-dessus de la jauge
    text="Seuil de défaut",  # Texte à afficher
    showarrow=False,
    font=dict(size=14, color="black"),  # Style du texte
    xanchor="center"  # Centre du texte au-dessus du seuil
)

fig.add_annotation(
    x=0.5,  # Position x 
    y=0,  # Position y 
    text=f"<b>Pour le client {client_id} : {reponse_credit}</b>",  # Texte à afficher
    showarrow=False,
    font=dict(size=20, color="black"),  # Style du texte
    xanchor="center"  # Centre du texte au-dessus du seuil
)

# Redimensionnement du graphique
fig.update_layout(
    autosize=False,
    width=400,  # Largeur ajustée
    height=300,  # Hauteur ajustée
    margin=dict(l=30, r=30, t=30, b=30)  # Marges pour aérer le design
)

# Affichage de la jauge dans Streamlit
st.plotly_chart(fig)

st.subheader("➡️ Variables qui ont contribué au modèle")

# Interprétation du score avec SHAP
explainer = shap.LinearExplainer(logistic_model, X_scaled_imputed)
X_df = pd.DataFrame(X_scaled_imputed, columns=np.array(X.columns))
shap_values = explainer.shap_values(X_df)

# summary_plot
fig_summary = plt.figure()  # Créer explicitement une figure
shap.summary_plot(shap_values, X, max_display=10, show=False)  # Ne pas afficher automatiquement la figure
st.pyplot(fig_summary)  # Passer la figure à st.pyplot()

st.markdown(
    """
    <div style="background-color: #d9edf7; padding: 10px; border-radius: 5px; border: 1px solid #bce8f1;">
        <b>Evaluation de l’importance de chaque  caractéristique dans le modèle :</b>
        <ul>
            Les valeurs SHAP (SHapley Additive exPlanations) fournissent des explications sur la contribution de chaque caractéristique (feature) à la prédiction d'un modèle de machine learning. 
            <li> La dispersion des points le long de l'axe et la densité de points à différentes valeurs SHAP reflètent l'importance relative de chaque caractéristique dans le modèle.</li>
            <li> La variable client_bureau_balance_STATUS_C_count_norm_mean (fréquence moyenne à laquelle un client clôture des prêts dans son historique de crédit) est considérée comme la plus importante pour expliquer les prédictions du modèle. Pour une valeur élevée de cette variable (points rouges), la probabilité de défaut du client sera faible (SHAP value négative).</li>
            <li> Pour une valeur faible de la variable bureau_DAYS_CREDIT_sum (points bleus), la probabilité de défaut du client sera faible (SHAP value négative).</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.text("\n")
st.subheader(f"➡️ Données qui ont contribué à prédire ce score pour le client : {client_id}")

# Sélection du client
client_index = clients_dashboard[clients_dashboard['client_id'] == client_id].index[0]
client_shap_values = shap_values[client_index]

# Suppose que 'client_shap_values' représente les valeurs SHAP d'un seul client et 'X' le DataFrame des données.
client_data = X_df.iloc[client_index]  # Les données du client

# Créer un objet shap.Explanation
client_explanation = shap.Explanation(
    values=client_shap_values,  # Les valeurs SHAP pour ce client
    base_values=explainer.expected_value,  # La valeur de base (expected_value)
    data=client_data,  # Les données de l'individu
    feature_names=X.columns  # Les noms des colonnes (caractéristiques)
)

# Créer le waterfall plot avec l'objet Explanation
fig_waterfall = plt.figure()
shap.waterfall_plot(client_explanation, show=False)
st.pyplot(fig_waterfall)

st.markdown(
    """
    <div style="background-color: #d9edf7; padding: 10px; border-radius: 5px; border: 1px solid #bce8f1;">
        <b>Interprétation pour le client :</b>
        <ul>
            <li>La Base Value f(x) (ici exprimée en log-odds) représente (après transformation) la probabilité moyenne avant d'examiner cet exemple spécifique.</li>
            <li>Les caractéristiques avec une contribution négative diminuent la probabilité de défaut du client.</li>
            <li>Les caractéristiques avec une contribution positive augmentent la probabilité de défaut du client.</li>
            <li>En ajoutant ces contributions à la base value, vous obtenez la Prédiction Finale pour ce client.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)
