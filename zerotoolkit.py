#!/usr/bin/env python

from programs.commands import (
    cmd_back,
    cmd_dashboard,
    cmd_db,
    cmd_exit,
    cmd_help,
    cmd_index,
    cmd_keys,
    cmd_marketplace,
    cmd_modules,
    cmd_options,
    cmd_pdb,
    cmd_script,
    cmd_shell,
    cmd_show,
    cmd_snapshots,
    cmd_spool,
    cmd_workspaces,
)

class ZeroToolkit:
    GREEN = "\033[92m"   # Green color for banner
    YELLOW = "\033[93m"  # Yellow color for prompt
    RED = "\033[91m"     # Red color for error messages
    RESET = "\033[0m"    # Reset color to default

    def __init__(self):
        self.current_workspace = "default"
        self.prompt = f"{self.YELLOW}[zerotoolkit][{self.current_workspace}] > {self.RESET}"
        self.commands = {
            "back": cmd_back,
            "dashboard": cmd_dashboard,
            "db": cmd_db,
            "exit": cmd_exit,
            "help": cmd_help,
            "index": cmd_index,
            "keys": cmd_keys,
            "marketplace": cmd_marketplace,
            "modules": cmd_modules,
            "options": cmd_options,
            "pdb": cmd_pdb,
            "script": cmd_script,
            "shell": cmd_shell,
            "show": cmd_show,
            "snapshots": cmd_snapshots,
            "spool": cmd_spool,
            "workspaces": cmd_workspaces,
        }

    def display_banner(self):
        banner = f"""
        {self.GREEN}
        ███████╗███████╗██████╗  ██████╗ ████████╗ ██████╗  ██████╗ ██╗     ██╗  ██╗██╗████████╗
        ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██║ ██╔╝██║╚══██╔══╝
          ███╔╝ █████╗  ██████╔╝██║   ██║   ██║   ██║   ██║██║   ██║██║     █████╔╝ ██║   ██║   
         ███╔╝  ██╔══╝  ██╔══██╗██║   ██║   ██║   ██║   ██║██║   ██║██║     ██╔═██╗ ██║   ██║   
        ███████╗███████╗██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝███████╗██║  ██╗██║   ██║   
        ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   
        {self.RESET}
        {self.GREEN}Developed by Kamarudheen{self.RESET}
        """
        print(banner)

    def run(self):
        """Main loop for the CLI."""
        self.display_banner()
        while True:
            try:
                command = input(self.prompt).strip()
                if not command:
                    continue
                cmd_parts = command.split()
                cmd = cmd_parts[0]
                args = cmd_parts[1:]

                if cmd in self.commands:
                    self.commands[cmd](args)
                else:
                    print(f"{self.RED}Unknown command: {cmd}.{self.RESET}")
            except KeyboardInterrupt:
                print("\nExiting ZeroToolkit. Goodbye!")
                break


if __name__ == "__main__":
    toolkit = ZeroToolkit()
    toolkit.run()