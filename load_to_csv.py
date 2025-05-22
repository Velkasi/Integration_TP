import pandas as pandas
import pymysql

# Charge le fichier CSV dans un DataFrame
df = pandas.read_csv("customer.csv")

# Connexion à la BDD
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="integration_test",
    port=3307,
    autocommit=True
)

# Crée un curseur -> objet python qui permet de dialoguer avec une bdd
#try :
cursor = conn.cursor()
#except :
    #("Erreur de connexion du curseur")

# Mapper et insérer les données dans la BDD
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO customers (name, email, birthdate, total_amount, enabled)
        VALUES (%s, %s, %s, %s, %s)
    """, (row["nom"], row["email"], row["date_naissance"], row["montant"], bool(row["actif"])))

print("Données insérées dans la base")

# Fermer la connexion à la BDD
cursor.close()
conn.close()