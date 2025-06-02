import pandas as pandas
import pymysql

# Charge le fichier CSV dans un DataFrame
df = pandas.read_csv("TP_Generation_Donnee_Synthetique/suppliers.csv")

# Connexion à la BDD
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="supplier_integration_test",
    port=3307,
    autocommit=True
)

# Crée un curseur -> objet python qui permet de dialoguer avec une bdd
#try :
cursor = conn.cursor()
#except :
    #("Erreur de connexion du curseur")
inserted = 0

# Mapper et insérer les données dans la BDD
for _, row in df.iterrows(): #Boucle for (similaire a for each du au _ qui enlève la premiere ligne)
    try:
        cursor.execute("""
            INSERT INTO suppliers (supplier_name, contact_email, registration_date, country, reputation_score, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (row["supplier_name"], row["contact_email"], row["registration_date"], row["country"], row["reputation_score"], bool(row["is_active"])))
        inserted += 1
        print(f'{inserted} lignes enregistrés')
    except Exception as e: #Enregistre les erreurs Try / Catch(except)
        print(e)
print("Données insérées dans la base")


# Verification s'il y a des dates futures (incorrectes)

def registration_error():
    cursor.execute("""
        SELECT COUNT(*) FROM suppliers
        WHERE registration_date > CURDATE();
        """)
    cursor_error_registration = cursor.fetchone()[0]
    print(f'{cursor_error_registration} Dates future')
registration_error()

def email_error():
    cursor.execute("""
        SELECT contact_email
        FROM suppliers
        WHERE contact_email NOT REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.(com|fr|org|net|edu|gov|biz|info)$'
    """)
    invalid_emails = cursor.fetchall()
    print("Emails invalides:", invalid_emails)
email_error()

def doublon_error():
    cursor.execute("""
        SELECT supplier_name, COUNT(*)
        FROM suppliers
        GROUP BY supplier_name
        HAVING COUNT(*) > 1;
        """)
    cursor_error_double = cursor.fetchall()
    for supplier_name in cursor_error_double:
        print(f"{supplier_name} aparait plusieurs fois.")
doublon_error()

def reputation_error():
    cursor.execute("""
        SELECT reputation_score, COUNT(*) 
        FROM suppliers
        WHERE reputation_score > 50 
        AND reputation_score < 100 ;
        """)
    cursor_error_reputation = cursor.fetchone()[0]
    print(f'{cursor_error_reputation} reputation entre 50 et 100')
reputation_error()

# Fermer la connexion à la BDD
cursor.close()
conn.close()
