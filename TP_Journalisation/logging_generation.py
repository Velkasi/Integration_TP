# Variable globales de suivi

total_rows = 0
inserted_count = 0
ignored_count = 0
error_count = 0
error_rows = []


# Initialiser le fichier de log
def log_insert_success(log_file, row):
    global inserted_count
    inserted_count += 1
    log_file.write("Inserted : {row['email']}\n")

# Consigner une insertion reussie
def log_ignored_row(log_file, row, reason):
    global ignored_count
    ignored_count += 1
    log_file.write(f'Ignored : {row.get('email', 'N/A')} | Reason : {reason}\n')

# Consigner une ligne ignoree
def log_error(log_file, row, error_msg):
    global error_count
    error_count += 1

# Consigner une erreur
    error_rows.append({
        "email" : row.get("email, N/A"),
        "error" : error_msg
    })

    log_file.write(f'Error: {row.get('email', 'N/A')} | Reason : {error_msg}')

# Generer un rapport de migration


# Fermer proprement le fichier log et generer le rapport final