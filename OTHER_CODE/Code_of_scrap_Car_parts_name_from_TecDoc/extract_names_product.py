from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import sys
import json
def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--lang=en')
    # options.add_argument('--headless')  # Uncomment to run headless
    return options

def login(driver):
    try:
        # Wait for and input the username
        username_field = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.NAME, "identifier"))
        )
        username_field.send_keys("first.choice.auto.parts.ltd@gmail.com")

        # Click the "Next" button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='button button-primary' and @value='Next']"))
        )
        next_button.click()

    except Exception as e:
        handle_error(driver, "Error during login - Username:", e)

    try:
        # Wait for and input the password
        password_field = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.NAME, "credentials.passcode"))
        )
        password_field.send_keys("Fcap2020")

        # Click the "Verify" button
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='button button-primary' and @value='Verify']"))
        )
        verify_button.click()

    except Exception as e:
        handle_error(driver, "Error during login - Password:", e)

    # Handle additional pages that may appear after login
    handle_additional_pages(driver)

def handle_additional_pages(driver):
    try:
        # Close the additional page if it appears
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ta-icon-cancel')]"))
        )
        close_button.click()

    except Exception as e:
        print("Close button not found:", e)

    try:
        # Check for and click on "Continue" button
        additional_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='button button-primary' and @value='Continue']"))
        )
        additional_button.click()
        print("Clicked on 'Continue' button")

    except Exception as e:
        print("Continue button not found:", e)

    try:
        # Check for and click on cancel icon if "Continue" button was not found
        cancel_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='ta-icon-cancel']"))
        )
        cancel_icon.click()
        print("Clicked on cancel icon")

    except Exception as e:
        print("Cancel icon not found:", e)

def search_and_interact(driver):
    try:
        # Maximize the window
        driver.maximize_window()

        # Wait for the search box to be visible after login
        search_box = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='typeNumber']"))
        )


        #search_query = input("Enter your search query: ")
        # Get search query from command line arguments
        search_query = sys.argv[1]

        search_box.send_keys(search_query)

        # Click the search icon
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='ta-icon-search']"))
        )
        search_icon.click()

        # Take a screenshot after login and page load
        screenshot_path = os.path.join(os.getcwd(), 'screenshot.png')
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Click on "All product groups" dropdown
        product_groups_div = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='p-multiselect-label p-placeholder']"))
        )
        product_groups_div.click()

        # Click on the checkbox (adjust the XPath accordingly)
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='checkbox' and @class='p-checkbox-box']"))
        )
        checkbox.click()

        # Scroll to load more elements in the shutdown bar
        scroll_shut_down_bar_and_extract_text(driver, search_query)

        # Extract text from all specified elements
        #extract_text_from_elements(driver)

    except Exception as e:
        handle_error(driver, "Error during search and interaction:", e)


def scroll_shut_down_bar_and_extract_text(driver, search_query):
    try:
        shutdown_bar = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.p-scroller.ng-star-inserted"))
        )

        # Obtenez la hauteur de l'élément de la barre de défilement
        scroll_height = int(shutdown_bar.get_attribute("scrollHeight"))

        # Initialiser un ensemble pour stocker les textes uniques
        unique_texts = set()

        # Faire défiler petit à petit
        step = 100  # Ajustez la taille du défilement ici
        current_scroll = 0
        while current_scroll < scroll_height:
            # Faire défiler la barre de défilement
            driver.execute_script(f"arguments[0].scrollTo(0, {current_scroll});", shutdown_bar)
            time.sleep(0.5)  # Délai pour le défilement

            # Extraire et ajouter les textes uniques à partir des éléments visibles
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[@class='count-item-label ng-star-inserted']"))
            )
            for element in elements:
                unique_texts.add(element.text.strip())

            # Mettre à jour le défilement actuel
            current_scroll += step

        # Atteindre la fin de la barre de défilement
        driver.execute_script(f"arguments[0].scrollTo(0, {scroll_height});", shutdown_bar)
        time.sleep(2)  # Temps d'attente final si nécessaire
        unique_texts_list = list(unique_texts)

        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

        output_dir = os.path.join(desktop_path, 'Car_Parts_TecDoc')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Chemin complet du fichier de sortie
        output_file = os.path.join(output_dir, f"{search_query}.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(unique_texts_list, f, ensure_ascii=False, indent=4)

        print(f"Les éléments uniques ont été enregistrés dans : {output_file}")
        # Afficher le nombre d'éléments uniques
        print(f"Nombre d'éléments uniques : {len(unique_texts)}")
        print("Liste des textes uniques :")
        for text in unique_texts:
            print(text)

    except Exception as e:
        print("Erreur lors du défilement et de l'extraction de texte :", e)





def handle_error(driver, message_prefix, exception):
    print(f"{message_prefix} {exception}")
    screenshot_path = os.path.join(os.getcwd(), 'error_screenshot.png')
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")
    driver.quit()
    exit()

def main():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=get_chrome_options())

    url = "https://web.tecalliance.net/tecdoc/en/home"
    driver.get(url)

    try:
        login(driver)
        search_and_interact(driver)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()