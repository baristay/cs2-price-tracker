import pandas as pd
from urllib.parse import quote
import os
import logging
import requests
import time
import datetime

#Log Settings
currentdir = os.getcwd()
currentdir = currentdir.replace("Scripts", "")

c = datetime.datetime.now()
currenttime = c.strftime('%Y-%m-%d %H.%M.%S')

logdir = os.path.join(currentdir, "Logs", f"ItemDataLog_{currenttime}.log")

logger = logging.getLogger('my_logger')
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(logdir, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
    
logger.info("Starting script...")

#Getting apiKey from provided excel spreadsheet
def read_apikey(exceldirectory: str) -> str:
    try:
        df_welcome_page = pd.read_excel(exceldirectory, sheet_name='Welcome Page', header=None)
        apikey = df_welcome_page.iloc[20, 3]
        if pd.isna(apikey) or not apikey:
            raise ValueError("API key is empty or invalid.")
        logger.info(f"API key successfully retrieved.")
        return apikey
    except ValueError as e:
        logger.error(f"Error: {e}")
        exit(1)
    except Exception as e:
        logger.error(f"Unexpected error while reading API key: {e}")
        exit(1)

#Creating dataframe from provided excel spreadsheet
def read_items(exceldirectory: str) -> pd.core.frame.DataFrame:
    try:
        logger.info("Reading Main Data sheet.")
        df = pd.read_excel(exceldirectory, sheet_name='Main Data')
        logger.info(f"Main Data sheet successfully read. Total items: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Error while reading Main Data sheet: {e}")
        exit(1)

#fetching price for an item
def fetch_price(apikey: str, itemname: str,retries: int=3,delay: int=2) -> list[str, str]:
    itemname_encoded = quote(str(itemname))
    url = f"http://steamcommunity.com/market/priceoverview/?currency=1&appid=730&market_hash_name={itemname_encoded}&key={apikey}"
    logger.info(f"Checking price for item: {itemname} (Encoded: {itemname_encoded})")
    #Retrying for the range of "retries"
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                prices = [data.get('lowest_price', "Price not available"),
                          data.get('median_price', "Price not available")]
                logger.info(f"Price check successful for item: {itemname}. Prices: {prices}")
                return prices
            else:
                logger.warning(f"Attempt {attempt + 1}: Failed to fetch price for item {itemname}. HTTP Status: {response.status_code}")
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: Error fetching price for item {itemname}. Error: {e}")
        time.sleep(delay)
    return ['Error', 'Error']

#Getting and organizing data with the help of fetch_price function    
def organizing_data(df: pd,apikey: str) -> list[dict[str,str]]:
    results = []
    for _, row in df.iterrows():
        itemname = row['Full Name']
        logger.info(f"Processing item: {itemname}")
        price = fetch_price(apikey, itemname)
        results.append({'Actual Name': itemname, 'Lowest Price': price[0], 'Median Price': price[1]})
    logger.info(f"Total processed items: {len(results)}")
    return results

#saving result to provided csv directory
def saving_to_csv(results: list,csvdirectory: str):
    try:
        pd.DataFrame(results).to_csv(csvdirectory, index=False)
        logger.info("Results saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")

def main():
    #Directories
    current_directory = os.getcwd()
    c = datetime.datetime.now()
    currenttime = c.strftime('%Y-%m-%d %H.%M.%S')
    current_directory = current_directory.replace("scripts", "")
    Excelfile_directory = os.path.join(current_directory, "Main Spreadsheet.xlsm")
    Csvout_directory = os.path.join(current_directory, "Data", f"price_{currenttime}.csv")
    
    apikey = read_apikey(Excelfile_directory)
    df = read_items(Excelfile_directory)
    results = organizing_data(df, apikey)
    saving_to_csv(results,Csvout_directory)

    logger.info("Cvs file saved.")

if __name__ == "__main__":
    main()