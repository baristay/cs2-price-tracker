from steam_community_market import Market, AppID
import pandas as pd
from subprocess import call
import os
import logging
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

#Calling and running another python file from directory
def run_py_file(filename):
    call(["python", f"Scripts/{filename}"])

#Getting currency from provided excel spreadsheet
def get_currency(exceldirectory: str) -> str:
    try:
        logger.info("Reading Currency.")
        df = pd.read_excel(exceldirectory, "Welcome Page")
        if df.iat[16,6] == None:
            logger.info(f"Currency successfully read. Currency: {"USD"}")
            return "USD"
        logger.info(f"Currency successfully read. Currency: {df.iat[16,6]}")
        return df.iat[16,6] 
    except Exception as e:
        logger.error(f"Error while reading Main Data sheet: {e}")
        exit(1)

#Creating dataframe from provided excel spreadsheet
def read_items(exceldirectory: str) -> pd.DataFrame:
    try:
        logger.info("Reading Main Data sheet.")
        df = pd.read_excel(exceldirectory, sheet_name='Main Data')
        logger.info(f"Main Data sheet successfully read. Total items: {len(df)}")
        return df
    except Exception as e:
        logger.error(f"Error while reading Main Data sheet: {e}")
        exit(1)

#Fetching price for an item
def fetch_price(market, GameID, itemname: str,retries: int=2 ,delay: int=2) -> list[str, str, str]:
    retries = 3
    logger.info(f"Checking price for item: {itemname}")
    for attempt in range(retries):
        try:
            result = market.get_overview(itemname,GameID)
            if result["success"] == True:
                prices = [result.get("lowest_price", "Price not available"),
                          result.get("median_price", "Price not available"),
                          result.get("volume", "Volume not available")]
                logger.info((f"Price check successful for item: {itemname}. Prices: {prices}"))
                return prices
            else:
                logger.warning(f"Attempt {attempt + 1}: Failed to fetch price for item {itemname}.")
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}: Error fetching price for item {itemname}. Error: {e}")
        time.sleep(delay)
    return ["Error","Error","Error"]

#Getting and organizing data with the help of fetch_price function    
def organizing_data(df: pd, market, CsID) -> list[dict[str,str]]:
    results = []
    for _, row in df.iterrows():
        itemname = row['Full Name']
        logger.info(f"Processing item: {itemname}")
        price = fetch_price(market, CsID, itemname)
        results.append({'Actual Name': itemname, 'Lowest Price': price[0], 'Median Price': price[1], 'Volume': price[2]})
    logger.info(f"Total processed items: {len(results)}")
    return results

#saving result to provided csv directory
def saving_to_csv(results: list,csvdirectory: str):
    try:
        pd.DataFrame(results).to_csv(csvdirectory, index=False, encoding='utf-8-sig')
        logger.info("Results saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")

def main():
    #Directories
    c = datetime.datetime.now()
    currenttime = c.strftime('%Y-%m-%d %H.%M.%S')
    current_directory = os.getcwd()
    current_directory = current_directory.replace("scripts", "")
    Excelfile_directory = os.path.join(current_directory, "Main Spreadsheet.xlsm")
    Csvout_directory = os.path.join(current_directory, "Data", f"price_{currenttime}.csv")

    #Script names
    sorting_logs_prices = "Sorting_Logs_Prices.py"

    #Currency and Game ID
    currency = get_currency(Excelfile_directory)
    market = Market(currency)
    CsID = AppID.CSGO

    #executing functions
    run_py_file(sorting_logs_prices)
    df = read_items(Excelfile_directory)
    results = organizing_data(df, market, CsID)
    saving_to_csv(results,Csvout_directory)

if __name__ == "__main__":
    main()