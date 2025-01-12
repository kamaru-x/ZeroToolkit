# marketplace.py

marketplace_items = [
    {"id": "mapper", "name": "Network Mapper", "description": "Find device in a network", "url": "https://github.com/kamaru-x/Scanner.git", "type": "script", "language": "python", "folder": "mapper", "start": "scanner.py", "superuser": True},
]

def list_marketplace_items(items, title):
    print("\n")
    print(f"\033[92m{title.center(60)}\033[0m")
    headers = ["ID", "Name", "Type", "Description"]
    rows = [[item["id"], item["name"], item["type"], item["description"]] for item in items]
    print_table(rows, headers)
    print("\n")

def print_table(rows, headers):
    column_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + rows))]
    column_widths = [width + 2 for width in column_widths]

    def format_row(row):
        return " │ " + " │ ".join(f" {str(item).ljust(width)}" for item, width in zip(row, column_widths)) + " │"

    def print_divider(char="─"):
        print("   " + char * (sum(column_widths) + 3 * len(headers) + 1))

    print_divider("═")
    print(format_row(headers))
    print_divider()

    for row in rows:
        print(format_row(["" for _ in headers]))
        print(format_row(row))
        print(format_row(["" for _ in headers]))
        print_divider()