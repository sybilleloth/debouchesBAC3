#vérifier l'état du fichier utilisateur
import sqlite3
import pandas as pd


print("édition des données pour chacune des tables users et logs")
# Connexion à la base de données
conn = sqlite3.connect('project.db')
cursor = conn.cursor()

# Récupération de la liste des tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Parcours des tables et affichage des données sous forme de DataFrame
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    
    # Lire la table dans un DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    
    # Afficher le DataFrame
    print(df)
    print("\n")

# Fermeture de la connexion
#conn.close()




#infos completes

print("édition des données globales")
# Chemin vers la base de données
db_path = 'project.db'

# Reconnexion à la base de données
conn = sqlite3.connect(db_path)

# Charger les données des utilisateurs
users_df = pd.read_sql_query("SELECT uid, email, password FROM users", conn)

# Charger les logs pour les connexions
logs_df = pd.read_sql_query("SELECT uid, action, value FROM logs WHERE action = 'logged'", conn)

# Compter le nombre de connexions par utilisateur
connection_count_df = logs_df.groupby('uid').size().reset_index(name='num_connections')

# Extraire le dernier état de connexion pour chaque utilisateur en sachant que la dernière entrée dans les logs correspond à l'état actuel)
latest_connection_df = logs_df.groupby('uid').tail(1)[['uid', 'value']].rename(columns={'value': 'is_connected'})

# Fusionner les informations sur les utilisateurs avec le nombre de connexions et l'état de connexion actuel
final_df = pd.merge(users_df, connection_count_df, on='uid', how='left')
final_df = pd.merge(final_df, latest_connection_df, on='uid', how='left')

# Opérer sur une copie des colonnes
num_connections_copy = final_df['num_connections'].copy().fillna(0)
is_connected_copy = final_df['is_connected'].copy().fillna('disconnected')

# Assigner les copies modifiées aux colonnes originales
final_df['num_connections'] = num_connections_copy
final_df['is_connected'] = is_connected_copy

# Fermer la connexion
conn.close()

# Afficher le DataFrame final
print(final_df)


#execute : python check_directory.py
