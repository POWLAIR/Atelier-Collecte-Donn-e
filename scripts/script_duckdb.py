import mysql.connector
from mysql.connector import errorcode
import requests
from io import StringIO
import pandas as pd
import duckdb
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Informations de connexion
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rocade_bordeaux'
}

# URLs des données
trafic_url = "https://opendata.bordeaux-metropole.fr/explore/dataset/ci_trafi_l/download/?format=csv"
meteo_url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/synop.2023.csv.gz"
accidents_url = "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405"

# Fonction pour supprimer et recréer la base de données
def reset_database():
    try:
        conn = mysql.connector.connect(host=config['host'], user=config['user'], password=config['password'])
        cursor = conn.cursor()

        # Supprimer la base de données si elle existe
        cursor.execute(f"DROP DATABASE IF EXISTS {config['database']}")
        
        # Créer la base de données
        cursor.execute(f"CREATE DATABASE {config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Base de données '{config['database']}' réinitialisée.")

    except mysql.connector.Error as err:
        print(f"Erreur lors de la réinitialisation de la base de données : {err}")
        exit(1)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Réinitialiser la base de données
reset_database()

# Créer le moteur SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{config['user']}:{config['password']}@{config['host']}/{config['database']}?charset=utf8mb4")

# Connexion persistante à DuckDB
duckdb_conn = duckdb.connect('data/rocade_bordeaux.duckdb')

# Fonction pour télécharger et charger les données CSV
def load_csv_data(url, table_name):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            csv_data = StringIO(response.content.decode('utf-8'))
        except UnicodeDecodeError:
            csv_data = StringIO(response.content.decode('latin-1'))
        
        df = pd.read_csv(csv_data, on_bad_lines='skip', sep=';')
        
        # Nettoyer et raccourcir les noms de colonnes
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df.columns = [col[:63] if len(col) > 63 else col for col in df.columns]
        
        try:
            # Diviser le DataFrame en morceaux plus petits
            chunk_size = 1000
            for i in range(0, len(df), chunk_size):
                chunk = df[i:i+chunk_size]
                with engine.begin() as connection:
                    chunk.to_sql(table_name, connection, if_exists='append' if i > 0 else 'replace', index=False)
            print(f"Données chargées dans la table {table_name}")
        except SQLAlchemyError as e:
            print(f"Erreur lors du chargement des données dans {table_name}: {str(e)}")
    else:
        print(f"Erreur lors du téléchargement des données pour {table_name}")

# Chargement des données
try:
    load_csv_data(trafic_url, "trafic_data")
    load_csv_data(meteo_url, "meteo_data")
    load_csv_data(accidents_url, "accidents_data")
except Exception as e:
    print(f"Une erreur est survenue lors du chargement des données : {str(e)}")

# Fonction pour réinitialiser DuckDB
def reset_duckdb():
    duckdb_conn.execute("DROP TABLE IF EXISTS trafic_data")
    duckdb_conn.execute("DROP TABLE IF EXISTS meteo_data")
    duckdb_conn.execute("DROP TABLE IF EXISTS accidents_data")
    print("Tables DuckDB réinitialisées.")

# Réinitialiser DuckDB
reset_duckdb()

# Ingestion des données dans DuckDB
def ingest_data(table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        duckdb_conn.register(f'df_{table_name}', df)
        duckdb_conn.execute(f"""
        CREATE TABLE {table_name} AS
        SELECT * FROM df_{table_name}
        """)
        print(f"Données de {table_name} ingérées dans DuckDB")
    except Exception as e:
        print(f"Erreur lors de l'ingestion des données de {table_name} dans DuckDB: {str(e)}")

# Ingérer les données dans DuckDB
ingest_data("trafic_data")
ingest_data("meteo_data")
ingest_data("accidents_data")

# Fermeture des connexions
engine.dispose()
duckdb_conn.close()

print("Chargement des données terminé.")
