import pandas as pd


# Chargement des fichiers contenant les données erronées et les référentiels valides
df_intervenant = pd.read_csv('intervenants.csv')         # Données des intervenants
df_client_agence1 = pd.read_csv('clients_agence1.csv')   # Référentiel des clients de l'agence 1
df_client_agence2 = pd.read_csv('clients_agence2.csv')  # Référentiel des clients de l'agence 2
df_projet = pd.read_csv('projets.csv')  # Référentiel des projets
df_affectation = pd.read_csv('affectations.csv')   # Référentiel des affectations

###################### Concatener les deux csv clients###########################
# Colonne agence 1 : ID,NomClient,DateInscription,EmailContact,Commentaire
# Colonne agence 2 : ClientID,Raison Sociale,email,Inscrit_le,Region

##################################Suppression de l'ID###########################
#####Agence 1##########
df_client_agence1 = df_client_agence1.drop(columns=['ID']) #Suppression de l'ID car re-création par la BDD
df_client_agence1['Region'] = None# Colonne "Region" ajoutée
df_client_agence1 = df_client_agence1[['NomClient', 'DateInscription', 'EmailContact', 'Region', 'Commentaire']]

#####Agence 2##########
df_client_agence2 = df_client_agence2.drop(columns=['ClientID']) #Suppression de l'ID car re-création par la BDD
df_client_agence2 = df_client_agence2.rename(columns={'Raison Sociale': 'NomClient','Inscrit_le': 'DateInscription', 'email': 'EmailContact'}) # Renomme les colonnes

df_client_agence2['Commentaire'] = None # Colonne ajoutée : Raison Sociale,"email","Inscrit_le",Region,"Commentaire"

##Colonne finale pour les agences : NomClient,DateInscription,EmailContact,Region,Commentaire

# Fusion des deux jeux de donnée---
df_clients = pd.concat([df_client_agence1, df_client_agence2], ignore_index=True)

#####Ecriture du fichiers
df_clients.to_csv ("agence.csv", index=False)
