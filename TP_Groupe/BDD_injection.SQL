CREATE DATABASE IF NOT EXISTS clevity_db;
USE clevity_db;

DROP TABLE IF EXISTS client_agence;

# ID,NomClient,DateInscription,EmailContact,Commentaire + ClientID,Raison Sociale,email,Inscrit_le,Region
CREATE TABLE IF NOT EXISTS client_agence (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    NomClient VARCHAR (100),
    EmailContact VARCHAR (100),
    DateInscription DATETIME,
    Commentaire VARCHAR (200),
    Region VARCHAR (100)
);

# id_affectation,id_projet,id_intervenant,date_affectation,role,commentaire
CREATE TABLE IF NOT EXISTS affectations (
    id_affectation INT AUTO_INCREMENT PRIMARY KEY,
    id_projet VARCHAR (100),
    id_intervenant VARCHAR (100),
    date_affectation DATETIME,
    role VARCHAR (100),
    commentaire VARCHAR (200)
);

# id_intervenant,nom,prenom,email,agence,telephone
CREATE TABLE IF NOT EXISTS intervenant (
    id_intervenant INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR (100),
    prenom VARCHAR (100),
    agence VARCHAR (100),
    email VARCHAR (100),
    telephone VARCHAR (100)
);


#id_projet,nom_projet,id_client,date_debut,date_fin,statut,note_satisfaction
CREATE TABLE IF NOT EXISTS projets (
    id_projet INT AUTO_INCREMENT PRIMARY KEY,
    nom_projet VARCHAR (100),
    id_client INT,
    date_debut DATETIME,
    date_fin DATETIME,
    status BOOLEAN,
    note_satisfaction INT
);