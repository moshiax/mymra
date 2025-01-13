import argparse
import os
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

defaultmarker = b'MQAZWERPASDZXW'
defaultpassword = 'RAMRANCHREALLYROCKS'

def generate_password_key(password):
    return sha256(password.encode()).digest()

def encrypt_data(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_GCM, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted_data

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_GCM, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    except (ValueError, KeyError) as e:
        raise ValueError("Decryption failed. Possible invalid data or key.") from e
    return decrypted_data

def write_embedded_data(host_data, data_to_embed, marker, output_file_path):
    end_marker = marker[::-1]
    combined_data = host_data + marker + data_to_embed + end_marker
    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)
    return output_file_path

def extract_embedded_data(host_data, marker):
    end_marker = marker[::-1]

    start_marker_index = host_data.find(marker)
    end_marker_index = host_data.find(end_marker)

    if start_marker_index == -1 or end_marker_index == -1 or end_marker_index <= start_marker_index:
        raise ValueError("Required markers not found or improperly placed in the host file. Extraction failed.")

    return host_data[start_marker_index + len(marker):end_marker_index]

def embed_string(input_string, host_file_path, output_file_path, password=None, marker=None):
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker
    elif not isinstance(marker, bytes):
        marker = marker.encode()

    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    if marker in host_data:
        raise ValueError("The file already contains embedded data.")

    encrypted_data = encrypt_data(input_string.encode(), key)
    return write_embedded_data(host_data, encrypted_data, marker, output_file_path)

def embed_file(input_file_path, host_file_path, output_file_path, password=None, marker=None):
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker
    elif not isinstance(marker, bytes):
        marker = marker.encode()

    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    if marker in host_data:
        raise ValueError("The file already contains embedded data.")

    with open(input_file_path, 'rb') as input_file:
        input_data = input_file.read()

    file_name = os.path.splitext(os.path.basename(input_file_path))[0] 
    file_extension = os.path.splitext(input_file_path)[1][1:] or 'noextension'
    metadata = f"{file_name}:{file_extension}".encode()

    encrypted_metadata = encrypt_data(metadata, key)
    encrypted_data = encrypt_data(input_data, key)

    combined_data = encrypted_metadata + marker + encrypted_data
    return write_embedded_data(host_data, combined_data, marker, output_file_path)

def extract_string(host_file_path, password=None, marker=None):
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker
    elif not isinstance(marker, bytes):
        marker = marker.encode()

    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    encrypted_data = extract_embedded_data(host_data, marker)
    decrypted_data = decrypt_data(encrypted_data, key)

    if decrypted_data is None:
        raise ValueError("Failed to decrypt data with the given password.")

    return decrypted_data.decode()

def extract_file(host_file_path, password=None, marker=None):
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker
    elif not isinstance(marker, bytes):
        marker = marker.encode()

    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    encrypted_combined_data = extract_embedded_data(host_data, marker)
    metadata_marker_index = encrypted_combined_data.find(marker)

    if metadata_marker_index == -1:
        raise ValueError("Metadata marker not found. Extraction failed.")

    encrypted_metadata = encrypted_combined_data[:metadata_marker_index]
    encrypted_data = encrypted_combined_data[metadata_marker_index + len(marker):]

    decrypted_metadata = decrypt_data(encrypted_metadata, key)
    if decrypted_metadata is None:
        raise ValueError("Failed to decrypt metadata.")

    try:
        file_name, file_extension = decrypted_metadata.decode().split(':')
    except ValueError:
        raise ValueError("Invalid metadata format.")

    if not file_extension or file_extension == 'noextension':
        output_file_name = file_name
    else:
        if file_name.lower().endswith(f".{file_extension.lower()}"):
            output_file_name = file_name
        else:
            output_file_name = f"{file_name}.{file_extension}"

    decrypted_data = decrypt_data(encrypted_data, key)
    if decrypted_data is None:
        raise ValueError("Failed to decrypt data.")

    output_path = os.path.join(os.path.dirname(host_file_path), output_file_name)

    with open(output_path, 'wb') as output_file:
        output_file.write(decrypted_data)

    return output_path

def analyze_file(host_file_path, password=None, marker=None):

    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker
    elif not isinstance(marker, bytes):
        marker = marker.encode()

    key = generate_password_key(password)
    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    try:
        encrypted_combined_data = extract_embedded_data(host_data, marker)
    except ValueError as e:
        raise ValueError(f"No embedded data found: {e}")
    
    metadata_marker_index = encrypted_combined_data.find(marker)
    if metadata_marker_index != -1:
        encrypted_metadata = encrypted_combined_data[:metadata_marker_index]
        encrypted_data = encrypted_combined_data[metadata_marker_index + len(marker):]

        try:
            decrypted_metadata = decrypt_data(encrypted_metadata, key)
        except ValueError:
            raise ValueError("Failed to decrypt metadata with the provided password.")

        try:
            file_name, file_extension = decrypted_metadata.decode().split(':', 1)
        except ValueError:
            raise ValueError("Invalid metadata format. Could not parse file name/extension.")
        
        try:
            decrypted_file_data = decrypt_data(encrypted_data, key)
        except ValueError:
            raise ValueError("Failed to decrypt file data with the provided password.")

        return {
            'type': 'file',
            'file_name': file_name,
            'file_extension': file_extension,
            'file_size': len(decrypted_file_data)
        }
    else:
        try:
            decrypted_data = decrypt_data(encrypted_combined_data, key)
        except ValueError:
            raise ValueError("Failed to decrypt string data with the provided password.")

        return {
            'type': 'string',
            'value': decrypted_data.decode()
        }
        
