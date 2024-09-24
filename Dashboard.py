# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:19:29 2024

@author: druar

Content : création d'un dashboard interactif streamlit à destination des chargés 
de relation client pour expliquer les décisions d’octroi de crédit 
"""

import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="👋",
)

st.write("# 📋 Dashboard de prédiction de score de crédit")

st.sidebar.success("Naviguez dans les sections du dashboard.")

st.markdown(
    """
    Un outil de “scoring crédit” a récement été mis en place pour calculer la probabilité qu’un client rembourse son crédit, 
    et classifier la demande en crédit accordé ou refusé. 
    
    Ce dashboard interactif vous permet de visualiser les informations et les caractéristiques d'un client, de prédire
    sa probabilité de défaut de paiement et de savoir si son crédit est accepté au vu de cette probabilité.
    
    Il vous donnera tous les élémnents nécessaires pour expliquer de façon la plus transparente possible aux clients 
    les décisions d’octroi de crédit.
    """
)







