from programs.marketplace import marketplace_items, list_marketplace_items

INSTALL_DIRS = {
    "module": "modules",
    "script": "scripts",
    "exploit": "exploits"
}

################################################## SEARCH ##################################################

def search_items_by_type(item_type, search_term):
    filtered_items = [item for item in marketplace_items if item["type"] == item_type and search_term.lower() in item["name"].lower()]
    if filtered_items:
        list_marketplace_items(filtered_items, item_type.capitalize())
    else:
        print(f"No {item_type}s found for search term '{search_term}'.")

def search_items(search_term):
    filtered_items = [item for item in marketplace_items if search_term.lower() in item["name"].lower()]
    if filtered_items:
        list_marketplace_items(filtered_items, "Search Results")
    else:
        print(f"No items found for search term '{search_term}'.")