from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Percorso di EdgeDriver
edge_service = Service("C:/Users/nicol/Desktop/Studi/Ironhack/Module1_project/Scraping_immobiliare/edgedriver_win64/msedgedriver.exe")

# Impostazioni del browser (Edge)
edge_options = Options()
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--log-level=3")
edge_options.add_argument("--disable-extensions")
edge_options.add_argument("--disable-software-rasterizer")
edge_options.add_argument("--disable-webgl")

# Inizializza il driver di Selenium per Edge
driver = webdriver.Edge(service=edge_service, options=edge_options)

# URL della pagina principale da cui raccogliere dati
url = "https://www.immobiliare.it/vendita-case/milano/porta-romana-cadore-montenero/"
driver.get(url)

# Accetta il banner dei cookie se presente
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
    )
    cookie_button.click()
    print("Banner dei cookie accettato.")
except Exception as e:
    print("Errore nel clic sul banner dei cookie:", e)

# Itera attraverso i primi annunci (esempio con i primi 5)
for i in range(5):
    try:
        # Ricarica la pagina principale per evitare che gli elementi diventino stantii
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.in-listingCardTitle.is-spaced")))

        # Pausa per evitare di sovraccaricare il server
        time.sleep(2)

        # Trova nuovamente tutti i link degli annunci
        annunci = driver.find_elements(By.CSS_SELECTOR, "a.in-listingCardTitle.is-spaced")
        
        # Controlla se ci sono abbastanza annunci nella lista
        if i >= len(annunci):
            print("Indice dell'annuncio fuori dal range, interrompo il ciclo.")
            break

        link = annunci[i].get_attribute('href')
        print(f"Link annuncio {i+1}: {link}")
        
        # Naviga verso il link dell'annuncio
        driver.get(link)
        
        # Pausa per permettere il caricamento completo della pagina
        time.sleep(3)

        # Estrazione del prezzo
        try:
            price_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".re-overview__price"))
            )
            price_text = price_div.text.strip().replace("€", "").replace(".", "").strip()
            if "-" in price_text:
                print("Annuncio escluso perché il prezzo è un intervallo")
                continue
            print(f"Prezzo: {price_text}")
        except Exception as e:
            print("Errore nell'estrazione del prezzo:", e)
            continue

        # Estrazione della superficie
        try:
            surface_dt = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//dt[text()='Superficie']/following-sibling::dd"))
            )
            surface_text = surface_dt.text.strip().replace("m²", "").strip()
            print(f"Superficie: {surface_text} m²")
        except Exception as e:
            print("Errore nell'estrazione della superficie:", e)
            continue

        # Estrazione del numero di locali
        try:
            locali = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//dt[text()='Locali']/following-sibling::dd"))
            )
            locali_num = int(locali.text.strip())
            print(f"Locali: {locali_num}")
        except Exception as e:
            print("Errore nell'estrazione dei locali:", e)
            locali_num = 0

        # Estrazione del numero di bagni
        try:
            bagni = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//dt[text()='Bagni']/following-sibling::dd"))
            )
            bagni_num = int(bagni.text.strip())
            print(f"Bagni: {bagni_num}")
        except Exception as e:
            print("Errore nell'estrazione dei bagni:", e)
            bagni_num = 0

        # Calcolo del numero totale di stanze
        total_rooms = locali_num + bagni_num
        print(f"Numero totale di stanze: {total_rooms}")

        # Scorri fino al pulsante per vedere tutte le caratteristiche e assicurati che sia visibile e cliccabile
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".re-primaryFeatures__openDialogButton"))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)  # Pausa per assicurarsi che l'elemento sia visibile

            # Prova diversi metodi per cliccare il pulsante
            try:
                button.click()
                print("Pulsante 'Vedi tutte le caratteristiche' cliccato.")
            except Exception:
                driver.execute_script("arguments[0].click();", button)
                print("Pulsante cliccato tramite JavaScript.")
            
            # Estrarre l'anno di costruzione
            try:
                year_built = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//dt[text()='Anno di costruzione']/following-sibling::dd"))
                )
                year_built_text = year_built.text.strip()
                print(f"Anno di costruzione: {year_built_text}")
            except Exception as e:
                print("Errore nell'estrazione dell'anno di costruzione:", e)

        except Exception as e:
            print("Errore nel clic sul pulsante delle caratteristiche:", e)
            continue

        # Pausa per evitare sovraccarico di richieste
        time.sleep(2)

    except Exception as e:
        print(f"Errore nell'estrazione dei dati: {e}")
        continue

    print("-" * 40)

# Chiudi il browser alla fine del processo
driver.quit()
