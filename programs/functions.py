from programs.marketplace import marketplace_items, list_marketplace_items


################################################## SEARCH ##################################################

def search_items(query):
    print(f"\033[92mSearching for '{query}' in Marketplace...\033[0m")
    found_items = [item for item in marketplace_items if query.lower() in item["name"].lower() or query.lower() in item["description"].lower()]
    
    if found_items:
        list_marketplace_items(found_items, "Search Results")
    else:
        print(f"No results found for '{query}'.")