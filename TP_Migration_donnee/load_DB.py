import pymysql


# Connexion a la BDD
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    port=3307,
    database="integration_test",
    autocommit=True
)

# Creation du curseur
cursor = connection.cursor()

#Initialiser le fichier de journalisation
log_file = ini_log_file()

# Traitement ligne par ligne du CSV
for _, row in df.iterrows():
    logging_generation.total_rows += 1

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
            row["date_naissance"], # Date de naissance
            row["montant"], # Montant total
            bool(row["actif"]))) # conversion explicit en booleen

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
    SELECT COUNT(*) FROM customers
    WHERE birthdate > CURDATE();
""")
future_birthdates = cursor.fetchone()[0]
print(f"{future_birthdates} clients ont une date de naissance future")

# Fermeture fichier log


# Generation du rapport final
close_log_file(log_file)


# Fermeture du cursor et de la connexion a la base
cursor.close()
connection.close()
