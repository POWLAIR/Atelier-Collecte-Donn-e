import mysql.connector
from mysql.connector import errorcode
import requests
from io import StringIO
import pandas as pd

# Informations de connexion
config = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}

# Connexion au serveur MySQL
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Création de la base de données si elle n'existe pas
    cursor.execute("CREATE DATABASE IF NOT EXISTS rocade_bordeaux")
    print("Base de données 'rocade_bordeaux' vérifiée/créée.")
    conn.database = 'rocade_bordeaux'

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Erreur de connexion : nom d'utilisateur ou mot de passe incorrect.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("La base de données n'existe pas et ne peut pas être créée.")
    else:
        print(err)
    exit(1)

# Fonction pour télécharger et charger les données CSV
def load_csv_data(url, table_name):
    response = requests.get(url)
    if response.status_code == 200:
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Données chargées dans la table {table_name}")
    else:
        print(f"Erreur lors du téléchargement des données pour {table_name}")

# Chargement des données de trafic
trafic_url = "https://opendata.bordeaux-metropole.fr/explore/dataset/ci_trafi_l/download/?format=csv"
load_csv_data(trafic_url, "trafic_data")

# Chargement des données météorologiques (exemple avec des données publiques de Météo-France)
meteo_url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/synop.2023.csv.gz"
load_csv_data(meteo_url, "meteo_data")

# Chargement des données sur les accidents
accidents_url = "https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405"
load_csv_data(accidents_url, "accidents_data")

# Fermeture de la connexion
cursor.close()
conn.close()

print("Chargement des données terminé.")
