---

### README.txt

---

#### Introduction

This Python script uses Selenium to automate interaction with a TecDoc website, extracting data from an Excel file and saving the results in JSON files.
---

#### Project structure

- test.py # Main file containing all the functions
---
#### Use

1. **Install dependencies**:
   - Make sure you have installed Python and all the dependencies listed in `requirements.txt`.
   - Use `pip install -r requirements.txt` to install the dependencies.

2. **Run the script**:
   - Open a command line.
   - Navigate to the directory containing `test.py`.
   - Run the script using `python test.py`. (NOTE: this command requires a code modification to the main function as it is linked from the Excel interface).

3. **Using the Excel interface**:
   - This script is designed to interact with an Excel interface for data entry. Make sure that your Excel file is correctly configured and accessible from the script.  
---

#### Main functions

1)def get_chrome_options():
    """
    Configures the Chrome browser options.

    Returns:
        ChromeOptions: Options configured for the Chrome browser.
    """

2)def login(driver):
    """
    Logs the user in by filling in the login form.

    Args:
        driver (WebDriver): Instance of the WebDriver driver to control the browser.

    Raises:
        Exception: If an error occurs during the connection process.
    """

3)def handle_additional_pages(driver):
    """
    Handles additional pages that may appear after logging in by clicking buttons or closing windows.

    Args:
        driver (WebDriver): Instance of the WebDriver to control the browser.
    """

4)def search_and_interact(driver, excel_path , ktype, part1):
    """
    Performs a search and interacts with page elements based on data provided in an Excel file.

    Args:
        driver (WebDriver): Instance of the WebDriver to control the browser.
        excel_path (str): Path to the Excel file containing the data to be used.
        ktype (str): KType of search to perform.
        part1 (str): Name of the part to create a directory, here it is the vehicle number extracted from the Excel interface input.

    Raises:
        TimeoutException: If the required elements are not found or are not visible within the time limit.
        Exception: Any other unspecified exception during the search and interaction.

    """

5)def interact_with_articles(driver, query_dir, json_file_name):

    """
    Interacts with articles on a page,click on the article , extracts the data and saves it to a JSON file.

    Args:
        driver (WebDriver): Instance of the WebDriver driver to control the browser.
        query_dir (str): Query directory where files should be saved.
        json_file_name (str): Name of the JSON file to be saved.

    Raises:
        TimeoutException: If the required items are not found or are not visible within the timeout period.
        Exception: Any other unspecified exception during interaction with items.

    """

def click_on_list_items(driver):
    """
    Clicks on each list item in a specified <ul> element on the current web page
    and extracts specific information for each item.

    Args:
        driver (WebDriver): Instance of the WebDriver to control the browser.

    Returns:
        list: List containing the extracted data for each list item.

    Raises:
        Exception: Any unspecified exception during data extraction.

    """

7)def click_on_list_items(driver):
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

def extract_data_for_list_item(driver):
    """
    Extracts specific column values from each row of a table on the current web page.
    The data here is related to vehicles compatible with the searched vehicle.

    Args:
        driver (WebDriver): Instance of the WebDriver to control the browser.

    Returns:
        list: List containing the extracted data for each row of the table.

    Raises:
        Exception: Any unspecified exception during data extraction.

    """

def main():
    """
    Main function to execute the automation script for interacting with the TecDoc website.

    Args:
        No arguments are passed directly to the function. Uses sys.argv to get ktype from the command line.
        The ktype here is the vehicle's part2.
        While the VN is part1.

    Raises:
        No exceptions are directly handled in this function, but exceptions may be raised during the execution of the automation.

    """


---

#### Additional Notes

- Make sure to set up the environment with the correct path to the Excel file and the output directory for JSON files.
- The Excel file is named VN.
- This script uses Selenium and requires an active internet connection and an installed Chrome browser.
---

