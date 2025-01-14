#!/usr/bin/env python

from typing import Dict, Callable, List
import platform
if platform.system() == "Linux":
    import readline
from programs.commands import (cmd_help, cmd_marketplace, cmd_install, cmd_list, cmd_execute, cmd_update, cmd_delete, cmd_exit, cmd_clear)
from programs.marketplace import Color

class ZeroToolkit:
    """Main toolkit class handling command execution and user interaction"""

    def __init__(self) -> None:
        self.workspace: str = "executer"
        self.prompt: str = f"{Color.YELLOW}[zerotoolkit][{self.workspace}] > {Color.RESET}"
        self.commands: Dict[str, Callable] = {
            "help": cmd_help,
            "marketplace": cmd_marketplace,
            "install": cmd_install,
            "list": cmd_list,
            "execute": cmd_execute,
            "update": cmd_update,
            "delete": cmd_delete,
            "clear": cmd_clear,
            "exit": cmd_exit
        }
        self.setup_readline()

    def setup_readline(self) -> None:
        """Configure readline for command history if on Linux"""
        if platform.system() == "Linux":
            readline.set_history_length(1000)
            readline.parse_and_bind('tab: complete')

    def display_banner(self) -> None:
        """Display the toolkit banner"""
        banner = f"""
        {Color.GREEN}
        ███████╗███████╗██████╗  ██████╗ ██╗  ██╗██████╗ ██╗      ██████╗ ██╗████████╗
        ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██║╚══██╔══╝
          ███╔╝ █████╗  ██████╔╝██║   ██║ ╚███╔╝ ██████╔╝██║     ██║   ██║██║   ██║
         ███╔╝  ██╔══╝  ██╔══██╗██║   ██║ ██╔██╗ ██╔═══╝ ██║     ██║   ██║██║   ██║
        ███████╗███████╗██║  ██║╚██████╔╝██╔╝ ██╗██║     ███████╗╚██████╔╝██║   ██║
        ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝   ╚═╝
        {Color.RESET}
        {Color.GREEN}Developed by Kamarudheen{Color.RESET}
        """
        print(banner)

    def execute_command(self, cmd: str, args: List[str]) -> None:
        """Execute a command with its arguments"""
        if cmd in self.commands:
            try:
                self.commands[cmd](args)
            except Exception as e:
                print(f"{Color.RED}Error executing command: {e}{Color.RESET}")
        else:
            print(f"{Color.RED}Unknown command: {cmd}. Use 'help' for available commands.{Color.RESET}")

    def run(self) -> None:
        """Main execution loop"""
        self.display_banner()

        while True:
            try:
                command = input(self.prompt).strip()
                if not command:
                    continue

                cmd_parts = command.split()
                cmd, args = cmd_parts[0], cmd_parts[1:]
                self.execute_command(cmd, args)

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except EOFError:
                print("\nExiting ZeroToolkit. Goodbye!")
                break
            except Exception as e:
                print(f"{Color.RED}Unexpected error: {e}{Color.RESET}")

def main() -> None:
    """Entry point of the application"""
    toolkit = ZeroToolkit()
    toolkit.run()

if __name__ == "__main__":
    main()