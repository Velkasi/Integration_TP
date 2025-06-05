import pandas as pandas
import pymysql

#Appeller les fichiers CSV générées
df_intervenant = pandas.read_csv('"Cas 1/Cas 1"/data_1/intervenants.csv')
df_client_agence = pandas.read_csv('"Cas 1/Cas 1"/data_1/clients_agence.csv')
df_projet = pandas.read_csv('"Cas 1/Cas 1"/data_1/projets.csv')
df_affectation = pandas.read_csv('"Cas 1/Cas 1"/data_1/affectations.csv')

#Connexion à la BDD
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="clevity_db",
    port=3307,
    autocommit=True
)

#Créer un curseur => objet python qui permet de dialoguer avec une BDD
cursor = conn.cursor()

inserted_lien = 0

#Mapper et insérer les données dans la BDD
for _, row in df_intervenant.iterrows():
    try:
        cursor.execute("""
            INSERT INTO intervenant (nom, prenom, agence, email, telephone)
            VALUES (%s, %s, %s, %s, %s)           
        """, (row["nom"], row["prenom"], row["agence"], row["email"], row["telephone"]))
        inserted_lien += 1
    except Exception as e:
        print(e)
print("Données insérées dans la table intervenant")

for _, row in df_client_agence.iterrows():
    try:
        cursor.execute("""
            INSERT INTO suppliers (NomClient, EmailContact, DateInscription, Commentaire, Region)
            VALUES (%s, %s, %s, %s, %s)           
        """, (row["NomClient"], row["EmailContact"], row["DateInscription"], row["Commentaire"], row["Region"]))
        inserted_lien += 1
    except Exception as e:
        print(e)
print("Données insérées dans la table agence")

for _, row in df_projet.iterrows():
    try:
        cursor.execute("""
            INSERT INTO suppliers (nom_projet, date_debut, date_fin, statut, note_satisfaction)
            VALUES (%s, %s, %s, %s, %s, %s)           
        """, (row["nom_projet"], row["date_debut"], row["date_fin"], bool(row["statut"]), row["note_satisfaction"]))
        inserted_lien += 1
    except Exception as e:
        print(e)
print("Données insérées dans la table projet")

for _, row in df_affectation.iterrows():
    try:
        cursor.execute("""
            INSERT INTO suppliers (date_affectation, role, commentaire)
            VALUES (%s, %s, %s, %s, %s, %s)           
        """, (row["date_affectation"], row["role"], row["commentaire"]))
        inserted_lien += 1
    except Exception as e:
        print(e)
print("Données insérées dans la table affectation")

#Fermer la connexion à la BDD
cursor.close()
conn.close()