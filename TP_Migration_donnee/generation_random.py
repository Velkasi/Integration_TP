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
            "name" : fake.name(),
            "email" : fake.email(),
            "date_recrut" : fake.date(),
            "salaire_annuel" : round(random.uniform(10000 ,80000),2),
            "salarie_active" : random.choice([True,False]),
        })
    return pd.DataFrame(data)

# Creation du dataframe
df = generate_clients(1000)

# dataframe to csv (index = false) permet de venir écrasé le csv précédent
df.to_csv("employees.csv", index=False)
print("Fichier clients généré")