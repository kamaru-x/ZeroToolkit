# marketplace.py

# Define available types
ITEM_TYPES = {
    "module": "modules",
    "script": "scripts",
    "exploit": "exploits"
}

# Only support Python
SUPPORTED_LANGUAGE = "python"

marketplace_items = [
    {"id": "mapper", "name": "Network Mapper", "description": "Find device in a network", 
     "url": "https://github.com/kamaru-x/Scanner.git", "type": "script", 
     "folder": "mapper", "start": "scanner.py", "superuser": True},
]

def get_plural_name(item_type):
    return ITEM_TYPES.get(item_type, f"{item_type}s")

def is_valid_type(item_type):
    return item_type in ITEM_TYPES

def list_marketplace_items(items, title):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    
    print("\n" + "─" * 100)
    print(f"{GREEN}{title.center(100)}{RESET}")
    print("─" * 100 + "\n")
    
    for item in items:
        print(f"{CYAN}❯ {YELLOW}ID{RESET}: {item['id']}")
        print(f"{CYAN}├─{YELLOW}Name{RESET}: {BLUE}{item['name']}{RESET}")
        print(f"{CYAN}├─{YELLOW}Type{RESET}: {item['type']}")
        print(f"{CYAN}└─{YELLOW}Description{RESET}: {item['description']}")
        print()