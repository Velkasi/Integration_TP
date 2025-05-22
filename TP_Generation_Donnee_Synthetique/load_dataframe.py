import pandas as pandas
import pymysql

# Charge le fichier CSV dans un DataFrame
df = pandas.read_csv("suppliers.csv")

# Connexion à la BDD
conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="supplier_integration_test",
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
        INSERT INTO suppliers (supplier_name, contact_email, registration_date, country, reputation_score, is_active)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (row["supplier_name"], row["contact_email"], row["registration_date"], row["country"], row["reputation_score"], bool(row["is_active"])))

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
        SELECT COUNT(*) FROM suppliers
        WHERE contact_email REGEXP '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{3,}$'
        AND contact_email IS NOT NULL;
        """)
    cursor_error_mail = cursor.fetchone()[0]
    print(f'{cursor_error_mail} problème mail')
email_error()

def doublon_error():
    cursor.execute("""
        SELECT COUNT(*) FROM suppliers
        WHERE supplier_name 
        GROUP BY supplier_name
        HAVING count > 1;
        """)
    cursor_error_doublon = cursor.fetchone()[0]
    print(f'{cursor_error_doublon} problème doublon')
doublon_error()

#cursor.execute("""
    #SELECT COUNT(*) FROM suppliers
    #WHERE reputation_score < 0 ;
#""")

# Fermer la connexion à la BDD
cursor.close()
conn.close()