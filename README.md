# AES File Embed/Extract

This project allows you to embed and extract files or strings within other files using AES encryption.

## Installing dependencies

First, make sure you have all the necessary dependencies installed:

```bash
pip install pycryptodome
```

## Use as a command tool

### Embedding a file in a storage file

To embed a file within another file using AES encryption, run the command:

```bash
mymra embed <input_file> <host_file> <output_file> -p <password>
```

**Options**:
- `<input_file>` — path to the file that needs to be embedded.
- `<host_file>` — path to the storage file that will contain the embedded file.
- `<output_file>` — path to save the file with embedded data.
- `-p <password>` - (optional) encryption password (default: `RAMRANCHREALLYROCKS`)

### Retrieving a file from file storage

To retrieve a file from storage using AES encryption, run the command:

```bash
mymra extract <host_file> -p <password>
```

**Options**:
- `<host_file>` — path to the storage file containing embedded data.
- `-p <password>` - (optional) decryption password (default: `RAMRANCHREALLYROCKS`)

## Example as a library

You can use the file embedding and extracting functionality as a library by importing the appropriate functions.

First, install it. Run

```bash
pip install .
```

now you can work with it like with a library

```python
from mymra import embed_file, extract_file

# Example of embedding a file
embed_file('123.mp4', '123.png', '1488.png', 'COCKER')

# Example of extracting a file
extract_file('1488.png', 'COCKER')
```

## Example as cmd

1. Embed the file `123.mp4` into the file `123.png` with the password `COCKER` and save it in `1488.png`:

```bash
mymra embed 123.mp4 123.png 1488.png -p COCKER
```

2. Extract the file from `1488.png` with the password `COCKER`:

```bash
mymra extract 1488.png -p COCKER
```


### Embedding a string in a storage file

To embed a string within another file using AES encryption, run the command:

```bash
mymra embed_string <input_string> <host_file> <output_file> -p <password>
```

**Options**:
- `<input_string>` — the string to embed.
- `<host_file>` — path to the storage file that will contain the embedded string.
- `<output_file>` — path to save the file with embedded data.
- `-p <password>` - (optional) encryption password (default: `RAMRANCHREALLYROCKS`)

### Retrieving a string from a storage file

To retrieve an embedded string from storage using AES decryption, run the command:

```bash
mymra extract_string <host_file> -p <password>
```

**Options**:
- `<host_file>` — path to the storage file containing the embedded string.
- `-p <password>` - (optional) decryption password (default: `RAMRANCHREALLYROCKS`)

### Removing embedded data from a file

To remove all embedded data from a file and restore it to its original state, run the command:

```bash
mymra deembed <host_file> <output_file>
```

**Options**:
- `<host_file>` — path to the storage file containing embedded data.
- `<output_file>` — path to save the cleaned file.

More detailed examples in test.py