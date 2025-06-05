from datetime import datetime

import pandas as pd
import pymysql

from TP_Migration_Old_To_New import loggingGen
from TP_Migration_Old_To_New.loggingGen import ini_log_file, log_ignored_row, log_insert_success, log_error, \
    close_log_file

# Connexion a la BDD
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    port=3307,
    database="university",
    autocommit=True
)

# Creation du curseur
cursor = connection.cursor()

# Lecture du fichier CSV
dataframeEnrollments = pd.read_csv("TD reprise de données/jeux de données et bdd/enrollments.csv")
dataframeMajors = pd.read_csv("TD reprise de données/jeux de données et bdd/majors.csv")
dataframeStudents = pd.read_csv("TD reprise de données/jeux de données et bdd/students.csv")

# Initialiser le fichier de journalisation
log_file = ini_log_file()

for _, row in dataframeMajors.iterrows():
    loggingGen.total_rows += 1

    try:
        # Vérifier que tous les champs sont remplis
        if pd.isnull(row['major_code']) or pd.isnull(row['major_name']):
            log_ignored_row(log_file, row, 'Champs obligatoires manquants')
            continue

        # Insérer les données dans la table majors
        cursor.execute("""
            INSERT INTO majors (major_code, major_name)
            VALUES (%s, %s)
            """, (
            row["major_code"],
            row["major_name"]))

        log_insert_success(log_file, row)

    except Exception as e:
        log_error(log_file, row, str(e))

for _, row in dataframeStudents.iterrows():
    loggingGen.total_rows += 1

    try:
        # Vérifier que tous les champs sont remplis
        if pd.isnull(row['student_id']) or pd.isnull(row['full_name']) or pd.isnull(row['birth_date']) or pd.isnull(row['email']) or pd.isnull(row['nationality']):
            log_ignored_row(log_file, row, "Champs obligatoires manquants")
            continue

        # Vérifier si la date de naissance est valide
        if pd.to_datetime(row["birth_date"]) > datetime.now():
            log_ignored_row(log_file, row, "Date de naissance invalide")
            continue

        # Insérer les données dans la table students
        cursor.execute("""
            INSERT INTO students (student_id, full_name, birth_date, email, nationality)
            VALUES (%s, %s, %s, %s, %s)
            """, (
            row["student_id"],
            row["full_name"],
            row["birth_date"],
            row["email"],
            row["nationality"]))

        log_insert_success(log_file, row)

    except Exception as e:
        log_error(log_file, row, str(e))

# Traitement ligne par ligne du CSV dataframeEnrollments
for _, row in dataframeEnrollments.iterrows():
    loggingGen.total_rows += 1

    try:
        ######################### AVANT MIGRATION #########################

        # Verifier les donnees essentielles de la base initiales avec insertion
        # Si un champ obligatoire est manquant, on le consigne dans les logs

        # Vérifier que tous les champs sont remplis.
        if pd.isnull(row['major_code']) or pd.isnull(row['registration_date']) or pd.isnull(row['status']) or pd.isnull(
                row['student_id']):
            log_ignored_row(log_file, row, 'Champs obligatoires manquants')
            continue
        # Verification s'il y a des dates futures (incorrectes)

        if pd.to_datetime(row["registration_date"]) > datetime.now():
            log_ignored_row(log_file, row, "Date de recrutement future")
            continue
        #-----------------------------------------------------------------------
        # -----------------------------------------------------------------------
        # Insertion les donnees dans la table enrollments
        cursor.execute("""
            INSERT INTO enrollments (major_code, registration_date, status, student_id)
            VALUES (%s, %s, %s, %s)
            """, (
            row["major_code"],  # Code Majeur
            row["registration_date"],  # Date d'enregistrement
            row["status"],  # Status
            row["student_id"]))  # ID student

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