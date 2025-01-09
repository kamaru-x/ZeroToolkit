import os
import subprocess
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

################################################## EXECUTE PROGRAMME ##################################################

def execute_item(item_id):
    item = next((i for i in marketplace_items if i["id"] == item_id), None)
    
    if item:
        print(f"\033[92mExecuting {item['name']}...\033[0m")
        
        if item["type"] == "module":
            exec_path = os.path.join(os.getcwd(), "modules", item["folder"], item["start"])
        elif item["type"] == "script":
            exec_path = os.path.join(os.getcwd(), "scripts", item["folder"], item["start"])
        elif item["type"] == "exploit":
            exec_path = os.path.join(os.getcwd(), "exploits", item["folder"], item["start"])
        else:
            print(f"Error: Unknown item type '{item['type']}'")
            return
        
        if os.path.exists(exec_path):
            try:
                if item["language"] == "python":
                    subprocess.run(["python", exec_path], check=True)
                elif item["language"] == "bash":
                    subprocess.run(["bash", exec_path], check=True)
                else:
                    print(f"Error: Unsupported language '{item['language']}' for {item['name']}.")
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to execute {item['name']}. {e}")
        else:
            print(f"Error: {item['start']} not found in the specified path.")
    else:
        print(f"Error: Item with ID {item_id} not found.")