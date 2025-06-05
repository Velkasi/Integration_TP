# validate.py — Validation post-migration de clevity_db

import pymysql
import pandas as pd
from datetime import datetime

# Connexion à la base de données clevity_db
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    port=3307,
    database="clevity_db",
    autocommit=True
)
cursor = connection.cursor()

# Chargement des données sources (CSV) pour comparaison post-migration
df_clients = pd.read_csv("data_1/client_agence.csv")
df_intervenants = pd.read_csv("data_1/intervenant.csv")
df_projets = pd.read_csv("data_1/projets.csv")
df_affectations = pd.read_csv("data_1/affectations.csv")

# Création du fichier de rapport horodaté
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
report_filename = f"rapport_validation_{timestamp}.txt"

with open(report_filename, "w", encoding="utf-8") as report:
    report.write("Rapport de validation post-migration\n")
    report.write(f"Horodatage : {datetime.now()}\n\n")

    # 1. CONTRÔLE DES VOLUMES
    report.write("[1] Contrôle des volumes\n")
    for table_name, df in [("client_agence", df_clients), ("intervenant", df_intervenants), ("projets", df_projets), ("affectations", df_affectations)]:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count_db = cursor.fetchone()[0]
        count_csv = len(df)
        result = "OK" if count_db == count_csv else "ERREUR"
        report.write(f"- {table_name} : {count_db} en BDD / {count_csv} attendus => {result}\n")

    report.write("\n")

    # 2. CONTRAINTES D'UNICITÉ
    report.write("[2] Contraintes d'unicité\n")
    for table, col in [("intervenant", "id_intervenant"), ("projets", "id_projet"), ("client_agence", "ID")]:
        cursor.execute(f"SELECT COUNT(DISTINCT {col}) FROM {table}")
        unique_count = cursor.fetchone()[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        total_count = cursor.fetchone()[0]
        result = "OK" if unique_count == total_count else "DOUBLONS"
        report.write(f"- {table}.{col} : {unique_count} uniques / {total_count} total => {result}\n")

    report.write("\n")

    # 3. CONTRAINTES DE NON NULLITÉ
    report.write("[3] Contraintes de non nullité\n")
    checks = {
        "client_agence": ["NomClient", "EmailContact", "DateInscription", "Region"],
        "intervenant": ["id_intervenant", "nom", "prenom", "email", "agence", "telephone"],
        "projets": ["id_projet", "nom_projet", "id_client", "date_debut", "status"],
        "affectations": ["id_affectation", "id_projet", "id_intervenant", "date_affectation"]
    }
    for table, columns in checks.items():
        for col in columns:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
            null_count = cursor.fetchone()[0]
            result = "OK" if null_count == 0 else f"{null_count} NULLS"
            report.write(f"- {table}.{col} : {result}\n")

    report.write("\n")

    # 4. CONTRAINTES DE COHÉRENCE INTER-TABLES
    report.write("[4] Contraintes de cohérence inter-tables\n")

    # Vérifier que projets.id_client existe dans client_agence
    cursor.execute("""
        SELECT COUNT(*) FROM projets p
        LEFT JOIN client_agence c ON p.id_client = c.ID
        WHERE c.ID IS NULL
    """)
    invalid_clients = cursor.fetchone()[0]
    result = "OK" if invalid_clients == 0 else f"{invalid_clients} incohérences"
    report.write(f"- projets.id_client -> client_agence.ID : {result}\n")

    # Vérifier que affectations.id_projet existe dans projets
    cursor.execute("""
        SELECT COUNT(*) FROM affectations a
        LEFT JOIN projets p ON a.id_projet = p.id_projet
        WHERE p.id_projet IS NULL
    """)
    invalid_proj = cursor.fetchone()[0]
    result = "OK" if invalid_proj == 0 else f"{invalid_proj} incohérences"
    report.write(f"- affectations.id_projet -> projets.id_projet : {result}\n")

    # Vérifier que affectations.id_intervenant existe dans intervenant
    cursor.execute("""
        SELECT COUNT(*) FROM affectations a
        LEFT JOIN intervenant i ON a.id_intervenant = i.id_intervenant
        WHERE i.id_intervenant IS NULL
    """)
    invalid_interv = cursor.fetchone()[0]
    result = "OK" if invalid_interv == 0 else f"{invalid_interv} incohérences"
    report.write(f"- affectations.id_intervenant -> intervenant.id_intervenant : {result}\n")

    # Fin du rapport
    report.write("\nFin du rapport de validation.")

# Fermer les connexions
cursor.close()
connection.close()

# Console
print(f"Rapport de validation généré : {report_filename}")
