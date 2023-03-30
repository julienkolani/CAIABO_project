
-- Pour lancer le script de la BD 
-- sqlite3 ma_base_de_donnees.db < caiabo_memory.sql


CREATE TABLE memoireDeBase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cle TEXT,
    contenu TEXT
);

CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY
);

CREATE TABLE discussions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    utilisateur_id INTEGER,
    heure DATETIME,
    message TEXT,
    reponse TEXT,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
); 


INSERT INTO memoireDeBase ( cle, contenu) VALUES ('cle_de_bot','CAIABO');
INSERT INTO memoireDeBase ( cle, contenu) VALUES ('cle_de_contenu','KOLANI Julien');
INSERT INTO memoireDeBase ( cle, contenu) VALUES ('description_contenu','KOLANI Julien est un étudiant en système et réseaux de l université de lomé');
INSERT INTO memoireDeBase ( cle, contenu) VALUES ('cle_propre','CAIABO');
INSERT INTO memoireDeBase ( cle, contenu) VALUES ('usages','chatbot');
INSERT INTO memoireDeBase ( cle, contenu) VALUES ('information','Je me cleme CAIABO j ai été concu par Julien inspiré de JARVIS de MARVEL');
INSERT INTO memoireDeBase ( cle, contenu) VALUES ('end','Merci');

