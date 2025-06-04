from datetime import datetime
import pandas as pd
import pymysql
import re

import logging_gen
from TP_Migration_donnee.logging_gen import log_insert_success, ini_log_file, log_ignored_row, log_error, close_log_file

# Connexion a la BDD
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    port=3307,
    database="company_db",
    autocommit=True
)

# Creation du curseur
cursor = connection.cursor()

#Lecture du fichier CSV
dataframe = pd.read_csv("TP_Migration_donnee/employees.csv")

#Initialiser le fichier de journalisation
log_file = ini_log_file()

# Traitement ligne par ligne du CSV
for _, row in dataframe.iterrows():
    logging_gen.total_rows += 1

    try :
######################### AVANT MIGRATION #########################

# Verifier les donnees inssentielles de la base initiales avec insertion
# Si un champ obligatoire est manquant, on le consigne dans les logs
        
        #Vérifier que tous les champs sont remplis.
        if pd.isnull(row['email']) or pd.isnull(row['name']) or pd.isnull(row['date_recrut']) or pd.isnull(row['salaire_annuel']):
            log_ignored_row(log_file, row, 'Champs obligatoires manquants')
            continue
        # Verification s'il y a des dates futures (incorrectes)

        if pd.to_datetime(row["date_recrut"]) > datetime.now():
            log_ignored_row(log_file, row, "Date de recrutement future")
            continue

        #Vérifier que l'email est bien formaté.
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|fr|org|net|edu|gov|biz|info)$", row["email"]):
            log_ignored_row(log_file, row, "Email mal formaté")
            continue


        #Vérifier que le salaire est positif.
        if float(row["salaire_annuel"]) <= 0:
            log_ignored_row(log_file, row, "Salaire invalide")
            continue


# Insertion les donnees dans la table
        cursor.execute("""
            INSERT INTO employees (name, email, date_recrut, salaire_annuel, salarie_active)
            VALUES (%s, %s, %s, %s, %s)
            """, (
            row["name"], #Nom client
            row["email"], # Email client
            row["date_recrut"], # Date de recrutement
            row["salaire_annuel"], # Salaire annuel
            bool(row["salarie_active"]))) # Salarie en activites en booleen

######################### PENDANT MIGRATION #########################
# Si insertion reussie : Log l'evenement
        log_insert_success(log_file, row)


# Si erreur : Log erreur
    except Exception as e:
        log_error(log_file, row, str(e))

######################### APRES MIGRATION #########################

# Verification du fichier

# Fermeture fichier log
# Generation du rapport final
close_log_file(log_file)


# Fermeture du cursor et de la connexion a la base
cursor.close()
connection.close()
