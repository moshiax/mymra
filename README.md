
# AES File Embed/Extract

This project allows you to embed and extract files or strings within other files using AES encryption.

## Installation

Install the necessary dependencies:

```bash
pip install pycryptodome
```

## Usage Examples

### Library Functions

#### Embedding a File
Embed a file into a host file:

```python
from mymra import embed_file

output_path = embed_file(
    input_file_path='123.mp4',  # File to embed
    host_file_path='123.png',   # Host file
    output_file_path='1488.png',  # Path to save file with embedded data
    password='COCKER',          # Optional password
    marker='ITSTEST'            # Optional marker
)

print(output_path)
```

#### Extracting a File
Extract an embedded file from a host file:

```python
from mymra import extract_file

output_path = extract_file(
    host_file_path='1488.png',  # File containing embedded data
    password='COCKER',          # Optional password
    marker='ITSTEST'            # Optional marker
)

print(output_path)
```

#### Embedding a string
Embed a string into a host file:

```python
from mymra import embed_string

file_path = embed_string(
    input_string='secret',  # String to embed
    host_file_path='123.png',      # Host file
    output_file_path='output.png', # Path to save file with embedded string
    password='COCKER',             # Optional password
    marker='ITSTEST'          # Optional marker
)

print(file_path)
```

#### Extracting a string
Extract a string from file:

```python
from mymra import extract_string

string = extract_string(
    host_file_path='output.png',      # File with embedded string
    password='COCKER',             # Optional password
    marker='ITSTEST'          # Optional marker
)

print(string)
```

#### Deembedding
Removes embedded data from a file

```python
from mymra import deembed_file

output_path = deembed_file(
    host_file_path='123.png',      # File with embedded data
	output_file_path='321.png', # Path to save file
    password='COCKER',             # Optional password
    marker='ITSTEST'          # Optional marker
)

print(output_path)
```

### Command-Line Interface

#### Embedding a File
Embed a file with optional arguments:
```bash
mymra embed 123.mp4 123.png 1488.png -p COCKER -m ITSTEST
```

#### Extracting a File
Extract an embedded file using optional arguments:
```bash
mymra extract 1488.png -p COCKER -m ITSTEST
```

#### Embedding a String
Embed a string into a host file:
```bash
mymra embed_string "Secret Data" 123.png string_embedded.png -p COCKER -m ITSTEST
```

#### Extracting a String
Extract a string from a host file:
```bash
mymra extract_string string_embedded.png -p COCKER -m ITSTEST
```

#### Removing Embedded Data
Remove embedded data from a file:
```bash
mymra deembed 1488.png cleaned_123.png -m ITSTEST
```