import pymysql
import pandas as pandas

from TP_Migration_donnee import logging_gen
from TP_Migration_donnee.generation_random import df
from TP_Migration_donnee.logging_gen import log_insert_success, ini_log_file, log_ignored_row, log_error, close_log_file

# Connexion a la BDD
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    port=3307,
    database="company_db",
    autocommit=True
)

# Creation du curseur
cursor = connection.cursor()

#Initialiser le fichier de journalisation
log_file = ini_log_file()

# Traitement ligne par ligne du CSV
for _, row in df.iterrows():
    logging_gen.total_rows += 1

    try :
######################### AVANT MIGRATION #########################

# Verifier les donnees inssentielles de la base initiales avec insertion
# Si un champ obligatoire est manquant, on le consigne dans les logs
        if pandas.isnull(row['email']):
            log_ignored_row(log_file, row, 'required field email is missing')
            continue

# Insertion les donnees dans la table
        cursor.execute("""
            INSERT INTO customers (name, email, birthdate, total_amount, enabled)
            VALUES (%s, %s, %s, %s, %s)
            """, (
            row["nom"], #Nom client
            row["email"], # Email client
            row["date_recrut"], # Date de naissance
            row["salaire_annuel"], # Montant total
            bool(row["salaire_active"]))) # conversion explicit en booleen

######################### PENDANT MIGRATION #########################
# Si insertion reussie : Log l'evenement
        log_insert_success(log_file, row)


# Si erreur : Log erreur
    except Exception as e:
        log_error(log_file, row, str(e))

######################### APRES MIGRATION #########################

# Verification du fichier
# Verification s'il y a des dates futures (incorrectes)

cursor.execute("""
    SELECT COUNT(*) FROM employees
    WHERE date_recrut > CURDATE();
""")
future_birthdates = cursor.fetchone()[0]
print(f"{future_birthdates} clients ont une date de naissance future")

#Vérifier que l'email est bien formaté.
cursor.execute("""
    SELECT email
    FROM employees
    WHERE email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.(com|fr|org|net|edu|gov|biz|info)$'
""")
invalid_emails = cursor.fetchall()
print("Emails invalides:", invalid_emails)

#Vérifier que tous les champs sont remplis.


#Vérifier que le salaire est positif.
cursor.execute("""
    SELECT salaire_annuel, COUNT(*) 
    FROM employees
    WHERE salaire_annuel > 0 
    AND salaire_annuel < 100000 
    GROUP BY salaire_annuel ;
""")
cursor_error_reputation = cursor.fetchall()
print(f'{cursor_error_reputation} salaire annuel Superieur a 0')

# Fermeture fichier log


# Generation du rapport final
close_log_file(log_file)


# Fermeture du cursor et de la connexion a la base
cursor.close()
connection.close()
