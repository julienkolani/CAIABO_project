import sqlite3
import datetime

def connect_database():
    """Fonction pour ouvrir une connexion à la base de données"""
    connexion = sqlite3.connect('ma_base_de_donnees.db')
    requette = connexion.cursor()
    return connexion, requette

# Fonction pour créer la table "utilisateurs"
def create_table():
    connexion, requette = connect_database()
    requette.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
                    id INTEGER PRIMARY KEY
                )''')
    connexion.commit()
    connexion.close()

# Fonction pour ajouter un utilisateur
def add_user(id):
    connexion, requette = connect_database()
    requette.execute("INSERT INTO utilisateurs (id) VALUES (?)", (id,))
    connexion.commit()
    connexion.close()

# Fonction pour récupérer un utilisateur par son id
def get_user(id):
    connexion, requette = connect_database() 
    requette.execute("SELECT * FROM utilisateurs WHERE id=?", (id,))
    user = requette.fetchone()
    connexion.close()
    return user

# Fonction pour mettre à jour un utilisateur
def update_user(id, new_id):
    connexion, requette = connect_database() 
    requette.execute("UPDATE utilisateurs SET id=? WHERE id=?", (new_id, id))
    connexion.commit()
    connexion.close()

# Fonction pour supprimer un utilisateur
def delete_user(id):
    connexion, requette = connect_database() 
    requette.execute("DELETE FROM utilisateurs WHERE id=?", (id,))
    connexion.commit()
    connexion.close()
    

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# Fonction pour créer un nouveau message
def create_message(utilisateur_id, heure, message, reponse=None):
    connexion, requette = connect_database()
    requette.execute("INSERT INTO discussions (utilisateur_id, heure, message, reponse) VALUES (?, ?, ?, ?)", (utilisateur_id, heure, message, reponse))
    connexion.commit()
    connexion.close()

# Fonction pour lire tous les messages d'un utilisateur
def read_messages_by_user_id(utilisateur_id):
    connexion, requette = connect_database()
    requette.execute("SELECT * FROM discussions WHERE utilisateur_id=?", (utilisateur_id,))
    rows = requette.fetchall()
    connexion.close()
    return rows


# Fonction pour mettre à jour un message existant
def update_message(id, utilisateur_id=None, heure=None, message=None, reponse=None):
    connexion, requette = connect_database()
    query = "UPDATE discussions SET"
    params = []
    if utilisateur_id:
        query += " utilisateur_id=?,"
        params.append(utilisateur_id)
    if heure:
        query += " heure=?,"
        params.append(heure)
    if message:
        query += " message=?,"
        params.append(message)
    if reponse:
        query += " reponse=?,"
        params.append(reponse)
    query = query.rstrip(',')
    query += " WHERE id=?"
    params.append(id)
    requette.execute(query, params)
    connexion.commit()
    connexion.close()

# Fonction pour supprimer un message
def delete_message(id):
    connexion, requette = connect_database()
    requette.execute("DELETE FROM discussions WHERE id=?", (id,))
    connexion.commit()
    connexion.close()

# Fonction pour récupération d'historique d'un user
def read_history(id):
    connexion, requete = connect_database()
    """Récupère les informations avec l'ID spécifié dans la table."""
  
    requete.execute("SELECT * FROM discussions WHERE utilisateur_id=? ORDER BY heure", (id,))
    rows = requete.fetchall()
    connexion.close()

    print(rows)

    # Créer un dictionnaire avec la clé représentée par la valeur de la colonne "clé"
    # et la valeur représentée par la valeur de la colonne "content" pour chaque ligne
    history = {}
    all_history = []
    for row in rows:
        history["user"] = row[3]
        all_history.append(history)
        history["system"] = row[4]
        all_history.append(history)

    # Retourner le dictionnaire s'il n'est pas vide, sinon None
    return all_history if all_history else None


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def create_memoire( cle, contenu):
    connexion, requette = connect_database()
    """Crée un nouveau tuple dans la table memoireDeBase avec la clé et le contenu spécifiés."""
    
    requette.execute("INSERT INTO memoireDeBase (cle, contenu) VALUES (?, ?)", (cle, contenu))
    connexion.commit()
    connexion.close()

    return requette.lastrowid


def read_memoire( id):
    connexion, requette = connect_database()
    """Récupère le tuple avec l'ID spécifié dans la table memoireDeBase."""
    
    requette.execute("SELECT * FROM memoireDeBase WHERE id=?", (id,))
    row = requette.fetchone()
    connexion.close()
    return row


def update_memoire( id, cle, contenu):
    connexion, requette = connect_database()
    """Met à jour le tuple avec l'ID spécifié dans la table memoireDeBase avec les valeurs de clé et de contenu spécifiées."""
    
    requette.execute("UPDATE memoireDeBase SET cle=?, contenu=? WHERE id=?", (cle, contenu, id))
    connexion.commit()
    connexion.close()

    return requette.rowcount


def delete_memoire( id):
    connexion, requette = connect_database()
    """Supprime le tuple avec l'ID spécifié dans la table memoireDeBase."""
    
    requette.execute("DELETE FROM memoireDeBase WHERE id=?", (id,))
    connexion.commit()
    connexion.close()

    return requette.rowcount

def read_memoire_info():
    connexion, requete = connect_database()
    """Récupère toutes les lignes de la table memoireDeBase."""

    requete.execute("SELECT * FROM memoireDeBase")
    rows = requete.fetchall()
    connexion.close()

    # Créer un dictionnaire avec la clé représentée par la valeur de la colonne "clé"
    # et la valeur représentée par la valeur de la colonne "content" pour chaque ligne
    # de la table memoireDeBase.
    memoire_dict = {}
    for row in rows:
        
        memoire_dict[row[1]] = row[2]

    return memoire_dict
 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def clean_discussions_table():
    connexion, requette = connect_database()
    now = datetime.datetime.now()
    requette.execute("SELECT MIN(heure) FROM discussions")
    result = requette.fetchone()
    if result is not None:
        first_date = datetime.datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        diff = now - first_date
        if diff.total_seconds() >= 86400:
            requette.execute("DELETE FROM discussions")
            connexion.commit()

            print("Table vide.")
        else:
            print("En cours")
    else:
        print("Table vide.")
    connexion.close()

def clean_discussions_now():
    connexion, requette = connect_database()
    requette.execute("DELETE FROM discussions")
    connexion.commit()
    connexion.close()