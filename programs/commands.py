import os
import shutil
import subprocess
from programs.marketplace import marketplace_items, list_marketplace_items
from programs.functions import search_items, search_items_by_type, execute_item

project_dir = os.path.abspath(os.getcwd())


################################################## HELP ##################################################

def cmd_help(args):
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    print(f"""
    {BLUE}marketplace{RESET}     {WHITE}Interfaces with the module marketplace{RESET}
    {BLUE}modules{RESET}         {WHITE}List all installed modules{RESET}
    {BLUE}scripts{RESET}         {WHITE}List all installed scripts{RESET}
    {BLUE}exploits{RESET}        {WHITE}List all installed exploits{RESET}
    {BLUE}exit{RESET}            {WHITE}Exits the framework{RESET}
    """)

################################################## MARKETPLACE ##################################################

def cmd_marketplace(args):
    item_types = {item["type"] for item in marketplace_items}

    if not args:
        list_marketplace_items(marketplace_items, "Marketplace (All Items)")
    elif len(args) == 1:
        if args[0] == "modules":
            list_marketplace_items([item for item in marketplace_items if item["type"] == "module"], "Modules")
        elif args[0] == "scripts":
            list_marketplace_items([item for item in marketplace_items if item["type"] == "script"], "Scripts")
        elif args[0] == "exploits":
            list_marketplace_items([item for item in marketplace_items if item["type"] == "exploit"], "Exploits")
        elif args[0] in item_types:
            list_marketplace_items([item for item in marketplace_items if item["type"] == args[0]], args[0].capitalize())
        else:
            print(f"Error: Unknown argument '{args[0]}'. Valid types are {', '.join(item_types)}.")
    elif len(args) >= 2:
        if args[0] == "search":
            if args[1] in item_types:
                search_items_by_type(args[1], " ".join(args[2:]))
            else:
                search_items(" ".join(args[1:]))
        elif args[0] == "install":
            cmd_install(args[1:])
        else:
            print("Error: Invalid command format. Use 'marketplace [modules|scripts|exploits]' or 'marketplace search <term>' or 'marketplace install <item_id>'.")
    else:
        print("Error: Invalid command format.")

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

################################################## MODULES ##################################################

def cmd_modules(args):
    installed_modules_path = os.path.join(os.getcwd(), "modules")
    installed_modules = []

    for item in marketplace_items:
        if item["type"] == "module":
            module_path = os.path.join(installed_modules_path, item["folder"])
            if os.path.exists(module_path):
                installed_modules.append(item)

    if installed_modules:
        for item in installed_modules:
            print(f"\033[94mID: {item['id']}\033[0m")
            print(f"Module: \033[92m{item['name']}\033[0m")
            print(f"Description: {item['description']}\n")
    else:
        print("\033[91mNo installed modules found.\033[0m")


################################################## SCRIPTS ##################################################

def cmd_scripts(args):
    installed_scripts_path = os.path.join(os.getcwd(), "scripts")
    installed_scripts = []

    for item in marketplace_items:
        if item["type"] == "script":
            script_path = os.path.join(installed_scripts_path, item["folder"])
            if os.path.exists(script_path):
                installed_scripts.append(item)

    if installed_scripts:
        for item in installed_scripts:
            print(f"\033[94mID: {item['id']}\033[0m")
            print(f"Script: \033[92m{item['name']}\033[0m")
            print(f"Description: {item['description']}\n")
    else:
        print("\033[91mNo installed scripts found.\033[0m")


################################################## EXPLOITS ##################################################

def cmd_exploits(args):
    installed_exploits_path = os.path.join(os.getcwd(), "exploits")
    installed_exploits = []

    for item in marketplace_items:
        if item["type"] == "exploit":
            exploit_path = os.path.join(installed_exploits_path, item["folder"])
            if os.path.exists(exploit_path):
                installed_exploits.append(item)

    if installed_exploits:
        for item in installed_exploits:
            print(f"\033[94mID: {item['id']}\033[0m")
            print(f"Exploit: \033[92m{item['name']}\033[0m")
            print(f"Description: {item['description']}\n")
    else:
        print("\033[91mNo installed exploits found.\033[0m")

################################################## EXECUTE ##################################################

def cmd_execute(args):
    if len(args) == 1:
        item_id = args[0]
        execute_item(item_id)
    else:
        print("Error: Invalid command format. Use 'execute <item_id>'.")

################################################## UPDATE ##################################################

def cmd_update(args):
    if len(args) == 1:
        item_id = args[0]
        
        item = next((i for i in marketplace_items if i["id"] == item_id), None)
        
        if item:
            if item["type"] == "module":
                install_path = os.path.join(os.getcwd(), "modules", item["folder"])
            elif item["type"] == "script":
                install_path = os.path.join(os.getcwd(), "scripts", item["folder"])
            elif item["type"] == "exploit":
                install_path = os.path.join(os.getcwd(), "exploits", item["folder"])
            else:
                print(f"Error: Unknown item type '{item['type']}'")
                return

            if os.path.exists(install_path):
                try:
                    shutil.rmtree(install_path)
                    print(f"\033[92mDeleted old {item['name']} from {install_path}\033[0m")
                except Exception as e:
                    print(f"\033[91mError: Failed to delete the old version of {item['name']}. {e}\033[0m")
            
            print(f"\033[92mReinstalling {item['name']}...\033[0m")
            try:
                subprocess.run(["git", "clone", item["url"], install_path], check=True)
                print(f"\033[92mSuccessfully reinstalled {item['name']} to folder: {install_path}\033[0m")
            except subprocess.CalledProcessError as e:
                print(f"\033[91mError: Failed to reinstall {item['name']}. Git clone failed. {e}\033[0m")
        else:
            print(f"Error: Item with ID {item_id} not found.")
    else:
        print("Error: Invalid command format. Use 'update <item_id>'.")

################################################## DELETE ##################################################

def cmd_delete(args):
    if len(args) == 1:
        item_id = args[0]
        
        item = next((i for i in marketplace_items if i["id"] == item_id), None)
        
        if item:
            if item["type"] == "module":
                install_path = os.path.join(os.getcwd(), "modules", item["folder"])
            elif item["type"] == "script":
                install_path = os.path.join(os.getcwd(), "scripts", item["folder"])
            elif item["type"] == "exploit":
                install_path = os.path.join(os.getcwd(), "exploits", item["folder"])
            else:
                print(f"Error: Unknown item type '{item['type']}'")
                return

            if os.path.exists(install_path):
                try:
                    shutil.rmtree(install_path)
                    print(f"\033[92mSuccessfully deleted {item['name']} from {install_path}\033[0m")
                except Exception as e:
                    print(f"\033[91mError: Failed to delete {item['name']}. {e}\033[0m")
            else:
                print(f"\033[91mError: {item['name']} is not installed.\033[0m")
        else:
            print(f"Error: Item with ID {item_id} not found.")
    else:
        print("Error: Invalid command format. Use 'delete <item_id>'.")

################################################## EXIT ##################################################

def cmd_exit(args):
    print("Exiting ZeroToolkit. Goodbye!")
    exit(0)