from steam_community_market import Market, AppID

market = Market("USD")

item = "P2000 | Urban Hazard (Field-Tested)"

print(market.get_overview(item, 730))


print(market.get_volume(item, 730))
