# Projet ETL - TP CI/CD sur Windows

Ce dpt contient plusieurs TPs visant apprendre l'automatisation des traitements de donnes (ETL) avec
génération, chargement et journalisation, intégrés dans un pipeline CI/CD via GitHub Actions.
---

## Pré-requis pour exécuter les projets sur un serveur **Windows**

### Outils obligatoires

- Python 3.10
- MySQL Server (ex. XAMPP avec port 3306 ou 3307)
- Git (pour cloner le dpt)
- PowerShell ou terminal compatible
- Un diteur de texte/code (Visual Studio Code recommand)
- 
### Modules Python ncessaires

 installer avec pip :
 
```bash
pip install pandas pymysql faker

```
---
## Configuration MySQL (exemple)
1. Démarrer MySQL avec un utilisateur `root` et mot de passe vide **ou** `"root"`.
2. Modifier les fichiers Python si besoin :
   
```python
# Exemple dans load_dataframe.py
conn = pymysql.connect(
 host="127.0.0.1",
 user="root",
 password="root", # ou vide selon config
 port=3306,
 database="nom_de_la_base",
 autocommit=True
)
```
3. Exécuter les fichiers `.sql` pour créer les bases et tables :
   
```bash
mysql -u root -p < TP_Generation_Donnee_Synthetique/suppliers.sql
```
---
## Lancement manuel d'un TP

### Exemple : TP_Generation_Donnee_Synthetique

```bash
python TP_Generation_Donnee_Synthetique/data_sup.py
python TP_Generation_Donnee_Synthetique/load_dataframe.py
```
---
## Exécution automatique (CI/CD)

1. Le fichier `.github/workflows/etl.yml` excute l'ETL via GitHub Actions.
2. Il est déclenché chaque `push` sur la branche principale.
3. Pour tester un TP automatiquement, adapter les chemins dans `etl.yml`.
---
## Astuce

Crer un fichier `.env` ou utiliser des variables d'environnement Windows pour scuriser les mots de passe.
---
## Besoin d'aide ?

Crer une issue ou envoyer un message l'auteur du dpt
