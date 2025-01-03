import os
from colorama import Fore, Style, init
from mymra import embed_file, extract_file, embed_string, extract_string, deembed_file

init()

# Example of embedding a file
try:
    embed_file('123.mp4', '123.png', '1488.png', 'COCKER')
    print(f"{Fore.GREEN}Embedding a file - Successful{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Embedding a file - Failed! Error: {e}{Style.RESET_ALL}")

# Example of extracting a file
try:
    extract_file('1488.png', 'COCKER')
    print(f"{Fore.GREEN}Extracting a file - Successful{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Extracting a file - Failed! Error: {e}{Style.RESET_ALL}")

# Example of embedding a string
try:
    embed_string('This is a secret string', '123.png', 'string_embedded.png', 'COCKER')
    print(f"{Fore.GREEN}Embedding a string - Successful{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Embedding a string - Failed! Error: {e}{Style.RESET_ALL}")

# Example of extracting a string
try:
    extract_string('string_embedded.png', 'COCKER')
    print(f"{Fore.GREEN}Extracting a string - Successful{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Extracting a string - Failed! Error: {e}{Style.RESET_ALL}")

# Example of removing embedded data
try:
    deembed_file('1488.png', 'cleaned_123.png')
    print(f"{Fore.GREEN}Removing embedded data - Successful{Style.RESET_ALL}")
except Exception as e:
    print(f"{Fore.RED}Removing embedded data - Failed! Error: {e}{Style.RESET_ALL}")

try:
    os.remove('cleaned_123.png')
    os.remove('1488.png')
    os.remove('string_embedded.png')
except OSError as e:
    print(f"{Fore.YELLOW}Warning: {e}{Style.RESET_ALL}")
