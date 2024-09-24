# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 17:13:46 2024

@author: druar
"""

# 1. Visualisation des caractéristiques clients par rapport aux autres clients

import numpy as np
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

st.write("# ➤ Caractéristiques du client")
st.write("Cette section vous permet de visualiser les caractéristiques d'un client et de les comparer à l'ensemble des clients.")

st.sidebar.success("Naviguez dans les sections du dashboard.")

client_id = st.session_state.client_id
clients_dashboard_modif = st.session_state.clients_dashboard_modif

st.subheader(f"➡️ L'ID client que vous avez sélectionné est : {client_id}")

st.write("Vous pouvez choisir un nouveau client en le sélectionnant dans l'onglet Informations Client.")

st.subheader("➡️ Visualisation d'une caractéristique du client par rapport aux autres clients")

# Style CSS pour augmenter la taille de la police du selectbox
st.markdown(
    """
    <style>
    label[for="selectbox"] {
        font-size: 20px;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Sélecteur pour choisir la caractéristique à visualiser
feature_to_plot = st.selectbox("Choisissez une caractéristique à visualiser", clients_dashboard_modif.columns)

# Vérifier si la valeur pour le client est NaN
client_value = clients_dashboard_modif.loc[clients_dashboard_modif['client_id'] == client_id, feature_to_plot].values[0]

if np.isnan(client_value):
    st.warning(f"La caractéristique '{feature_to_plot}' est manquante pour le client {client_id}. Veuillez sélectionner une autre caractéristique.")
else:
    # Filtrer les valeurs manquantes de la colonne sélectionnée pour l'histogramme
    filtered_feature_values = clients_dashboard_modif[feature_to_plot].dropna()

    # Calculer la distribution des fréquences avec numpy.histogram
    hist_values, bin_edges = np.histogram(filtered_feature_values, bins='auto')

    # Récupérer la fréquence maximale (max sur l'axe y)
    max_y_value = hist_values.max()

    # Créer un graphique de distribution de la caractéristique choisie
    fig = px.histogram(clients_dashboard_modif, x=feature_to_plot, title=f'Distribution de {feature_to_plot}')

    # Ajouter une ligne rouge à la valeur du client
    fig.add_vline(x=client_value, line_width=3, line_dash="dash", line_color="red")

    # Ajouter une annotation au-dessus de la ligne rouge
    fig.add_annotation(
        x=client_value,  # Position en x correspondant à la ligne rouge
        y=max_y_value,  # Position en y au-dessus du graphique (fréquence maximale)
        text=f"<b>Client :  {client_id}</b>",  # Texte de l'annotation
        showarrow=False,  # Pas de flèche
        yshift=10,  # Décalage vers le haut
        font=dict(size=14, color="black"),  # Style du texte
        xanchor="center"  # Centrer le texte au-dessus de la ligne
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

# 2. Analyse bi-variée entre deux caractéristiques sélectionnées

st.subheader("➡️ Visualisation croisée de 2 caractéristiques et mise en évidence de la probabilité de défaut")

# Sélecteurs pour choisir les deux caractéristiques à comparer
feature_x = st.selectbox("Choisissez la première caractéristique", clients_dashboard_modif.columns)
feature_y = st.selectbox("Choisissez la seconde caractéristique", clients_dashboard_modif.columns)

st.markdown(f"<h6 style='font-weight:bold;'> Croisement des variables {feature_x} et {feature_y} en fonction de la probabilité de défaut des clients </h6>", unsafe_allow_html=True)

# Récupérer les valeurs pour le client
client_x_value = clients_dashboard_modif.loc[clients_dashboard_modif['client_id'] == client_id, feature_x].values[0]
client_y_value = clients_dashboard_modif.loc[clients_dashboard_modif['client_id'] == client_id, feature_y].values[0]

# Vérifier si les valeurs sont manquantes
if np.isnan(client_x_value) or np.isnan(client_y_value):
    st.warning(f"Les données pour le client {client_id} sont manquantes pour au moins une des caractéristiques sélectionnées.")
    
    # Créer le graphique sans le point du client
    fig, ax = plt.subplots()
    scatter = ax.scatter(clients_dashboard_modif[feature_x], clients_dashboard_modif[feature_y], 
                         c=clients_dashboard_modif['proba_defaut'], cmap='viridis')
    
    # Ajout de la barre de couleur et labels
    cbar = plt.colorbar(scatter, ax=ax, label='Probabilité de défaut de paiement (seuil=0.5)')
    cbar.ax.tick_params(labelsize=8)  # Modifier la taille de police des ticks de la colorbar
    cbar.set_label('Probabilité de défaut de paiement (seuil=0.5)', fontsize=8)  # Taille de la police du label
    ax.set_xlabel(f'Variable {feature_x}', fontsize=8)  # Taille de police réduite pour les étiquettes
    ax.set_ylabel(f'Variable {feature_y}', fontsize=8)  # Taille de police réduite pour les étiquettes
    ax.tick_params(axis='both', which='major', labelsize=6)  # Taille de police réduite pour les valeurs des axes
    ax.legend(fontsize=8)  # Taille de police réduite pour la légende
    
else:
    # Créer le graphique avec le point du client
    fig, ax = plt.subplots()
    scatter = ax.scatter(clients_dashboard_modif[feature_x], clients_dashboard_modif[feature_y], 
                         c=clients_dashboard_modif['proba_defaut'], cmap='viridis')

    # Ajouter le point correspondant aux caractéristiques du client en rouge
    ax.scatter(client_x_value, client_y_value, color='red', s=100, label=f"Client {client_id}", edgecolor='black')

    # Ajout de la barre de couleur et labels
    cbar = plt.colorbar(scatter, ax=ax, label='Probabilité de défaut de paiement (seuil=0.5)')
    cbar.ax.tick_params(labelsize=8)  # Modifier la taille de police des ticks de la colorbar
    cbar.set_label('Probabilité de défaut de paiement (seuil=0.5)', fontsize=8)  # Taille de la police du label
    ax.set_xlabel(f'Variable {feature_x}', fontsize=8)  # Taille de police réduite pour les étiquettes
    ax.set_ylabel(f'Variable {feature_y}', fontsize=8)  # Taille de police réduite pour les étiquettes
    ax.tick_params(axis='both', which='major', labelsize=6)  # Taille de police réduite pour les valeurs des axes
    ax.legend(fontsize=8)  # Taille de police réduite pour la légende

# Afficher le graphique dans Streamlit
st.pyplot(fig)



