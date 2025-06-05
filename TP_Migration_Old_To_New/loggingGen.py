import datetime
# Variable globales de suivi

total_rows = 0
inserted_count = 0
ignored_count = 0
error_count = 0
error_rows = []


# Initialiser le fichier de log
def ini_log_file():
    #On donne un nom au fichier contenant date et heure
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'log_{timestamp}'

    #Ouvrir le fichier en mode ecriture
    log_file = open(filename, "w", encoding="utf-8")

    #En-tete
    log_file.write("Log de migration de donnees \n")
    log_file.write(f'Date : {datetime.datetime.now()}\n')

    return log_file


def log_insert_success(log_file, row):
    global inserted_count
    inserted_count += 1
    log_file.write(f"Inserted : {row['major_code']}\n")

# Consigner une insertion reussie
def log_ignored_row(log_file, row, reason):
    global ignored_count
    ignored_count += 1
    log_file.write(f'Ignored : {row.get('major_code', 'N/A')} | Reason : {reason}\n')

# Consigner une ligne ignoree
def log_error(log_file, row, error_msg):
    global error_count
    error_count += 1

# Consigner une erreur major_code, registration_date, status, student_id
    error_rows.append({
        "major_code" : row.get("major_code, N/A"),
        "registration_date" : row.get("registration_date, N/A"),
        "status" : row.get("status"),
        "student_id" : row.get("student_id"),
        "error" : error_msg
    })

    log_file.write(f'Error: {row.get('major_code', 'N/A')} | Reason : {error_msg}\n')

# Generer un rapport de migration
def generate_summary_report():
    filename = "resume_migration_enrollments.txt"

    with open(filename, "w", encoding="utf-8") as report:
        report.write("Rapport de migration\n")
        report.write(f'Total de ligne traitées : {total_rows}\n')
        report.write(f'Insertion reussies : {inserted_count}\n')
        report.write(f'Lignes ignorees : {ignored_count}\n')
        report.write(f"Erreurs : {error_count}\n\n")

        #Detail des erreurs
        if error_rows:
            report.write("Detail des erreurs : \n")
            for error in error_rows:
                report.write(f'Email: {error['email']} Erreur: {error['error']}\n')
        else :
            report.write("Aucune erreur detectee")
        report.close()

# Fermer proprement le fichier log et generer le rapport final
def close_log_file(log_file):
    log_file.write('\nFin du journal')
    log_file.close()
    generate_summary_report()