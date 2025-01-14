from typing import Dict, List
from programs.marketplace import (
    marketplace_items, list_marketplace_items,
    MarketplaceItem, Color as c
)

INSTALL_DIRS: Dict[str, str] = {
    "module": "modules",
    "script": "scripts",
    "exploit": "exploits"
}

def search_items_by_type(item_type: str, search_term: str) -> None:
    """
    Search items by type and search term

    Args:
        item_type: Type of item to search for
        search_term: Search string to match against item names
    """
    filtered_items = [
        item for item in marketplace_items
        if item.type == item_type and search_term.lower() in item.name.lower()
    ]

    if filtered_items:
        list_marketplace_items(filtered_items, f"Search Results: {item_type.capitalize()}")
    else:
        print(f"{c.RED}No {item_type}s found matching '{search_term}'{c.RESET}")

def search_items(search_term: str) -> None:
    """
    Search all items regardless of type

    Args:
        search_term: Search string to match against item names
    """
    filtered_items = [
        item for item in marketplace_items
        if search_term.lower() in item.name.lower()
    ]

    if filtered_items:
        list_marketplace_items(filtered_items, f"Search Results: '{search_term}'")
    else:
        print(f"{c.RED}No items found matching '{search_term}'{c.RESET}")