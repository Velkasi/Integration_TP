import random
import pandas as pd
from faker import Faker

fake = Faker('fr_FR')

# Fonction pour créer les clients
def generate_clients(nb):
    # Declaration d'un tableau vide
    data= []
    # Boucle for
    for _ in range(nb):
        # Ajout des nom, mails etc...
        data.append({
            "supplier_name" : fake.name(),
            "contact_email" : fake.email(),
            "registration_date" : fake.date_time(),
            "country" : fake.country(),
            "reputation_score" : round(random.uniform(0,100)),
            "is_active" : random.choice([True,False]),
        })
    return pd.DataFrame(data)

# Creation du dataframe
df = generate_clients(1000)

# dataframe to csv (index = false) permet de venir écrasé le csv précédent
df.to_csv("suppliers.csv", index=False)
print("Fichier clients généré")