def deembed_file(host_file_path, output_file_path, marker=None):
    if marker is None:
        marker = defaultmarker
    elif not isinstance(marker, bytes):
        marker = marker.encode()

    end_marker = marker[::-1]  

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    start_marker_index = host_data.find(marker)
    end_marker_index = host_data.find(end_marker)

    if start_marker_index == -1:
        raise ValueError(f"Embedding marker not found in {host_file_path}")
    
    if end_marker_index == -1 or end_marker_index <= start_marker_index:
        raise ValueError(f"End marker not found or improperly placed in {host_file_path}")

    cleaned_data = host_data[:start_marker_index] + host_data[end_marker_index + len(end_marker):]

    with open(output_file_path, 'wb') as output_file:
        output_file.write(cleaned_data)

    return output_file_path

def process_extract_file(args):
    result = extract_file(args.host_file, args.password, marker=args.marker)
    print(result)
    return result

def process_embed_file(args):
    result = embed_file(args.input_file, args.host_file, args.output_file, args.password, marker=args.marker)
    print(result)
    return result

def process_embed_string(args):
    result = embed_string(args.input_string, args.host_file, args.output_file, args.password, marker=args.marker)
    print(result)
    return result

def process_extract_string(args):
    result = extract_string(args.host_file, args.password, marker=args.marker)
    print(result)
    return result

def process_deembed_file(args):
    result = deembed_file(args.host_file, args.output_file, marker=args.marker)
    print(result)
    
def process_analyze_file(args):
    result = analyze_file(args.host_file, args.password, marker=args.marker)
    if result['type'] == 'file':
        print(f"Embedded content type: File")
        print(f"File Name: {result['file_name']}")
        print(f"File Extension: {result['file_extension']}")
        print(f"File Size: {result['file_size']} bytes")
    elif result['type'] == 'string':
        print(f"Embedded content type: String")
        print(f"Value: {result['value']}")
    return result

def main():
    parser = argparse.ArgumentParser(description='File embedding and extraction with AES encryption.')
    subparsers = parser.add_subparsers()

    embed_parser = subparsers.add_parser(
        'embed', 
        aliases=['embed_file'],
        help='Embed a file into a host file'
    )
    embed_parser.add_argument('input_file', help='Path to the file to embed')
    embed_parser.add_argument('host_file', help='Path to the host file')
    embed_parser.add_argument('output_file', help='Path to save the file with embedded data')
    embed_parser.add_argument('-p', '--password', help='Password for encryption', default=defaultpassword)
    embed_parser.add_argument('-m', '--marker', help='Marker for embedding data', default=defaultmarker)
    embed_parser.set_defaults(func=process_embed_file)

    extract_parser = subparsers.add_parser(
        'extract', 
        aliases=['extract_file'],
        help='Extract an embedded file from a host file'
    )
    extract_parser.add_argument('host_file', help='Path to the host file')
    extract_parser.add_argument('-p', '--password', help='Password for decryption', default=defaultpassword)
    extract_parser.add_argument('-m', '--marker', help='Marker for extracting data', default=defaultmarker)
    extract_parser.set_defaults(func=process_extract_file)

    embed_string_parser = subparsers.add_parser('embed_string', help='Embed a string into a host file')
    embed_string_parser.add_argument('input_string', help='String to embed')
    embed_string_parser.add_argument('host_file', help='Path to the host file')
    embed_string_parser.add_argument('output_file', help='Path to save the file with embedded string')
    embed_string_parser.add_argument('-p', '--password', help='Password for encryption', default=defaultpassword)
    embed_string_parser.add_argument('-m', '--marker', help='Marker for embedding data', default=defaultmarker)
    embed_string_parser.set_defaults(func=process_embed_string)

    extract_string_parser = subparsers.add_parser('extract_string', help='Extract an embedded string from a host file')
    extract_string_parser.add_argument('host_file', help='Path to the host file')
    extract_string_parser.add_argument('-p', '--password', help='Password for decryption', default=defaultpassword)
    extract_string_parser.add_argument('-m', '--marker', help='Marker for extracting data', default=defaultmarker)
    extract_string_parser.set_defaults(func=process_extract_string)

    deembed_parser = subparsers.add_parser(
        'deembed', 
        aliases=['deembed_file'],
        help='Remove embedded data from a host file'
    )
    deembed_parser.add_argument('host_file', help='Path to the host file')
    deembed_parser.add_argument('output_file', help='Path to save the cleaned host file')
    deembed_parser.add_argument('-m', '--marker', help='Marker for removing embedded data', default=defaultmarker)
    deembed_parser.set_defaults(func=process_deembed_file)
    
    analyze_parser = subparsers.add_parser(
        'analyze',
        aliases=['analyze_file'],
        help='Analyze a host file for embedded content'
    )
    analyze_parser.add_argument('host_file', help='Path to the host file')
    analyze_parser.add_argument('-p', '--password', help='Password for decryption', default=defaultpassword)
    analyze_parser.add_argument('-m', '--marker', help='Marker for analyzing embedded data', default=defaultmarker)
    analyze_parser.set_defaults(func=process_analyze_file)

    args = parser.parse_args()

    if not vars(args):
        parser.print_help()
    else:
        args.func(args)

if __name__ == "__main__":
    main()
