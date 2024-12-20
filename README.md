# Créer une API de scoring crédit et réaliser un DashBoard interactif - DASHBOARD

Vous trouverez la partie modèle de scoring dans ce repertoire : https://github.com/CathyTreg/Modele_scoring

Contexte : L’entreprise « Prêt à dépenser » souhaite déployer un outil de scoring crédit pour estimer la probabilité qu’un client rembourse son crédit, en s’appuyant sur un modèle prédictif et un suivi en temps réel.

Objectif : Mettre en place un modèle de prédiction des risques de défaut de paiement du client. Intégrer ce modèle via une API pour une utilisation dans un système de scoring en production. Déployer un dashboard interactif pour l’analyse des clients.

Tâches :
-	Développement du modèle de scoring :
o	Créer un modèle de régression logistique pour prédire la probabilité de défaut de paiement des clients ;
o	Implémenter un suivi de la performance du modèle via la surveillance du Data Drift avec Evidently et l'utilisation de SHAP pour expliciter les décisions du modèle ;
-	Mise en production avec une API :
o	Développer une API REST avec Flask permettant de recevoir des données, et de renvoyer des prédictions de scoring ;
o	Déployer l'API en continu avec GitHub Actions via Azure WebApp pour garantir la mise à jour automatique du modèle en production ;
o	Créer des tests unitaires pour assurer la qualité et la stabilité du code via une exécution automatisée lors du déploiement ;
-	Développement d’un Dashboard Interactif :
o	Concevoir un dashboard interactif avec Streamlit permettant aux chargés d’études de visualiser la probabilité de solvabilité d’un client et d’interpréter les résultats du scoring en temps réel ;
o	Mettre en place une interface utilisateur facilitant la compréhension des décisions du modèle grâce à des visualisations et des explications détaillées des prédictions.

Résultats : 
-	Évaluation en temps réel de la solvabilité des clients, fournissant des informations précises, et expliquées à un chargé d’études, ce qui améliore la prise de décision dans l'octroi de crédits ;
-	Grâce à l'intégration d'une approche MLOps, le modèle est facilement évolutif et peut être régulièrement mis à jour pour s'adapter aux nouvelles tendances et comportements clients.

Environnement de travail :
-	Outils de Développement : Jupyter Notebook, Python (via Anaconda), GitHub Actions
-	Outils de Machine Learning : scikit-learn, MLflow UI, Evidently (data drift), SHAP, SMOTE
-	Outils de déploiement et visualisation : Flask pour l'API, Azure WebApp, Streamlit pour le dashboard interactif, unittest pour les tests automatisés.

Lien Streamlit (la web app n'est plus active) : https://p8dashboard-iahha89fm7h6syqqkwvetu.streamlit.app/

![image](https://github.com/user-attachments/assets/b6c14d52-8e5c-49c9-8bb3-2828a78d455e)
