import requests
from bs4 import BeautifulSoup

# Fonction pour suivre les liens et scraper les détails
def scrape_details(base_url, links):
    for link in links:
        full_url = base_url + link
        response = requests.get(full_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Exemple de récupération d'informations détaillées
            details = soup.find('div', class_='details').text
            print(f"Details: {details}")
            # Mettre à jour les insertions dans DuckDB
            # ...

if __name__ == "__main__":
    # Exemple de liens à suivre
    links = ['/event1', '/event2']
    scrape_details("https://www.bordeaux-tourisme.com", links)
