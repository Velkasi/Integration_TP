import pandas as pd

import datetime

# Chargement des fichiers contenant les données erronées et les référentiels valides
df_intervenant = pd.read_csv('"Cas 1/Cas 1"/data_1/intervenants.csv')         # Données des intervenants
df_client_agence1 = pd.read_csv('"Cas 1/Cas 1"/data_1/clients_agence1.csv')   # Référentiel des clients de l'agence 1
df_client_agence2 = pd.read_csv('"Cas 1/Cas 1"/data_1/clients_agence2.csv')  # Référentiel des clients de l'agence 2
df_projet = pd.read_csv('"Cas 1/Cas 1"/data_1/projets.csv')  # Référentiel des projets  
df_affectation = pd.read_csv('"Cas 1/Cas 1"/data_1/affectations.csv')   # Référentiel des affectations

# Concatener les deux csv clients 

























##########################################################################################################################################################







#
# Conversion des dates de naissance ; les formats invalides deviennent NaT
df_students['birth_date'] = pd.to_datetime(df_students['birth_date'], errors='coerce')

# Suppression des lignes dont la date de naissance est invalide (NaT)
df_students = df_students.dropna(subset=['birth_date'])

# Suppression des doublons : même nom + même email → on garde l'entrée la plus récente (par student_id décroissant)
df_students = df_students.sort_values(by='student_id', ascending=False)
df_students = df_students.drop_duplicates(subset=['full_name', 'email'], keep='first')

# Nettoyer Enrollments

# Conversion des dates d'inscription ; suppression des lignes avec dates invalides
df_enrollments['registration_date'] = pd.to_datetime(df_enrollments['registration_date'], errors='coerce')
df_enrollments = df_enrollments.dropna(subset=['registration_date'])

# Filtrage : ne garder que les inscriptions liées à un étudiant existant
valid_student_ids = set(df_students['student_id'])
df_enrollments = df_enrollments[df_enrollments['student_id'].isin(valid_student_ids)]

# Filtrage : ne garder que les major_code présents dans le référentiel
df_enrollments = df_enrollments[df_enrollments['major_code'].isin(valid_majors)]

# Nettoyage des statuts : si le statut n’est pas reconnu, on le remplace par 'pending'
valid_status = {'active', 'cancelled', 'pending'}
df_enrollments['status'] = df_enrollments['status'].apply(lambda x: x if x in valid_status else 'pending')

# Vérification des doubles inscriptions : un étudiant ne peut être inscrit qu'une seule fois dans la même filière
duplicates = df_enrollments[df_enrollments.duplicated(subset=['student_id', 'major_code'], keep=False)]
duplicate_count = len(duplicates)

# Supprimer les doublons (on garde le premier par défaut)
df_enrollments = df_enrollments.drop_duplicates(subset=['student_id', 'major_code'])

# Export des fichiers clean
# Sauvegarde des fichiers nettoyés
df_students.to_csv('students_clean.csv', index=False)
df_enrollments.to_csv('enrollments_clean.csv', index=False)

# --- 6. DATABASE OPERATIONS WITH pymysql ---
# Connexion manuelle à la base MariaDB
conn = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    autocommit=False,
    charset='utf8mb4'
)

try:
    with conn.cursor() as cursor:
        # Suppression des anciennes données erronées
        # Cette suppression est limitée aux student_id valides après nettoyage
        format_ids = ",".join(["%s"] * len(valid_student_ids))
        cursor.execute(f"DELETE FROM enrollments WHERE student_id IN ({format_ids})", tuple(valid_student_ids))
        cursor.execute(f"DELETE FROM students WHERE student_id IN ({format_ids})", tuple(valid_student_ids))


        # Réinsertion des données stucdents corrigées
        student_insert = """
            INSERT INTO students (student_id, full_name, birth_date, email, nationality)
            VALUES (%s, %s, %s, %s, %s)
        """
        student_data = df_students.values.tolist()
        cursor.executemany(student_insert, student_data)

        # Réinjection des inscriptions corrigées
        enrollment_insert = """
            INSERT INTO enrollments (student_id, major_code, registration_date, status)
            VALUES (%s, %s, %s, %s)
        """
        enrollment_data = df_enrollments.values.tolist()
        cursor.executemany(enrollment_insert, enrollment_data)

    # Validation de toutes les opérations d'écriture (si tout s'est bien passé)
    conn.commit()

    # Logging
    # Traçabilité de l’opération de reprise (volumes, timestamp)
    with open('recovery_log.txt', 'w') as log:
        log.write(f"Reinjected {len(df_students)} students and {len(df_enrollments)} enrollments\n")
        log.write(f"Duplicates found and removed: {duplicate_count}\n")

    with open('recovery_report.txt', 'w') as report:
        report.write(f"Recovery operation completed on {datetime.datetime.now()}\n")
        report.write(f"Students inserted: {len(df_students)}\n")
        report.write(f"Enrollments inserted: {len(df_enrollments)}\n")
        report.write(f"Duplication issues found: {duplicate_count}\n")
        report.write("All anomalies have been corrected.\n")

except Exception as e:
    # En cas d'erreur, annulation de toutes les modifications
    conn.rollback()
    print("Error during recovery:", e)

finally:
    # Fermeture de la connexion à la base
    conn.close()
