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

### Données météorologiques :
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
