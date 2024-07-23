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
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--lang=en')  # Set browser language to English
    # options.add_argument('--headless')  # Uncomment to run headless
    return options
#####################################################################################################
#####################################################################################################
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
#####################################################################################################
#####################################################################################################
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
#####################################################################################################
#####################################################################################################
import os
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_and_interact(driver):
    try:
        # Maximize the window
        driver.maximize_window()

        # Wait for the search box to be visible after login
        search_box = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@formcontrolname='typeNumber']"))
        )

        search_query = input("Enter your search query: ")
        search_box.send_keys(search_query)

        # Create a directory for the search query if it doesn't exist
        query_dir = os.path.join(os.getcwd(), search_query)
        os.makedirs(query_dir, exist_ok=True)

        # Click the search icon
        search_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//i[@class='ta-icon-search']"))
        )
        search_icon.click()

        # Take a screenshot after login and page load
        screenshot_path = os.path.join(query_dir, 'screenshot.png')
        #driver.save_screenshot(screenshot_path)
        #print(f"Screenshot saved to {screenshot_path}")

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

        # Extract the number from the product groups div
        product_groups_text = product_groups_div.get_attribute('innerHTML')
        match = re.search(r'Product groups : <strong class="ng-star-inserted">\s*(\d+)\s*</strong>', product_groups_text)
        if match:
            product_groups_number = match.group(1)
            product_groups_number = int(product_groups_number)  # Convert to integer

            print(f"Product groups number: {product_groups_number}")

        time.sleep(5)  # Optional: Add a delay to see the interaction

        # Start interacting with articles
        interact_with_articles(driver, query_dir,product_groups_number)

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

def interact_with_articles(driver, query_dir,product_groups_number):
    try:
        current_index = 0

        def get_generic_articles():
            return WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//span[@class='generic-article']"))
            )

        def click_next_button():
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[@class='ag-icon ag-icon-next']"))
                )
                next_button.click()
                print("Current index after next button:", current_index)
                time.sleep(4)  # Wait for the new page to load articles
            except Exception as e:
                print("Next button not found or not clickable:", e)

        while True:
            if current_index % 25 == 0 and current_index != 0:
                click_next_button()

            try:
                if current_index == 0:
                    try:
                        close_icon = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//svg[contains(@class, 'p-icon p-multiselect-close-icon')]"))
                        )
                        close_icon.click()
                        print("Clicked on close icon.")
                        time.sleep(2)
                    except Exception as e:
                        print("Close icon not found or not clickable:", e)

                article_to_click = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, f"//div[@row-index='{current_index}']//div[@role='gridcell' and @col-id='stateText' and @aria-colindex='7']"))
                )
                article_to_click.click()
                time.sleep(2)  # Optional: Wait for the next page to load

                article_name = extract_article_name_from_page(driver)
                print("Clicking on article:", article_name)
                if "Bulb" in article_name:
                    print(f"Article {article_name} contains 'Bulb'. Skipping.")
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'p-menuitem-icon ta-icon ta-icon-back ng-star-inserted')]"))
                    )
                    back_button.click()
                    time.sleep(4)
                    current_index += 1
                    print("Current index :",current_index)

                else :
                # Check if the article name already exists in the directory
                 file_path = os.path.join(query_dir, f"{article_name}.json")
                 if os.path.exists(file_path):
                    print(f"Article {article_name} already exists. Skipping.")
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'p-menuitem-icon ta-icon ta-icon-back ng-star-inserted')]"))
                    )
                    back_button.click()
                    time.sleep(4)
                    current_index += 1
                    print("Current index :",current_index)

        
                    
                 else :
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
                  current_index += 1
                  print("Current index at end of loop:", current_index)

            except Exception as ex:
                print(f"Error clicking article: {article_name}, Exception: {ex}")
                # Skip the current article and continue with the next one
               

            # Get the total number of articles and check if we reached the end
            
            if current_index >= product_groups_number:
                break

    except Exception as e:
        handle_error(driver, "Error during article interaction:", e)

#####################################################################################################
#####################################################################################################

def extract_data_from_page(driver):
    data = {}
    #screenshot_counter=1
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

            chevrondownicon.click()

            #driver.save_screenshot(f"screenshot ili baad  _{screenshot_counter}.png")

            
            # Iterate over each car make and extract OE references
            for car_make in car_makes:
             try:
                
                chevrondownicon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'p-autocomplete-dropdown')]"))
            ) 
                chevrondownicon.click()
                time.sleep(2)
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
                screenshot_path = f"screenshot_list_item_{item_text.replace(' ', '_')}.png"
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
    screenshot_path = os.path.join(os.getcwd(), 'error_screenshot.png')
    #driver.save_screenshot(screenshot_path)
    #print(f"Screenshot saved to {screenshot_path}")
    driver.quit()
    exit()
#####################################################################################################
#####################################################################################################
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
