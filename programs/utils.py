from typing import List, Any
from dataclasses import dataclass

@dataclass
class TableConfig:
    """Configuration for table formatting"""
    padding: int = 2
    separator: str = "─"
    header_separator: str = "═"
    vertical: str = "│"

def print_table(rows: List[List[Any]], headers: List[str], config: TableConfig = TableConfig()) -> None:
    """Print formatted table with proper spacing and borders"""
    # Calculate column widths including padding
    column_widths = [
        max(len(str(item)) for item in col) + config.padding
        for col in zip(*([headers] + rows))
    ]

    total_width = sum(column_widths) + len(column_widths) + 1

    def format_row(items: List[Any]) -> str:
        """Format a single row with proper spacing"""
        cells = [
            f"{str(item):{width}}"
            for item, width in zip(items, column_widths)
        ]
        return f" {config.vertical} {f' {config.vertical} '.join(cells)} {config.vertical}"

    def print_divider(char: str = config.separator) -> None:
        """Print horizontal divider"""
        print(f"   {char * total_width}")

    # Print table
    print_divider(config.header_separator)
    print(format_row(headers))
    print_divider()

    for row in rows:
        print(format_row(["" for _ in headers]))
        print(format_row(row))
        print(format_row(["" for _ in headers]))
        print_divider()