import os
import shutil
import subprocess
from typing import List, Optional
from pathlib import Path
from programs.marketplace import (
    marketplace_items, list_marketplace_items, 
    ITEM_TYPES, is_valid_type, get_plural_name,
    Color as c, MarketplaceItem
)

PROJECT_DIR = Path(__file__).parent.parent.absolute()

def get_item_by_id(item_id: str) -> Optional[MarketplaceItem]:
    """Helper function to find item by ID"""
    return next((item for item in marketplace_items if item.id == item_id), None)

def cmd_help(args: List[str]) -> None:
    """Display help information"""
    help_text = f"""
    {c.BLUE}marketplace{c.RESET}                    {c.WHITE}Browse and search available items{c.RESET}
    {c.BLUE}list{c.RESET}                           {c.WHITE}List installed items{c.RESET}
    {c.BLUE}install{c.RESET}                        {c.WHITE}Install an item{c.RESET}
    {c.BLUE}execute{c.RESET}                        {c.WHITE}Execute an installed item{c.RESET}
    {c.BLUE}update{c.RESET}                         {c.WHITE}Update an installed item{c.RESET}
    {c.BLUE}delete{c.RESET}                         {c.WHITE}Remove an installed item{c.RESET}
    {c.BLUE}clear{c.RESET}                          {c.WHITE}Clear screen{c.RESET}
    {c.BLUE}exit{c.RESET}                           {c.WHITE}Exit framework{c.RESET}
    """
    print(help_text)

def cmd_marketplace(args: List[str]) -> None:
    """Handle marketplace operations"""
    if not args:
        list_marketplace_items(marketplace_items, "Marketplace (All Items)")
        return

    cmd = args[0].lower()
    type_singular = cmd[:-1] if cmd.endswith('s') else cmd

    if len(args) == 1:
        if is_valid_type(type_singular):
            filtered_items = [item for item in marketplace_items if item.type == type_singular]
            list_marketplace_items(filtered_items, get_plural_name(type_singular).capitalize())
        else:
            print(f"{c.RED}Error: Unknown type '{cmd}'. Valid types: {', '.join(ITEM_TYPES.values())}{c.RESET}")
    elif len(args) >= 2:
        if cmd == "search":
            search_term = " ".join(args[1:])
            filtered_items = [
                item for item in marketplace_items 
                if search_term.lower() in item.name.lower()
            ]
            if filtered_items:
                list_marketplace_items(filtered_items, f"Search Results for '{search_term}'")
            else:
                print(f"{c.RED}No items found matching '{search_term}'{c.RESET}")
        elif is_valid_type(type_singular):
            search_term = " ".join(args[1:])
            filtered_items = [
                item for item in marketplace_items 
                if item.type == type_singular and search_term.lower() in item.name.lower()
            ]
            if filtered_items:
                list_marketplace_items(filtered_items, f"Search Results for '{search_term}' in {get_plural_name(type_singular)}")
            else:
                print(f"{c.RED}No {get_plural_name(type_singular)} found matching '{search_term}'{c.RESET}")
        else:
            print(f"{c.RED}Invalid command format. Use:{c.RESET}")
            print("  marketplace")
            print("  marketplace <type>")
            print("  marketplace search <term>")
            print("  marketplace <type> <search_term>")

def cmd_install(args: List[str]) -> None:
    """Install an item from marketplace"""
    if len(args) != 1:
        print(f"{c.RED}Error: Usage: install <item_id>{c.RESET}")
        return

    item = get_item_by_id(args[0])
    if not item:
        print(f"{c.RED}Error: Item not found{c.RESET}")
        return

    install_path = PROJECT_DIR / get_plural_name(item.type) / item.folder
    
    print(f"{c.GREEN}Installing {item.name}...{c.RESET}")
    
    if not install_path.exists():
        install_path.mkdir(parents=True)
        print(f"Created folder: {install_path}")

    try:
        subprocess.run(["git", "clone", item.url, str(install_path)], check=True)
        print(f"{c.GREEN}Successfully installed {item.name}{c.RESET}")
    except subprocess.CalledProcessError as e:
        print(f"{c.RED}Installation failed: {e}{c.RESET}")

