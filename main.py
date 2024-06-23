from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

def getPastSales():
    # Path to the ChromeDriver executable
    # Step 1: Set up Selenium and navigate to the page
    driver_path = 'C:/Users/faisa/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'  # Change this to your WebDriver path
    url = 'https://www.compass.com/building/8-e-randolph-st-chicago-il-60601/593188869696766517/'  # Replace with your URL


    # Create a Service instance
    service = Service(driver_path)

    # Initialize the Chrome WebDriver with the Service instance
    driver = webdriver.Chrome(service=service)  # Replace with your URL
    driver.get(url)

    try:
        # Wait for the page to load and the "Past Sales" tab to be clickable
        wait = WebDriverWait(driver, 10)
        past_sales_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/main/div[4]/div/div[2]/div/button[2]")))  # Change the XPATH to the actual tab's identifier
        past_sales_tab.click()

        # Wait for the table to load after clicking the tab
    # wait.until(EC.presence_of_element_located((By.XPATH, "//table")))  # Change the XPATH to the actual table's identifier
        time.sleep(5)
        # Step 2: Parse the HTML content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Step 3: Find the table
        table = soup.find('table')  # Find the first table, or use a more specific selector

        # Step 4: Extract the table headers
        headers = []
        for th in table.find('tr').find_all('th'):
            headers.append(th.text.strip())

        # Step 5: Extract the table rows
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip the header row
            cells = tr.find_all('td')
            row = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
            rows.append(row)

        # Step 6: Convert to a pandas DataFrame (optional)
        df = pd.DataFrame(rows)

        # Print the DataFrame

        df['Ba'] = pd.to_numeric(df['Ba'], errors='coerce')

        df.dropna(subset=['Ba'], inplace=True)

        # Convert 'Ba' column to integer
        df['Ba'] = df['Ba'].astype(int)
        

        filtered_df = df[df['Ba'] < 2]
        print(filtered_df)

        

        # Save the DataFrame to a CSV file
        #df.to_csv('table_data.csv', index=False)

    finally:
        # Step 7: Close the browser
        driver.quit()

def getActiveSales():
    # Path to the ChromeDriver executable
    # Step 1: Set up Selenium and navigate to the page
    url = 'https://www.compass.com/building/8-e-randolph-st-chicago-il-60601/593188869696766517/'  # Replace with your URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure we notice bad responses

    # Step 2: Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Step 3: Find the table
    table = soup.find('table')  # Find the first table, or use a more specific selector

    # Step 4: Extract the table headers
    headers = []
    for th in table.find('tr').find_all('th'):
        headers.append(th.text.strip())

    # Step 5: Extract the table rows
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        cells = tr.find_all('td')
        row = {headers[i]: cells[i].text.strip() for i in range(len(cells))}
        rows.append(row)

    # Step 6: Convert to a pandas DataFrame (optional)
    df = pd.DataFrame(rows)

    # Print the DataFrame
    print(df)

#print(getPastSales())
print(getActiveSales())