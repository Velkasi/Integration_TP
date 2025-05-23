import datetime
import pandas as pandas
import pymysql

# Dataframe a partir du CSV
df=pandas.read_csv('customer.csv')

# Connexion BDD
connection = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    port=3307,
    database="integration_test",
    autocommit=True
)

# Cration du cursor
cursor = connection.cursor()

#Initialiser le fichier de journalisation
def ini_log_file():
    #On donne un nom au fichier contenant date et heure
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'log_{timestamp}'

    #Ouvrir le fichier en mode ecriture
    log_file = open(filename, "w", encoding="utf-8")

    #En-tete
    log_file.write("Log de migration de donnees \n")
    log_file.write(f'Date : {datetime.datetime.now()}')

    return log_file

# Traitement ligne par ligne du CSV

######################### AVANT MIGRATION #########################


# Verifier les donnees inssentielles de la base initiales avec insertion
# Si un champ obligatoire est manquant, on le consigne dans les logs


# Insertion les donnees dans la table

######################### PENDANT MIGRATION #########################


# Si insertion reussie : Log l'evenement


# Si erreur : Log erreur

######################### APRES MIGRATION #########################

# Verification du fichier


# Fermeture fichier log


# Generation du rapport final


# Fermeture du cursor et de la connexion a la base


# Message de fin dans le terminal


# Generation du rapport