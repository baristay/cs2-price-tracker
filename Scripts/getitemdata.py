from steam_community_market import Market, AppID

market = Market("USD")
CsID = AppID.CSGO
itemname = "P2000 | Urban Hazard (Field-Tested)"
def fetch_price(market, GameID, ItemName):
    retries = 3
    print(f"Checking price for item: {ItemName}")
    for attempt in range(retries):
        try:
            result = market.get_overview(ItemName,GameID)
            if result["success"] == True:
                prices = [result.get("lowest_price", "Price not available"),
                          result.get("median_price", "Price not available"),
                          result.get("volume", "Volume not available")]
                print((f"Price check successful for item: {ItemName}. Prices: {prices}"))
                return prices
            else:
                print(f"Attempt {attempt + 1}: Failed to fetch price for item {itemname}. HTTP Status: {response.status_code}")
        except Exception as e:
            print (f"Attempt {attempt + 1}: Error fetching price for item {itemname}. Error: {e}")
    return ["Error","Error","Error"]
fetch_price(market,CsID,itemname)



def fetch_price2(apikey: str, itemname: str,retries: int=3,delay: int=2) -> list[str, str]:
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