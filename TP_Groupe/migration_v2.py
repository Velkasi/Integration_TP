import pandas as pandas
import pymysql

#Appeller les fichiers CSV générées
df_intervenant = pandas.read_csv('"Cas 1/Cas 1"/data_1/intervenants.csv')
df_agence = pandas.read_csv('"Cas 1/Cas 1"/data_1/agence.csv')
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
try:
    with conn.cursor() as cursor:
        intervenant_insert = """
            INSERT INTO intervenant (nom, prenom, agence, email, telephone)
            VALUES (%s, %s, %s, %s, %s)           
        """
        cursor.executemany(intervenant_insert, df_intervenant.values.tolist())
        
        agence_insert = """
            INSERT INTO client_agence (NomClient, EmailContact, DateInscription, Commentaire, Region)
            VALUES (%s, %s, %s, %s, %s)           
        """
        cursor.executemany(agence_insert, df_agence.values.tolist())
        
        projet_insert = """
            INSERT INTO projet (nom_projet, date_debut, date_fin, statut, note_satisfaction)
            VALUES (%s, %s, %s, %s, %s)           
        """
        cursor.executemany(projet_insert, df_projet.values.tolist())
        
        affectation_insert = """
            INSERT INTO affectation (date_affectation, role, commentaire)
            VALUES (%s, %s, %s)           
        """
        cursor.executemany(affectation_insert, df_affectation.values.tolist())
        
    conn.commit()
    print("Données insérées dans la base.")

except Exception as e:
    conn.rollback()
    print("Erreur lors du chargement de la donée : ", e)

finally:
    conn.close()
