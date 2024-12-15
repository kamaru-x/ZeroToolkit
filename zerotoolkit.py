#!/usr/bin/env python

from pyfiglet import Figlet
from termcolor import colored
import time
import subprocess

def display_banner():
    figlet = Figlet(font='ansi_shadow', width=200)
    ascii_art = figlet.renderText("ZEROTOOLKIT")

    # Stylization
    line = "=" * 100
    tagline = "Your Ultimate Penetration Testing Toolkit"
    footer = "Stay ethical, stay secure!"

    print(colored(line, 'green', attrs=['bold']))
    print()  # Blank line for spacing
    print(colored(ascii_art, 'cyan', attrs=['bold']))
    print()  # Blank line for spacing
    print(colored(tagline.center(100), 'yellow'))
    print(colored(footer.center(100), 'magenta'))
    print(colored(line, 'green', attrs=['bold']))

def main():
    display_banner()

    menu_options = {
        1: "Network",
        2: "Web Application"
    }

    print("Select an option for penetration testing:")

    for key, value in menu_options.items():
        print(f"{key}. {value}")

    try:
        choice = int(input("\nEnter your choice (1-2): "))
        if choice == 1:
            subprocess.run(["python", "./programs/network.py"])
        elif choice == 2:
            subprocess.run(["python", "./programs/webapp.py"])
        else:
            print("Invalid choice. Please run the program again.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 2.")

if __name__ == "__main__":
    main()