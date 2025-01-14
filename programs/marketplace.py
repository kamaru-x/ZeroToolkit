from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class Color:
    """ANSI color codes for consistent styling"""
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

# Define available types with their plural forms
ITEM_TYPES: Dict[str, str] = {
    "module": "modules",
    "script": "scripts",
    "exploit": "exploits"
}

@dataclass
class MarketplaceItem:
    """Structure for marketplace items"""
    id: str
    name: str
    description: str
    url: str
    type: str
    folder: str
    start: str
    superuser: bool = False

marketplace_items: List[MarketplaceItem] = [
    MarketplaceItem(
        id="mapper",
        name="Network Mapper",
        description="Find device in a network",
        url="https://gitlab.com/marketplace7420103/scripts/mapper.git",
        type="script",
        folder="mapper",
        start="mapper.py",
        superuser=True
    )
]

def get_plural_name(item_type: str) -> str:
    """Get plural form of item type"""
    return ITEM_TYPES.get(item_type, f"{item_type}s")

def is_valid_type(item_type: str) -> bool:
    """Check if item type is valid"""
    return item_type in ITEM_TYPES

def list_marketplace_items(items: List[MarketplaceItem], title: str) -> None:
    """Display marketplace items in a stylized box format"""
    c = Color
    divider = "─" * 100

    print(f"\n{divider}")
    print(f"{c.GREEN}{title.center(100)}{c.RESET}")
    print(f"{divider}\n")

    for item in items:
        print(f"{c.CYAN}❯ {c.YELLOW}ID{c.RESET}: {item.id}")
        print(f"{c.CYAN}├─{c.YELLOW}Name{c.RESET}: {c.BLUE}{item.name}{c.RESET}")
        print(f"{c.CYAN}├─{c.YELLOW}Type{c.RESET}: {item.type}")
        print(f"{c.CYAN}└─{c.YELLOW}Description{c.RESET}: {item.description}")
        print()