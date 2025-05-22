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
            "nom" : fake.name(),
            "email" : fake.email(),
            "date_naissance" : fake.date_of_birth(minimum_age=18, maximum_age=90),
            "montant" : round(random.uniform(0 ,1000),2),
            "actif" : random.choice([True,False]),
        })
    return pd.DataFrame(data)

# Creation du dataframe
df = generate_clients(1000)

# dataframe to csv (index = false) permet de venir écrasé le csv précédent
df.to_csv("customer.csv", index=False)
print("Fichier clients généré")