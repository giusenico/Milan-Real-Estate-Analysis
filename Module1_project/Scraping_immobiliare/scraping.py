import requests
from bs4 import BeautifulSoup
import time

# URL della pagina principale da cui raccogliere dati
url = "https://www.immobiliare.it/vendita-case/milano/porta-romana-cadore-montenero/"

# Impostazione degli headers per simulare una richiesta da un browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# Effettua la richiesta al sito
response = requests.get(url, headers=headers)

# Verifica lo stato della richiesta e stampa una parte della risposta per controllare l'HTML
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Trova tutti i link degli annunci
    listings = soup.find_all('a', class_='in-listingCardTitle is-spaced')
    print(f"Numero di link trovati: {len(listings)}")  # Debug: stampa quanti link sono stati trovati

    if listings:
        for listing in listings:
            # Estrae il link dell'annuncio
            link = listing.get('href')
            # Completa il link se è relativo
            if not link.startswith("http"):
                link = "https://www.immobiliare.it" + link
            
            print(f"Link annuncio: {link}")
            
            # Effettua una richiesta alla pagina dell'annuncio
            ad_response = requests.get(link, headers=headers)
            if ad_response.status_code == 200:
                ad_soup = BeautifulSoup(ad_response.content, 'html.parser')
                
                # Estrarre il prezzo utilizzando la classe 're-overview__price'
                price_div = ad_soup.find('div', class_='re-overview__price')
                if price_div:
                    price_text = price_div.text.strip().replace("€", "").replace(".", "").strip()
                    print(f"Prezzo: {price_text}")

                # Estrarre la superficie
                surface_dt = ad_soup.find('dt', class_='re-featuresItem__title', string='Superficie')
                if surface_dt:
                    surface_dd = surface_dt.find_next('dd', class_='re-featuresItem__description')
                    if surface_dd:
                        surface_text = surface_dd.text.strip().replace("m²", "").strip()
                        print(f"Superficie: {surface_text} m²")

                # Estrarre il numero di locali
                locali_dt = ad_soup.find('dt', class_='re-featuresItem__title', string='Locali')
                locali_count = 0
                if locali_dt:
                    locali_dd = locali_dt.find_next('dd', class_='re-featuresItem__description')
                    if locali_dd:
                        locali_text = locali_dd.text.strip().split('-')[0].strip()
                        locali_count = int(locali_text)

                # Estrarre il numero di bagni
                bagni_dt = ad_soup.find('dt', class_='re-featuresItem__title', string='Bagni')
                bagni_count = 0
                if bagni_dt:
                    bagni_dd = bagni_dt.find_next('dd', class_='re-featuresItem__description')
                    if bagni_dd:
                        bagni_count = int(bagni_dd.text.strip())

                # Calcola il numero totale di stanze
                total_rooms = locali_count + bagni_count
                print(f"Numero totale di stanze: {total_rooms}")

                # Estrarre l'anno di costruzione
                anno_dt = ad_soup.find('dt', class_='re-primaryFeaturesDialogSection__featureTitle', string='Anno di costruzione')
                if anno_dt:
                    anno_dd = anno_dt.find_next('dd', class_='re-primaryFeaturesDialogSection__featureDescription')
                    if anno_dd:
                        anno_text = anno_dd.text.strip()
                        print(f"Anno di costruzione: {anno_text}")
                
                # Aspetta un attimo per evitare di sovraccaricare il server
                time.sleep(2)
                
            else:
                print(f"Errore nella richiesta della pagina dell'annuncio: {ad_response.status_code}")
            
            # Separatore per chiarezza
            print("-" * 40)
    else:
        print("Nessun link di annuncio trovato. Verifica la struttura HTML della pagina.")
else:
    print(f"Errore nella richiesta: {response.status_code}")
