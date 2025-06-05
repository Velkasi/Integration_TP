import panda as pd
import datetime

# Variable globales de suivi
total_rows = 0
inserted_count = 0
ignored_count =0
null_count = 0
error_count = 0
error_rows = []

# Initialiser le fichier de log
def init_log_file(): #on donne un nom au fichier contenant la date et heure actuelle
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = "log.txt"

    #Ouvrir le fichier en mode écriture
    log_file = open(filename, "w", encoding="utf-8")

    #en-tete
    log_file.write("Logs de migration de données\n")
    log_file.write(f"Date: {datetime.datetime.now()}\n")
    return log_file

# consigner une insertion réussie
def log_insert_success(log_file, row):
    global inserted_count
    inserted_count += 1
    log_file.write(f"Inserted : {row['name']}\n")

############################# Début des logs spécifique #############################
#consigner une ligne ignorée
def log_row_ignored(log_file, row, reason):
   global  ignored_count #appel une valeur existante dans le code, il réassigne donc global est necessaire
   ignored_count += 1
   log_file.write(f"Ignored : {row.get('nom', 'N/A')} {row.get('email', 'N/A')} {row.get('recruitment_date', 'N/A')} {row.get('annual_salary', 'N/A')} {row.get('is active', 'N/A')}| Reason : {reason}\n")

#consigner une erreur
def log_error(log_file, row, error_msg):
    global error_count
    error_count += 1

    # Garder les détails de l'erreur sur mon rapport
    error_rows.append({ # rajoute une ligne dans une ligne existante
        "email": row.get("email, N/A"),
        "error": error_msg
    })

    log_file.write(f"Error: {row.get("email", "N/A")} | reason : {error_msg}\n")

def enter_table(log_file, information):
    log_file.write(f"{information}")

########################################Rapport final########################
#généré un rapport de migration
def generate_summary_report():
    filename = "rapport_reprise.txt"

    with open(filename, "w", encoding="UTF-8") as report: #alias nommé report
        report.write("Rapport de migration\n")
        report.write(f"Total de lignes traitées: {total_rows}\n")
        report.write(f"Insertions réussies: {inserted_count}\n")
        report.write(f"Lignes ignorées : {ignored_count}\n")
        report.write(f"Erreur rencontrées : {error_count}\n")

        #affiche le détail des erreurs
        if error_rows:
            report.write("Détails des erreurs\n")
            for error in error_rows:
                report.write(f"Email:{error['email']} erreur ; {error['error']}\n")
        else :
            report.write("Aucune erreur détectée")

        report.close()

#fermer proprement le fichier log et générer le rapport final
def close_log_file(log_file):
    log_file.write("\n Fin du journal")
    log_file.close()
    generate_summary_report()
