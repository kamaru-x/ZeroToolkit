import os
import subprocess
from programs.marketplace import marketplace_items, list_marketplace_items
from programs.functions import search_items

project_dir = os.path.abspath(os.getcwd())


################################################## HELP ##################################################

def cmd_help(args):
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    print(f"""
    {BLUE}marketplace{RESET}     {WHITE}Interfaces with the module marketplace{RESET}
    {BLUE}exit{RESET}            {WHITE}Exits the framework{RESET}
    """)

################################################## MARKETPLACE ##################################################

def cmd_marketplace(args):
    item_types = {item["type"] for item in marketplace_items}

    if not args:
        list_marketplace_items(marketplace_items, "Marketplace (All Items)")
    elif len(args) == 1:
        if args[0] in item_types:
            list_marketplace_items([item for item in marketplace_items if item["type"] == args[0]], args[0].capitalize())
        else:
            print(f"Error: Unknown argument '{args[0]}'. Valid types are {', '.join(item_types)}.")
    elif len(args) == 2 and args[0] == "search":
        search_items(args[1])
    elif len(args) == 2 and args[0] == "install":
        cmd_install(args[1:])
    else:
        print("Error: Invalid command format. Use 'marketplace [modules|scripts|exploits]' or 'marketplace search <term>' or 'marketplace install <item_id>'.")

################################################## INSTALL ##################################################

def cmd_install(args):
    if len(args) == 1:
        item_id = args[0]
        
        item = next((i for i in marketplace_items if i["id"] == item_id), None)
        
        if item:
            print(f"\033[92mInstalling {item['name']}...\033[0m")
            
            type_to_folder = {"module": "modules", "script": "scripts", "exploit": "exploits"}
            
            install_type = item["type"]
            if install_type not in type_to_folder:
                print(f"Error: Unknown item type '{install_type}'")
                return

            install_path = os.path.join(os.getcwd(), type_to_folder[install_type], item["folder"])
            
            if not os.path.exists(install_path):
                os.makedirs(install_path)
                print(f"Created folder: {install_path}")

            try:
                subprocess.run(["git", "clone", item["url"], install_path], check=True)
                print(f"Successfully installed {item['name']} to folder: {install_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error: Failed to install {item['name']}. Git clone failed. {e}")
        else:
            print(f"Error: Item with ID {item_id} not found.")
    else:
        print("Error: Invalid command format. Use 'install <item_id>'.")

################################################## EXIT ##################################################

def cmd_exit(args):
    print("Exiting ZeroToolkit. Goodbye!")
    exit(0)