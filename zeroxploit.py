#!/usr/bin/env python

from programs.commands import (cmd_help, cmd_marketplace, cmd_install, cmd_modules, cmd_scripts, cmd_exploits, cmd_execute, cmd_update, cmd_delete, cmd_exit)

class ZeroToolkit:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"

    def __init__(self):
        self.workspace = "executer"
        self.prompt = f"{self.YELLOW}[zerotoolkit][{self.workspace}] > {self.RESET}"
        self.commands = {
            "help": cmd_help, "marketplace": cmd_marketplace, "install": cmd_install, "exit": cmd_exit, "modules": cmd_modules, "scripts": cmd_scripts, 
            "exploits": cmd_exploits, "execute" : cmd_execute, "update": cmd_update, "delete": cmd_delete
        }

    def display_banner(self):
        banner = f"""
        {self.GREEN}
        ███████╗███████╗██████╗  ██████╗ ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
        ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
          ███╔╝ █████╗  ██████╔╝██║   ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║   
         ███╔╝  ██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║   
        ███████╗███████╗██║  ██║╚██████╔╝██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║   
        ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝                                                                            
        {self.RESET}
        {self.GREEN}Developed by Kamarudheen{self.RESET}
        """
        print(banner)

    def run(self):
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