import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re 
from selenium.webdriver.common.keys import Keys

#####################################################################################################
#####################################################################################################
def get_chrome_options():
    """
    Configure les options du navigateur Chrome.

    Returns:
        ChromeOptions: Options configurées pour le navigateur Chrome.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--lang=en')  # Set browser language to English
    # options.add_argument('--headless')  # Uncomment to run headless
    return options
#####################################################################################################
#####################################################################################################
def login(driver):
    """
    Connecte l'utilisateur en remplissant le formulaire de connexion.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.

    Raises:
        Exception: En cas d'erreur lors du processus de connexion.
    """
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
#####################################################################################################
#####################################################################################################
def handle_additional_pages(driver):
    """
    Gère les pages supplémentaires qui peuvent apparaître après la connexion en cliquant sur les boutons ou en fermant les fenêtres.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.
    """
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
#####################################################################################################
#####################################################################################################
import os
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException


def search_and_interact(driver, excel_path , ktype, part1):
    """
    Effectue une recherche et interagit avec les éléments de la page en fonction des données fournies dans un fichier Excel.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.
        excel_path (str): Chemin du fichier Excel contenant les données à utiliser.
        ktype (str): KType de recherche à effectuer.
        part1 (str): Nom de la partie pour créer un répertoire , ici c'est le vehicle number extrait depuis l'input de l'interface Excel.

    Raises:
        TimeoutException: Si les éléments nécessaires ne sont pas trouvés ou ne sont pas visibles dans le délai imparti.
        Exception: Toute autre exception non spécifiée pendant la recherche et l'interaction.

    """
    try:
        # Maximize the window
        driver.maximize_window()

        # Wait for the search box to be visible after login
        search_box = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='typeNumber']"))
        )

        search_query = ktype
        search_box.send_keys(search_query)

        # Create a directory for the search query if it doesn't exist
        root_dir=r"C:\Users\IT2\Desktop\TecDoc"
        folder_name=part1+"_"+ktype
        query_dir = os.path.join(root_dir, folder_name)
        os.makedirs(query_dir, exist_ok=True)

        # Click the search icon
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='ta-icon-search']"))
        )
        search_icon.click()

        # Take a screenshot after login and page load
        #screenshot_path = os.path.join(query_dir, 'screenshot.png')
        #driver.save_screenshot(screenshot_path)
        #print(f"Screenshot saved to {screenshot_path}")

        # Load the Excel file
        df = pd.read_excel(excel_path)

        # Iterate through each part in the Excel file
        for index, row in df.iterrows():
            part_name_tech_doc = row['Part Name Tech Doc']
            #position = row['Fitting Position']
            
            # Click on "All product groups" dropdown
            product_groups_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='p-multiselect-label p-placeholder']"))
            )
            product_groups_div.click()

            # Enter the part name in the input box
            filter_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@role='textbox' and @class='p-multiselect-filter p-inputtext p-component']"))
            )
            filter_input.send_keys(part_name_tech_doc)
            time.sleep(2)  # Optional: Wait for the list to update

            # Get the list of items that appear
            items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']//li[@aria-label]"))
            )

            # Iterate through the items and click the one that matches the part name
            for item in items:
                item_label = item.get_attribute('aria-label')
                if part_name_tech_doc in item_label:
                    checkbox = item.find_element(By.XPATH, ".//div[@class='p-checkbox-box']")
                    checkbox.click()
                    print(f"Clicked on item: {item_label}")
                    break

            # Optional: Add a delay to see the interaction
            time.sleep(5)


            #expand button
            try:
                # Wait for the <a> element with specific class to be clickable and click it
                second_div = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "(//div[contains(@class, 'd-flex flex-grow-1 flex-nowrap align-items-center mw-100 ng-star-inserted')])[2]"))
                )

                # Find and click the expand button within the second div
                expand_button = second_div.find_element(By.XPATH, ".//a[@ta-name='expand-button' and contains(@class, 'text-primary') and contains(@class, 'ng-star-inserted')]")
                driver.execute_script("arguments[0].click();", expand_button)
                print("Clicked on expand button")
            except Exception as e:
                print("Expand button not found or not clickable")

            
            time.sleep(4)
            #extract of all criteria of the item and save it in list to compare if this criteria is used as column in excel 
            try:
              elements = WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(@class, 'criterion-title') and contains(@class, 'd-flex') and contains(@class, 'justify-content-between') and contains(@class, 'mt-2') and contains(@class, 'mb-1') and contains(@class, 'ng-star-inserted')]"))
    )
    
              for element in elements:
                try:
                    strong_elements = element.find_elements(By.XPATH, ".//strong")
            
                    for strong in strong_elements:

                        strong_text = strong.text.strip()
                       #print("hani lina :",strong_text)
                        for col in df.columns:                           
                           
                           if str(strong_text).strip() == str(col).strip():
                               strong.click()
                               print(f"Clicked on strong element: {strong_text}")
                               labels = driver.find_elements(By.XPATH, "//label[contains(@class, 'text-break p-checkbox-label ng-star-inserted')]")
                               for label in labels:
                                    label_text = label.text.strip()
                                    cleaned_text = re.sub(r'\([^)]*\)', '', label_text)  # Suppression du texte entre parenthèses
                                    print("compare cleand text with the label txt")
                                    print(cleaned_text.strip(),"hani")
                                    print(str(row[col]).strip(),"hani")
                                    if cleaned_text.strip() == str(row[col]).strip():
                                        label.click()
                except Exception as e:
                           print(f"Error extracting <strong> elements: {str(e)}")                 
                                    

              time.sleep(4)


              json_file_name= part1+"_"+row['Part  ID']

              interact_with_articles(driver, query_dir,json_file_name)
                               

                               
              back_button = WebDriverWait(driver, 10).until(
                                      EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'p-menuitem-icon ta-icon ta-icon-back ng-star-inserted')]"))
                                  )
              back_button.click()



              time.sleep(5)

            
                    
                   

            except TimeoutException:
                 print("Timeout: Elements not found or not visible.")
            except Exception as e:
                 print(f"Error occurred: {str(e)}")
 
        # Start interacting with articles

    except Exception as e:
        handle_error(driver, "Error during search and interaction:", e)

#####################################################################################################
#####################################################################################################
def extract_article_name_from_page(driver):
    try:
        # Locate the row with the "Product group" text
        product_group_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[th[text()='Product group ']]"))
        )
        # Extract the article name from the corresponding cell
        article_name = product_group_row.find_element(By.XPATH, "./td").text.strip()
        
        # Check for the presence of a pipe and take the substring before it if found
        if '|' in article_name:
            article_name = article_name.split('|')[0].strip()
            
        article_name = re.sub(r'[^a-zA-Z0-9_ ]', '_', article_name)
        return article_name
    except Exception as e:
        print("Error extracting article name:", e)
        return "unknown_article"

#####################################################################################################
#####################################################################################################

def interact_with_articles(driver, query_dir, json_file_name):

    """
    Interagit avec les articles sur une page,cliquer sur l'article , extrait les données et les enregistre dans un fichier JSON.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.
        query_dir (str): Répertoire de la requête où les fichiers doivent être enregistrés.
        json_file_name (str): Nom du fichier JSON à enregistrer.

    Raises:
        TimeoutException: Si les éléments nécessaires ne sont pas trouvés ou ne sont pas visibles dans le délai imparti.
        Exception: Toute autre exception non spécifiée pendant l'interaction avec les articles.

    """
    try:
        current_index = 0


      
           
        try:
                
                 article_to_click = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@row-index='{current_index}']//div[@role='gridcell' and @col-id='stateText' and @aria-colindex='7']"))
                )
                 article_to_click.click()
                 time.sleep(2)  # Optional: Wait for the next page to load

                 article_name = json_file_name
                 print("Clicking on article:", article_name)
               
                
                # Check if the article name already exists in the directory
                 file_path = f"{query_dir}\\{json_file_name}.json"


                 #print("HW il FILE PATh",file_path)               
        
                    
                
                # Extract data from the article page
                 data = extract_data_from_page(driver)

                # Save the extracted data to a JSON file
                 with open(file_path, 'w') as json_file:
                    json.dump(data, json_file, indent=4)
                 print(f"Data saved to {file_path}")

                # Click the back button to return to the article list
                 back_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'p-menuitem-icon ta-icon ta-icon-back ng-star-inserted')]"))
                )
                 back_button.click()
                 time.sleep(4)
 
                # Increment the index to move to the next article
                 

        except Exception as ex:
                print(f"Error clicking article: {article_name}, Exception: {ex}")
                # Skip the current article and continue with the next one
               

            # Get the total number of articles and check if we reached the end
         

    except Exception as e:
        handle_error(driver, "Error during article interaction:", e)

#####################################################################################################
#####################################################################################################

def extract_data_from_page(driver): 
    """
    Extracte les éléments de données de la page web actuelle.ici il y aura extraction des criteres de l'article cliqué avec les references de chaque article pour chaque type de vehicle.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.

    Returns:
        dict: Dictionnaire contenant les données extraites de la page.

    Raises:
        Exception: Toute exception non spécifiée pendant l'extraction des données.

    """
    data = {}
    screenshot_counter=1
    try:
        # Click the criteria button to open the criteria table
        try:
            criteria_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "i.ta-icon.ta-icon-criteria.ng-star-inserted"))
            )
            criteria_button.click()
            print("Clicked on the button of criteria")

            # Wait for the criteria table to be visible and extract data
            criteria_table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//table[@class='table table-sm table-2c-list table-border-top-0 mb-0']"))
            )
            rows = criteria_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                try:
                    criterion_name = row.find_element(By.XPATH, "./th").text.strip()
                    criterion_value = row.find_element(By.XPATH, "./td").text.strip()
                    data[criterion_name] = criterion_value
                except Exception as ex:
                    print(f"Error extracting data from row: {ex}")
        except Exception as ex:
            print(f"Criteria button not found: {ex}")
            data['Criteria'] = {}

        # Attempt to extract car makes and their OE references
        try:
            # Click the chevrondownicon to show all car makes
            chevrondownicon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-autocomplete-dropdown')]"))
            )
            chevrondownicon.click()
            print("Clicked on chevrondownicon to display all car makes")
            time.sleep(2)

            # Extract car makes
            car_makes_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option' and @class='p-ripple p-element p-autocomplete-item ng-star-inserted']"))
            )
            car_makes = [element.text.strip() for element in car_makes_elements if element.text.strip()]
            print("Extracted car makes:", car_makes)


            #driver.save_screenshot(f"screenshot ili 9bal _{screenshot_counter}.png")
            time.sleep(1)

            chevrondownicon.click()

            #driver.save_screenshot(f"screenshot ili baad  _{screenshot_counter}.png")
            time.sleep(1)

            
            # Iterate over each car make and extract OE references
            for car_make in car_makes:
             try:
                
                chevrondownicon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-autocomplete-dropdown')]"))
            ) 
                chevrondownicon.click()
                time.sleep(3)
                #driver.save_screenshot(f"screenshot_{screenshot_counter}.png")
                #screenshot_counter += 1
                # Click on the car make to select it
                car_make_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//li[@role='option' and .//span[text()='{car_make}']]"))
                )
                car_make_element.click()
                print(f"Clicked on car make: {car_make}")

                # Wait for OE references to load
                oe_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[@class='text-primary' and @ta-name='oe-button']/strong"))
                )
                oe_references = [oe_button.text.strip() for oe_button in oe_buttons]
                data[f'{car_make} OE References'] = oe_references
                print(f"Extracted OE references for {car_make}: {oe_references}")

                # Click on chevrondownicon again to show all car makes
                
                time.sleep(2)  # Adjust as needed

             except Exception as ex:
                print(f"Error extracting OE references for {car_make}: {ex}")
        except Exception as ex:
            print(f"Error displaying car makes: {ex}")
           # data['Car Makes'] = []
            
            # If car makes are not found, extract OE references directly
            try:
                oe_buttons = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//a[@class='text-primary' and @ta-name='oe-button']/strong"))
                )
                oe_references = [oe_button.text.strip() for oe_button in oe_buttons]
                data['OE References'] = oe_references
                print(f"Extracted OE references directly: {oe_references}")
            except Exception as oe_ex:
                print(f"Error extracting OE references directly: {oe_ex}")
                data['OE References'] = []

        try:
            car_icon = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@class='ta-icon ta-icon-car ng-star-inserted']"))
            )
            car_icon.click()
            print("Clicked on car icon")

            # Call the function to click on list items
            vehicle_data = click_on_list_items(driver)
            data['Vehicle Data'] = vehicle_data

        except Exception as e:
            print(f"Car icon not found: {e}")
            data['Vehicle Data'] = []
    except Exception as e:
        print(f"Error extracting data from page: {e}")

    return data

#####################################################################################################
#####################################################################################################
def click_on_list_items(driver):
    """
    Clique sur chaque élément de liste dans un élément <ul> spécifié sur la page web actuelle
    et extrait des informations spécifiques pour chaque élément.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.

    Returns:
        list: Liste contenant les données extraites pour chaque élément de liste.

    Raises:
        Exception: Toute exception non spécifiée pendant l'extraction des données.

    """
    vehicle_data = []
    try:
        # Locate all list items in <ul>
        list_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='mt-3']/li/a"))
        )

        # Click on each list item
        for item in list_items:
            try:
                item_text = item.text.strip()
                print(f"Clicking on list item: {item_text}")

                # Re-find the element in the page to avoid stale element reference error
                item_to_click = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, f"//ul[@class='mt-3']/li/a[contains(text(), '{item_text}')]"))
                )
                item_to_click.click()

                time.sleep(2)  # Optional: Wait for the next page to load

                # Extract specific information for each item

                item_data = extract_data_for_list_item(driver)


                vehicle_data.append({item_text: item_data})

                # Click the close button
                close_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'ta-icon-cancel')]"))
                )
                close_button.click()

                # Optional: Take a screenshot after clicking the list item
                # screenshot_path = f"screenshot_list_item_{item_text.replace(' ', '_')}.png"
                #driver.save_screenshot(screenshot_path)
                #print(f"Screenshot saved to {screenshot_path}")

                time.sleep(4)  # Optional: Wait for the previous page to reload

            except Exception as ex:
                print(f"Error clicking list item: {item_text}, Exception: {ex}")

    except Exception as e:
        print(f"Error clicking on list items: {e}")

    return vehicle_data
#####################################################################################################
#####################################################################################################
def extract_data_for_list_item(driver):
    """
    Extrait les valeurs spécifiques des colonnes de chaque ligne d'une table sur la page web actuelle.
    Les données ici sont les infos lieés aux vehicles compatibles avec notre vehicle en recherche.

    Args:
        driver (WebDriver): Instance du pilote WebDriver pour contrôler le navigateur.

    Returns:
        list: Liste contenant les données extraites pour chaque ligne de la table.

    Raises:
        Exception: Toute exception non spécifiée pendant l'extraction des données.

    """
    item_data = []
    try:
        # Wait for specific rows of the table to be visible
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[@ta-name='vehicle-linkage__item']"))
        )

        for row in rows:
            try:
                # Extract the different values of the columns
                vehicle_name = row.find_element(By.XPATH, ".//div[@class='d-flex flex-column']/a/span").text.strip()
                date_range = row.find_element(By.XPATH, ".//th[3]/span").text.strip()
                ta_value = row.find_element(By.XPATH, ".//th[4]/span").text.strip()
                power_hp = row.find_element(By.XPATH, ".//th[5]/span").text.strip()
                power_kw = row.find_element(By.XPATH, ".//th[6]/span").text.strip()
                engine_capacity = row.find_element(By.XPATH, ".//th[7]/span").text.strip()
                body_type = row.find_element(By.XPATH, ".//th[8]/span").text.strip()

                # Append the extracted data to the item data list
                item_data.append({
                    'Vehicle Name': vehicle_name,
                    'Date Range': date_range,
                    'TA Value': ta_value,
                    'Power (HP)': power_hp,
                    'Power (kW)': power_kw,
                    'Engine Capacity': engine_capacity,
                    'Body Type': body_type
                })

            except Exception as ex:
                print(f"Error extracting data from row: {ex}")

    except Exception as e:
        print(f"Error extracting data from list item page: {e}")

    return item_data
#####################################################################################################
#####################################################################################################
def handle_error(driver, message_prefix, exception):
    print(f"{message_prefix} {exception}")
    #screenshot_path = os.path.join(os.getcwd(), 'error_screenshot.png')
    #driver.save_screenshot(screenshot_path)
    #print(f"Screenshot saved to {screenshot_path}")
    driver.quit()
    exit()
#####################################################################################################
#####################################################################################################
import sys

def main():
    """
    Fonction principale pour exécuter le script d'automatisation d'interaction avec le site Web TecDoc.

    Args:
        Aucun argument directement passé à la fonction. Utilise sys.argv pour récupérer ktype en ligne de commande.
        Le ktype ici de vehicle est part2.
        Alors que le VN est part1.

    Raises:
        Aucune exception gérée directement dans cette fonction, mais des exceptions peuvent être levées pendant l'exécution de l'automatisation.

    """
  
    ktype = sys.argv[1]
    parts = ktype.split('-')
    if len(parts) != 2:
        print("Le format de ktype est incorrect. Il doit être sous la forme 'nombre1-nombre2'.")
        return

    part1, part2 = parts
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=get_chrome_options())

    url = "https://web.tecalliance.net/tecdoc/en/home"
    driver.get(url)

    try:
        excel_path_root = r"C:\Users\IT2\Desktop\TecDoc"
        excel_path=f"{excel_path_root}\\{part1}.xlsx"
        login(driver)
        print("VOILA LE KTYPE",ktype)
        search_and_interact(driver, excel_path, part2,part1)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()