#import library elements
from colorama import init, Fore, Back, Style
#initialize colorama for cross-platform colored terminal output
init()
#print colored Hello World
print(f"{Fore.RED}{Back.YELLOW}Hello World!{Style.RESET_ALL}")
print(f"{Fore.GREEN}Hello World in Green!{Style.RESET_ALL}")
print(f"{Fore.BLUE}{Style.BRIGHT}Hello World in Bright"
      f"Blue!{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Back.CYAN}Hello World with Magenta text and Cyan background!{Style.RESET_ALL}")
