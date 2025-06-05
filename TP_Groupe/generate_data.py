import random
from faker import Faker
import pandas as pandas

fake = Faker('fr_FR')

def generate_clients(nb):
    data =[]
    for _ in range(nb):
        data.append({
            "NomClient" : fake.name(),
            "EmailContact" : fake.unique.email(),
            "DateInscription" : fake.date_between(start_date="-10y", end_date="today"),
            "Commentaire" : fake.sentence(nb_words=10),
            "Region" : fake.country()
        })
    return pandas.DataFrame(data)

df = generate_clients(500)
df.to_csv("clients.csv", index=False)
print("Fichier clients généré")


def generate_intervenants(nb):
    data =[]
    for _ in range(nb):
        data.append({
            "nom" : fake.last_name(),
            "prenom" : fake.first_name(),
            "agence" : fake.city(),
            "email" : fake.unique.email(),
            "telephone" : fake.phone_number()
        })
    return pandas.DataFrame(data)

df = generate_intervenants(500)
df.to_csv("intervenants.csv", index=False)
print("Fichier intervenants généré")


def generate_projets(nb):
    data =[]
    for _ in range(nb):
        data.append({
            "nom_projet" : f"Projet_{fake.word()}_{round(random.randint(1, 500))}",
            "date_debut" : fake.date_between(start_date="-10y", end_date="today"),
            "date_fin" : fake.date_between(start_date="+1d", end_date="+10y"),
            "statut" : random.choice(["En cours", "Terminé"]),
            "note_satisfaction" : round(random.uniform(0, 5), 1) if "statut" == "Terminé" else ""
        })
    return pandas.DataFrame(data)

df = generate_projets(500)
df.to_csv("projets.csv", index=False)
print("Fichier projets généré")


def generate_affectations(nb):
    data =[]
    for _ in range(nb):
        data.append({
            "date_affectation" : fake.date_between(start_date="-10y", end_date="today"),
            "role" : fake.unique.email(),
            "commentaire" : fake.sentence(nb_words=10)
        })
    return pandas.DataFrame(data)

df = generate_affectations(500)
df.to_csv("affectations.csv", index=False)
print("Fichier affectations généré")