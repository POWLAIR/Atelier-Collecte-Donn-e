import requests
from bs4 import BeautifulSoup

# URL de la page à scraper
url = "https://www.bordeaux-tourisme.com/agenda"

# Remplacez 'bordeaux-tourisme.com' par 'tourisme.example' dans les données
def replace_domain(data):
    return data.replace('bordeaux-tourisme.com', 'tourisme.example')

# Fonction pour scraper la page
def scrape_agenda():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Exemple de récupération d'informations
        events = soup.find_all('div', class_='event')
        for event in events:
            title = event.find('h2').text
            date = event.find('span', class_='date').text
            print(f"Event: {title}, Date: {date}")
            # Remplacer le domaine
            title = replace_domain(title)
            # Stocker les données dans DuckDB
            # ...

if __name__ == "__main__":
    scrape_agenda()
