import os
import shutil
import subprocess
from programs.marketplace import (marketplace_items, list_marketplace_items, 
                                ITEM_TYPES, is_valid_type, get_plural_name)

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


################################################## HELP ##################################################

def cmd_help(args):
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    print(f"""
    {BLUE}marketplace{RESET}                        {WHITE}Interfaces with the module marketplace{RESET}

    {BLUE}list{RESET}                               {WHITE}List installed items (usage: list <type>){RESET}

    {BLUE}install{RESET}                            {WHITE}Install an item from marketplace (usage: install <item_id>){RESET}

    {BLUE}execute{RESET}                            {WHITE}Execute an installed item (usage: execute <item_id>){RESET}

    {BLUE}update{RESET}                             {WHITE}Update an installed item (usage: update <item_id>){RESET}

    {BLUE}delete{RESET}                             {WHITE}Remove an installed item (usage: delete <item_id>){RESET}

    {BLUE}clear{RESET}                              {WHITE}Clear the terminal screen{RESET}

    {BLUE}exit{RESET}                               {WHITE}Exit the framework{RESET}
    """)

################################################## MARKETPLACE ##################################################

def cmd_marketplace(args):
    if not args:
        list_marketplace_items(marketplace_items, "Marketplace (All Items)")
        return

    cmd = args[0]
    if len(args) == 1:
        # Remove 's' from plural form if present
        type_singular = cmd[:-1] if cmd.endswith('s') else cmd
        if is_valid_type(type_singular):
            filtered_items = [item for item in marketplace_items if item["type"] == type_singular]
            list_marketplace_items(filtered_items, get_plural_name(type_singular).capitalize())
        else:
            print(f"Error: Unknown type '{cmd}'. Valid types are: {', '.join(ITEM_TYPES.values())}")
    elif len(args) >= 2:
        if cmd == "search":
            search_term = " ".join(args[1:])
            filtered_items = [
                item for item in marketplace_items 
                if search_term.lower() in item["name"].lower()
            ]
            if filtered_items:
                list_marketplace_items(filtered_items, f"Search Results for '{search_term}'")
            else:
                print(f"\033[91mNo items found matching '{search_term}'\033[0m")
        elif is_valid_type(cmd):
            search_term = " ".join(args[1:])
            filtered_items = [
                item for item in marketplace_items 
                if item["type"] == cmd and search_term.lower() in item["name"].lower()
            ]
            if filtered_items:
                list_marketplace_items(filtered_items, f"Search Results for '{search_term}' in {get_plural_name(cmd)}")
            else:
                print(f"\033[91mNo {get_plural_name(cmd)} found matching '{search_term}'\033[0m")
        else:
            print("Error: Invalid command format. Use:")
            print("  marketplace")
            print("  marketplace <type>")
            print("  marketplace search <term>")
            print("  marketplace <type> <search_term>")

################################################## INSTALL ##################################################

def cmd_install(args):
    if len(args) == 1:
        item_id = args[0]
        
        item = next((i for i in marketplace_items if i["id"] == item_id), None)
        
        if item:
            print(f"\033[92mInstalling {item['name']}...\033[0m")
            
            type_to_folder = {item_type: get_plural_name(item_type) for item_type in ITEM_TYPES}
            
            install_type = item["type"]
            if install_type not in type_to_folder:
                print(f"Error: Unknown item type '{install_type}'")
                return

            # Use the project directory for installation
            install_path = os.path.join(PROJECT_DIR, type_to_folder[install_type], item["folder"])
            
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


################################################## LIST ##################################################

def cmd_list(args):
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    RESET = "\033[0m"

    if len(args) != 1:
        print(f"{RED}Error: Usage: list <type>{RESET}")
        print(f"{RED}Valid types: {', '.join(ITEM_TYPES.values())}{RESET}")
        return

    item_type = args[0][:-1] if args[0].endswith('s') else args[0]
    if not is_valid_type(item_type):
        print(f"{RED}Error: Unknown type '{args[0]}'. Valid types are: {', '.join(ITEM_TYPES.values())}{RESET}")
        return

    query_type = item_type
    installed_path = os.path.join(PROJECT_DIR, get_plural_name(item_type))
    installed_items = []

    for item in marketplace_items:
        if item["type"] == query_type:
            item_path = os.path.join(installed_path, item["folder"])
            if os.path.exists(item_path):
                installed_items.append(item)

    if installed_items:
        print("\n" + "─" * 100)
        print(f"{GREEN}Installed {get_plural_name(item_type).capitalize()}{RESET}".center(100))
        print("─" * 100 + "\n")
        
        for item in installed_items:
            print(f"{CYAN}❯ {YELLOW}ID{RESET}: {item['id']}")
            print(f"{CYAN}├─{YELLOW}Name{RESET}: {BLUE}{item['name']}{RESET}")
            print(f"{CYAN}├─{YELLOW}Type{RESET}: {item['type']}")
            print(f"{CYAN}└─{YELLOW}Description{RESET}: {item['description']}")
            print()
    else:
        print(f"{RED}No installed {get_plural_name(item_type)} found.{RESET}")

################################################## EXECUTE ##################################################

def cmd_execute(args):
    if len(args) == 1:
        item_id = args[0]
        item = next((i for i in marketplace_items if i["id"] == item_id), None)
        
        if item:
            print(f"\033[92mExecuting {item['name']}...\033[0m")
            
            type_to_folder = {item_type: get_plural_name(item_type) for item_type in ITEM_TYPES}
            folder_name = type_to_folder.get(item["type"])
            
            if not folder_name:
                print(f"Error: Unknown item type '{item['type']}'")
                return
            
            exec_path = os.path.join(PROJECT_DIR, folder_name, item["folder"], item["start"])
            
            if os.path.exists(exec_path):
                try:
                    command = ["python", exec_path]
                    
                    # Check if superuser is required
                    if item.get("superuser", False):
                        command.insert(0, "sudo")
                    
                    print(f"Running command: {' '.join(command)}")
                    subprocess.run(command, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error: Failed to execute {item['name']}. {e}")
            else:
                print(f"Error: {item['start']} not found in the specified path: {exec_path}")
        else:
            print(f"Error: Item with ID {item_id} not found.")
    else:
        print("Error: Invalid command format. Use 'execute <item_id>'.")

################################################## UPDATE ##################################################

def cmd_update(args):
    if len(args) == 1:
        item_id = args[0]
        
        item = next((i for i in marketplace_items if i["id"] == item_id), None)
        
        if item:
            install_path = os.path.join(PROJECT_DIR, get_plural_name(item["type"]), item["folder"])

            print(f"Install Path: {install_path}")

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
            install_path = os.path.join(PROJECT_DIR, get_plural_name(item["type"]), item["folder"])

            print(f"Install Path: {install_path}")

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


################################################## CLEAR ##################################################

def cmd_clear(args):
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        print("Error: Unsupported OS")

################################################## EXIT ##################################################

def cmd_exit(args):
    print("Exiting ZeroToolkit. Goodbye!")
    exit(0)