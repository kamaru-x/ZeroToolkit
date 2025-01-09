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