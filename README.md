
# Mymra

This project allows you to embed and extract files or strings within other files using AES encryption.

## Installation

Install library:

```bash
pip install mymra
```

## Usage Examples

### Library Functions

#### Embedding a File
Embed a file into a host file:

```python
from mymra import embed_file

embed_file(
    input_file_path='123.mp4',    # File to embed
    host_file_path='123.png',     # Host file
    output_file_path='1488.png',  # Optional path to save result file
    password='COCKER',            # Optional password
    marker='ITSTEST'              # Optional marker
	xor_key='123'                 # Optional XOR-key for marker encryption
)

```

#### Extracting a File
Extract an embedded file from a host file:

```python
from mymra import extract_file

output_path = extract_file(
    host_file_path='1488.png',  # File containing embedded data
    password='COCKER',          # Optional password
    marker='ITSTEST'            # Optional marker
	xor_key='123'               # Optional XOR-key for marker encryption
)

print(output_path)
```

#### Embedding a string
Embed a string into a host file:

```python
from mymra import embed_string

embed_string(
    input_string='secret',         # String to embed
    host_file_path='123.png',      # Host file
    output_file_path='output.png', # Optional path to save result file
    password='COCKER',             # Optional password
    marker='ITSTEST'               # Optional marker
	xor_key='123'                  # Optional XOR-key for marker encryption
)

```

#### Extracting a string
Extract a string from file:

```python
from mymra import extract_string

string = extract_string(
    host_file_path='output.png',      # File with embedded string
    password='COCKER',                # Optional password
    marker='ITSTEST'          		  # Optional marker
	xor_key='123'              		  # Optional XOR-key for marker encryption
)

print(string)
```

#### Deembedding
Remove embedded data from a file:

```python
from mymra import deembed_file

deembed_file(
    host_file_path='123.png',      # File with embedded data
    output_file_path='321.png',    # Optional path to save result file
    marker='ITSTEST'               # Optional marker
	xor_key='123'                  # Optional XOR-key for marker encryption
)

```

#### Analyzing a File
Analyze a host file to determine the embedded content type, metadata, or content:

```python
from mymra import analyze_file

# Analyze a file containing an embedded file
result = analyze_file(
    host_file_path='1488.png',  # File containing embedded data
    password='COCKER',          # Optional password
    marker='ITSTEST'            # Optional marker
	xor_key='123'               # Optional XOR-key for marker encryption
)

if result['type'] == 'file':
    print("Embedded file details:")
    print(f"Name: {result['file_name']}")
    print(f"Extension: {result['file_extension']}")
    print(f"Size: {result['file_size']} bytes")
elif result['type'] == 'string':
    print("Embedded string content:")
    print(result['value'])
```

---

### Command-Line Interface

#### Embedding a File
Embed a file with optional arguments:
```bash
mymra embed 123.mp4 123.png -o 1488.png -p COCKER -m ITSTEST -xor 123
```

#### Extracting a File
Extract an embedded file using optional arguments:
```bash
mymra extract 1488.png -p COCKER -m ITSTEST -xor 123
```

#### Embedding a String
Embed a string into a host file:
```bash
mymra embed_string "Secret Data" 123.png -o string_embedded.png -p COCKER -m ITSTEST -xor 123
```

#### Extracting a String
Extract a string from a host file:
```bash
mymra extract_string string_embedded.png -p COCKER -m ITSTEST -xor 123
```

#### Removing Embedded Data
Remove embedded data from a file:
```bash
mymra deembed 1488.png -o cleaned_123.png -m ITSTEST
```

#### Analyzing a File
Analyze a host file to identify embedded content:

- **Analyzing a file containing an embedded file**:
```bash
mymra analyze 1488.png -p COCKER -m ITSTEST -xor 123
```
Expected output:
```
Embedded file details:
Name: example.mp4
Extension: mp4
Size: 1048576 bytes
```

- **Analyzing a file containing an embedded string**:
```bash
mymra analyze string_embedded.png -p COCKER -m ITSTEST -xor 123
```
Expected output:
```
Embedded string content:
This is a secret string
```
