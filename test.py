import os
import sys
from colorama import Fore, Style, init
from mymra import embed_file, extract_file, embed_string, extract_string, deembed_file
from io import StringIO
from contextlib import redirect_stdout

init()

def print_message(message):
    if "failed" in message.lower():
        print(f"{Fore.RED}{message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def capture_and_print(func, *args, **kwargs):
    output = StringIO()
    with redirect_stdout(output): 
        func(*args, **kwargs)
    output_message = output.getvalue()
    if "failed" in output_message.lower():
        print(f"{Fore.RED}{output_message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}{output_message}{Style.RESET_ALL}")
    output.close()

# Example of embedding a file
print_message("Embedding a file...")
capture_and_print(embed_file, '123.mp4', '123.png', '1488.png', 'COCKER')

# Example of extracting a file
print_message("Extracting a file...")
capture_and_print(extract_file, '1488.png', 'COCKER')

# Example of embedding a string
print_message("Embedding a string...")
capture_and_print(embed_string, 'This is a secret string', '123.png', 'string_embedded.png', 'COCKER')

# Example of extracting a string
print_message("Extracting a string...")
capture_and_print(extract_string, 'string_embedded.png', 'COCKER')

# Example of removing embedded data
print_message("Removing embedded data...")
capture_and_print(deembed_file, '1488.png', 'cleaned_123.png')

os.remove('cleaned_123.png')
os.remove('1488.png')
os.remove('string_embedded.png')