def cmd_list(args: List[str]) -> None:
    """List installed items of a specific type"""
    if len(args) != 1:
        print(f"{c.RED}Error: Usage: list <type>{c.RESET}")
        print(f"{c.RED}Valid types: {', '.join(ITEM_TYPES.values())}{c.RESET}")
        return

    type_singular = args[0][:-1] if args[0].endswith('s') else args[0]
    if not is_valid_type(type_singular):
        print(f"{c.RED}Error: Unknown type. Valid types: {', '.join(ITEM_TYPES.values())}{c.RESET}")
        return

    installed_path = PROJECT_DIR / get_plural_name(type_singular)
    installed_items = [
        item for item in marketplace_items
        if item.type == type_singular and (installed_path / item.folder).exists()
    ]

    if installed_items:
        list_marketplace_items(installed_items, f"Installed {get_plural_name(type_singular).capitalize()}")
    else:
        print(f"{c.RED}No installed {get_plural_name(type_singular)} found{c.RESET}")

def cmd_execute(args: List[str]) -> None:
    """Execute an installed item"""
    if len(args) != 1:
        print(f"{c.RED}Error: Usage: execute <item_id>{c.RESET}")
        return

    item = get_item_by_id(args[0])
    if not item:
        print(f"{c.RED}Error: Item not found{c.RESET}")
        return

    exec_path = PROJECT_DIR / get_plural_name(item.type) / item.folder / item.start
    
    if not exec_path.exists():
        print(f"{c.RED}Error: {item.start} not found at {exec_path}{c.RESET}")
        return

    try:
        command = ["python", str(exec_path)]
        if item.superuser:
            command.insert(0, "sudo")
            
        print(f"{c.GREEN}Executing {item.name}...{c.RESET}")
        print(f"Command: {' '.join(command)}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{c.RED}Execution failed: {e}{c.RESET}")

def cmd_update(args: List[str]) -> None:
    """Update an installed item"""
    if len(args) != 1:
        print(f"{c.RED}Error: Usage: update <item_id>{c.RESET}")
        return

    item = get_item_by_id(args[0])
    if not item:
        print(f"{c.RED}Error: Item not found{c.RESET}")
        return

    install_path = PROJECT_DIR / get_plural_name(item.type) / item.folder

    if install_path.exists():
        try:
            shutil.rmtree(install_path)
            print(f"{c.GREEN}Removed old version{c.RESET}")
            subprocess.run(["git", "clone", item.url, str(install_path)], check=True)
            print(f"{c.GREEN}Successfully updated {item.name}{c.RESET}")
        except Exception as e:
            print(f"{c.RED}Update failed: {e}{c.RESET}")
    else:
        print(f"{c.RED}Item not installed. Use 'install {item.id}' first{c.RESET}")

def cmd_delete(args: List[str]) -> None:
    """Delete an installed item"""
    if len(args) != 1:
        print(f"{c.RED}Error: Usage: delete <item_id>{c.RESET}")
        return

    item = get_item_by_id(args[0])
    if not item:
        print(f"{c.RED}Error: Item not found{c.RESET}")
        return

    install_path = PROJECT_DIR / get_plural_name(item.type) / item.folder

    if install_path.exists():
        try:
            shutil.rmtree(install_path)
            print(f"{c.GREEN}Successfully deleted {item.name}{c.RESET}")
        except Exception as e:
            print(f"{c.RED}Deletion failed: {e}{c.RESET}")
    else:
        print(f"{c.RED}Item not installed{c.RESET}")

def cmd_clear(args: List[str]) -> None:
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def cmd_exit(args: List[str]) -> None:
    """Exit the framework"""
    print(f"{c.GREEN}Exiting ZeroToolkit. Goodbye!{c.RESET}")
    exit(0)