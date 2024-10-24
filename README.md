# Atelier 1 - Sources d'un modèle prédictif de trafic

## Étape 1 - Périmètre d'analyse

Voici une liste des facteurs influençant le trafic routier de la rocade bordelaise, classés par ordre décroissant d'importance :

1. Heure de la journée (heures de pointe)
2. Jour de la semaine (jours ouvrables vs week-end)
3. Conditions météorologiques (pluie, neige, brouillard)
4. Vacances scolaires et jours fériés
5. Événements spéciaux (concerts, matchs de football, festivals)
6. Travaux routiers et fermetures de voies
7. Accidents et incidents de circulation
8. Flux touristique saisonnier
9. Grèves et mouvements sociaux affectant les transports en commun
10. Prix du carburant
11. Qualité de l'air et restrictions de circulation
12. Développement urbain et changements démographiques

## Étape 2 - Sources de données

### Données de trafic en temps réel :

- **Source** : Bordeaux Métropole Open Data
- **URL** : [ci_trafi_l](https://opendata.bordeaux-metropole.fr/explore/dataset/ci_trafi_l/)
- **Caractéristiques** : Gratuit, mise à jour en temps réel
- **Remarque** : Nécessite une API pour l'ingestion en continu

### Données métorologiques :

- **Source** : Météo-France
- **URL** : [Météo-France](https://donneespubliques.meteofrance.fr/)
- **Caractéristiques** : Gratuit pour les données publiques, API payante pour les données en temps réel
- **Remarque** : Nécessite un traitement pour extraire les données pertinentes pour Bordeaux

### Calendrier des vacances scolaires et jours fériés :

- **Source** : data.gouv.fr
- **URL** : [Calendrier scolaire de la zone A](https://www.data.gouv.fr/fr/datasets/calendrier-scolaire-de-la-zone-a/)
- **Caractéristiques** : Gratuit, mise à jour annuelle
- **Remarque** : Nécessite un simple traitement pour extraire les dates pertinentes

### Événements spéciaux :

- **Source** : Open Agenda de Bordeaux Métropole
- **URL** : [Open Agenda](https://openagenda.com/bordeaux-metropole)
- **Caractéristiques** : Gratuit, mais nécessite un scraping ou l'utilisation de leur API

### Travaux routiers :

- **Source** : Bordeaux Métropole
- **URL** : [Infos-travaux](https://sedeplacer.bordeaux-metropole.fr/Infos-travaux)
- **Caractéristiques** : Gratuit, mais nécessite un scraping régulier du site web

### Données sur les accidents :

- **Source** : data.gouv.fr (Base de données des accidents corporels de la circulation)
- **URL** : [Base de données accidents corporels](https://www.data.gouv.fr/fr/datasets/base-de-donnees-accidents-corporels-de-la-circulation/)
- **Caractéristiques** : Gratuit, mise à jour annuelle
- **Remarque** : Nécessite un traitement pour extraire les données spécifiques à la rocade bordelaise

### Données touristiques :

- **Source** : Observatoire du tourisme de la Gironde
- **URL** : [Observatoire du tourisme](https://www.gironde-tourisme.fr/espace-pro/observatoire/)
- **Caractéristiques** : Gratuit, mais nécessite un traitement manuel des rapports PDF

### Prix du carburant :

- **Source** : data.gouv.fr (Prix des carburants en France)
- **URL** : [Prix des carburants en France](https://www.data.gouv.fr/fr/datasets/prix-des-carburants-en-france/)
- **Caractéristiques** : Gratuit, mise à jour quotidienne
- **Remarque** : Nécessite un traitement pour extraire les données spécifiques à Bordeaux

### Qualité de l'air :

- **Source** : ATMO Nouvelle-Aquitaine
- **URL** : [ATMO Nouvelle-Aquitaine](https://www.atmo-nouvelleaquitaine.org/donnees/telecharger)
- **Caractéristiques** : Gratuit, mais nécessite une inscription
- **Remarque** : Nécessite un traitement pour extraire les données pertinentes pour la zone de la rocade

## Étape 3 - Ingestion dans un Datalake

#### Installation de DuckDB

Pour commencer, installez le module `duckdb` en utilisant `pip`. Assurez-vous que votre environnement Python est activé, puis exécutez la commande suivante :

```bash
pip install duckdb
```

#### Ouvrir une connexion persistante à DuckDB

```python
conn = duckdb.connect('data/rocade_bordeaux.duckdb')
```

#### Charger les données à partir d'un fichier CSV

```python
def ingest_data(file_path, table_name):
conn.execute(f"""
CREATE OR REPLACE TABLE {table_name} AS
SELECT FROM read_csv_auto('{file_path}', normalize_names=True)
""")
print(f"Data from {file_path} ingested into {table_name}")
```

#### Exemple d'utilisation

```python
ingest_data('path/to/your/file.csv', 'nom_table')

```

## Atelier 2 - Collecte en ligne (scraping)

### Étape 1 - Aspect légal

Lors de la collecte de données en ligne via le scraping, il est crucial de respecter certaines limites pour minimiser le risque de poursuites juridiques. Voici les mesures que nous nous imposons :

1. **Respect du fichier `robots.txt`** : Avant de scraper un site, nous vérifions le fichier `robots.txt` pour comprendre quelles parties du site sont autorisées ou interdites au scraping.

2. **Conditions d'utilisation** : Nous lisons et respectons les conditions d'utilisation du site web pour nous assurer que le scraping est autorisé.

3. **Fréquence des requêtes** : Nous limitons la fréquence des requêtes pour éviter de surcharger le serveur du site web. Cela inclut l'utilisation de délais entre les requêtes pour réduire la charge.

4. **Identification correcte** : Nous utilisons un `User-Agent` approprié dans nos requêtes HTTP pour nous identifier correctement et éviter d'être bloqués par le site.

5. **Utilisation éthique des données** : Nous nous engageons à utiliser les données collectées de manière éthique, en respectant les droits d'auteur et en évitant de redistribuer les données sans autorisation.

6. **Consentement explicite** : Si nécessaire, nous contactons les administrateurs du site pour obtenir une autorisation explicite de scraper leurs données.

En suivant ces directives, nous nous efforçons de mener nos activités de scraping de manière responsable et légale.

### Étape 2 - Structure du projet

Pour organiser efficacement notre projet, nous avons structuré les répertoires et fichiers de la manière suivante :

1. **Dépôt GitHub** :

   - Un dépôt GitHub a été créé pour héberger le projet, facilitant ainsi la gestion de version et la collaboration.

2. **Organisation des Répertoires** :

- `scripts/` : Ce répertoire contient tous les scripts nécessaires pour le projet, y compris les scripts de scraping, d'ingestion, et d'exécution principale.
  - `main.py` : Script principal pour orchestrer l'exécution des autres scripts.
  - `scrape_agenda.py` : Script pour récupérer des informations de l'agenda.
  - `scrape_details.py` : Script pour explorer les liens et obtenir des informations détaillées.
  - `duckdb-A1_E3.py` : Script pour l'ingestion de données dans DuckDB.
- `config/` : Contient les fichiers de configuration nécessaires pour l'installation des outils et la gestion des dépendances.
  - `requirements.txt` : Liste des dépendances Python nécessaires pour le projet.
  - `data/` : Répertoire cible pour le fichier de base de données DuckDB, où les données persistentes sont stockées.

3. **Procédure de Configuration de l'Environnement de Développement** :
   - **Cloner le Dépôt** : Commencez par cloner le dépôt GitHub sur votre machine locale.
     ```bash
     git clone <url_du_dépôt>
     cd <nom_du_dépôt>
     ```
   - **Installer les Dépendances** : Utilisez `pip` pour installer toutes les dépendances listées dans `requirements.txt`.
     ```bash
     pip install -r config/requirements.txt
     ```
   - **Configurer les Fichiers de Configuration** : Assurez-vous que tous les fichiers de configuration nécessaires sont correctement configurés dans le répertoire `config/`.
   - **Exécuter les Scripts** : Utilisez le script `main.py` pour exécuter l'ensemble des scripts dans l'ordre approprié.
     ```bash
     python scripts/main.py
     ```

### Étape 3 - Récupération d'une liste

Pour enrichir notre jeu de données avec des informations touristiques, nous avons développé un script qui récupère des informations à partir d'une liste d'événements sur le site de Bordeaux Tourisme. Voici les étapes suivies pour réaliser cette tâche :

1. **Scraping des Données** :

   - Nous avons utilisé le module `requests` pour envoyer des requêtes HTTP au site web et `BeautifulSoup` pour analyser le contenu HTML de la page.
   - Le script `scrape_agenda.py` est conçu pour extraire un maximum d'informations pertinentes, telles que le titre de l'événement, la date, et la description.

2. **Remplacement du Domaine** :

   - Avant de stocker les données, nous remplaçons toutes les occurrences de `bordeaux-tourisme.com` par `tourisme.example` pour anonymiser les données.

3. **Stockage dans DuckDB** :

   - Les données extraites sont ensuite stockées dans une table de la base de données DuckDB, qui a été initialisée lors du premier atelier.
   - Nous utilisons la fonction `to_sql` de Pandas pour insérer les données dans DuckDB.

4. **Exécution du Script** :
   - Le script `scrape_agenda.py` peut être exécuté via le script principal `main.py`, qui orchestre l'exécution de tous les scripts du projet.

### Étape 4 - Exploration de lien

Pour obtenir des informations plus détaillées sur chaque événement listé, nous avons développé un script qui suit les liens de la liste initiale et extrait des données supplémentaires. Voici les étapes suivies pour réaliser cette tâche :

1. **Suivi des Liens** :

   - Le script `scrape_details.py` utilise `requests` pour suivre les liens individuels des événements extraits lors de l'étape précédente.
   - `BeautifulSoup` est utilisé pour analyser le contenu HTML des pages de détails et extraire des informations supplémentaires telles que l'emplacement, les horaires, et les descriptions détaillées.

2. **Mise à Jour des Insertion-s** :

   - Les nouvelles informations collectées sont utilisées pour mettre à jour les enregistrements existants dans la base de données DuckDB.
   - Nous utilisons des requêtes SQL pour insérer ou mettre à jour les données dans la table appropriée.

3. **Exécution du Script** :
   - Le script `scrape_details.py` est intégré dans le flux de travail global et peut être exécuté via le script principal `main.py`.

## Atelier 3 - Préparation des données

### Étape 1 - Isolation des données brutes

Pour organiser et préparer efficacement les données pour l'analyse, nous avons créé un schéma dédié dans notre base de données DuckDB pour stocker les données brutes. Cela permet de séparer les données non transformées des données transformées et analysées, facilitant ainsi la gestion et la traçabilité des données.

1. **Création du Schéma** :

   - Nous avons utilisé la commande SQL `CREATE SCHEMA IF NOT EXISTS raw;` pour créer un schéma nommé `raw`. Ce schéma est destiné à contenir toutes les données brutes importées dans DuckDB.

2. **Avantages de l'Isolation des Données Brutes** :

   - **Organisation** : En isolant les données brutes, nous pouvons mieux organiser notre base de données et éviter la confusion entre les données brutes et les données transformées.
   - **Traçabilité** : Cela facilite le suivi des transformations appliquées aux données, car les données brutes restent inchangées dans le schéma `raw`.
   - **Sécurité** : En gardant les données brutes séparées, nous réduisons le risque de modifications accidentelles qui pourraient affecter l'intégrité des données d'origine.

3. **Exécution de la Commande** :
   - La commande SQL pour créer le schéma peut être exécutée directement dans un script Python en utilisant la connexion DuckDB, comme illustré ci-dessous :

### Étape 2 - Initialisation du projet dbt

Pour transformer et modéliser nos données efficacement, nous avons initialisé un projet dbt (Data Build Tool) dans notre répertoire de projet. Voici les étapes suivies pour configurer dbt :

1. **Initialisation du Projet dbt** :

   - Nous avons utilisé la commande `dbt init <nom_du_projet>` pour créer un nouveau projet dbt. Cette commande génère la structure de base du projet, y compris les répertoires et fichiers nécessaires pour commencer à travailler avec dbt.

2. **Configuration de `profiles.yml`** :
   - Le fichier `profiles.yml` est utilisé pour configurer la connexion à la base de données. Il doit être placé dans le répertoire `~/.dbt/` de votre système. Voici un exemple de configuration pour DuckDB :

### Étape 3 - Modèles

Dans cette étape, nous avons créé des modèles "bronze" et "silver" pour transformer et enrichir nos données. Voici les étapes suivies :

1. **Création des Modèles "Bronze"** :

   - Les modèles "bronze" sont des transformations initiales appliquées aux données brutes pour les nettoyer et les préparer pour une analyse plus approfondie.
   - Nous avons créé un modèle "bronze" pour chaque table du schéma `raw`. Voici un exemple de modèle "bronze" pour la table `agenda_events` :

```sql
-- models/bronze/bronze_agenda_events.sql
{{ config(
materialized='table'
) }}
SELECT
,
LOWER(title) AS title_lowercase
FROM
{{ source('raw', 'agenda_events') }}
```

2. **Création des Modèles "Silver"** :
   - Les modèles "silver" intègrent des transformations plus complexes, y compris des jointures entre différentes tables.
   - Nous avons créé un modèle "silver" qui joint les données de `agenda_events` avec une autre table, par exemple `event_details` :

```sql
-- models/silver/silver_event_details.sql
{{ config(
materialized='table'
) }}
SELECT
ae.,
ed.location,
ed.time
FROM
{{ ref('bronze_agenda_events') }} ae
JOIN
{{ ref('bronze_event_details') }} ed
ON
```

3. **Configuration des Tests** :
   - Nous avons configuré des tests pour vérifier l'existence et l'unicité des clés primaires dans les modèles "silver". Voici un exemple de configuration dans `silver/models.yml` :

```yaml
models/bronze/models.yml
version: 2
models:
name: silver_event_details
description: "Détails enrichis des événements"
columns:
name: event_id
tests:
not_null
unique
```

4. **Vérification et Exécution** :
   - Nous avons utilisé les commandes `dbt build` et `dbt run` pour vérifier et exécuter nos transformations, assurant ainsi que les modèles fonctionnent correctement.

```bash
dbt build
dbt run
```

5. **Versionnement de l'Étape** :
   - Après avoir configuré et testé les modèles, nous avons utilisé Git pour versionner cette étape, enregistrant ainsi les changements apportés aux modèles dbt.

```bash
git add .
git commit -m "Création des modèles bronze et silver avec tests"
```

En suivant ces étapes, nous avons structuré et enrichi nos données pour une analyse plus approfondie.

### Étape 4 - Documentation

Pour assurer une bonne compréhension et traçabilité de nos transformations de données, nous avons documenté nos sources et modèles dans dbt. Voici les étapes suivies :

1. **Renseigner les Descriptions** :
   - Nous avons ajouté des descriptions détaillées pour chaque source et modèle dans les fichiers YAML de dbt. Cela inclut des informations sur l'origine des données, les transformations appliquées, et l'objectif de chaque modèle.

```yaml
models/silver/models.yml
version: 2
models:
name: silver_event_details
description: "Détails enrichis des événements, incluant l'emplacement et l'heure"
columns:
name: event_id
description: "Identifiant unique de l'événement"
tests:
not_null
unique
name: location
description: "Emplacement de l'événement"
name: time
description: "Heure de l'événement"
```

2. **Génération de la Documentation** :
   - Nous avons utilisé la commande `dbt docs build` pour générer la documentation statique de notre projet dbt. Cette documentation inclut des informations sur toutes les sources, modèles, et tests configurés.

```bash
dbt docs build
```

3. **Visualisation de la Documentation** :
   - Pour visualiser la documentation générée, nous avons utilisé la commande `dbt docs serve`, qui lance un serveur web local permettant de naviguer dans la documentation via un navigateur.

```bash
dbt docs serve
```

4. **Versionnement de l'Étape** :
   - Après avoir documenté et généré la documentation, nous avons utilisé Git pour versionner cette étape, enregistrant ainsi les descriptions et configurations ajoutées.

```bash
git add .
git commit -m "Documentation et tests ajoutés"
```
