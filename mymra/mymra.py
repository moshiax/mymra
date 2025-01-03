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

def embed_file(input_file_path, host_file_path, output_file_path, password=None, marker=None):
    
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker 
    else:
        marker = marker.encode()
    
    key = generate_password_key(password)
    
    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    if marker in host_data:
        raise ValueError("The file already contains embedded data.")

    with open(input_file_path, 'rb') as input_file:
        input_data = input_file.read()

    file_name = os.path.basename(input_file_path)
    file_extension = os.path.splitext(file_name)[1][1:] or "DMM"
    metadata = f"{file_name}:{file_extension}".encode()

    encrypted_metadata = encrypt_data(metadata, key)
    encrypted_data = encrypt_data(input_data, key)

    combined_data = host_data + marker + encrypted_metadata + marker + encrypted_data

    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)

    return output_file_path

def extract_file(host_file_path, password=None, marker=None):
    
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker 
    else:
        marker = marker.encode()
    
    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    marker_index = host_data.find(marker)
    if marker_index == -1:
        raise ValueError(f"Marker not found in {host_file_path}. Extraction failed.")

    metadata_start = marker_index + len(marker)
    metadata_end = host_data.find(marker, metadata_start)
    if metadata_end == -1:
        raise ValueError(f"End marker not found in {host_file_path}. Extraction failed.")

    encrypted_metadata = host_data[metadata_start:metadata_end]
    encrypted_data = host_data[metadata_end + len(marker):]

    decrypted_metadata = decrypt_data(encrypted_metadata, key)
    if decrypted_metadata is None:
        raise ValueError(f"Failed to decrypt metadata from {host_file_path}.")

    try:
        file_name, file_extension = decrypted_metadata.decode().split(':')
        if not file_extension:
            file_extension = 'DMM'
    except ValueError:
        raise ValueError(f"Invalid metadata format in {host_file_path}.")

    file_name = f"{file_name}.{file_extension}" if not file_name.endswith(f".{file_extension}") else file_name

    decrypted_data = decrypt_data(encrypted_data, key)
    if decrypted_data is None:
        raise ValueError(f"Failed to decrypt data from {host_file_path}.")

    with open(file_name, 'wb') as output_file:
        output_file.write(decrypted_data)

    return file_name

def embed_string(input_string, host_file_path, output_file_path, password=None, marker=None):
    
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker 
    else:
        marker = marker.encode()
        
    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    if marker in host_data:
        raise ValueError("The file already contains embedded data.")

    encrypted_data = encrypt_data(input_string.encode(), key)

    combined_data = host_data + marker + encrypted_data

    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)

    return output_file_path

def extract_string(host_file_path, password=None, marker=None):
    
    if password is None:
        password = defaultpassword 
    
    if marker is None:
        marker = defaultmarker 
    else:
        marker = marker.encode()
        
    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    marker_index = host_data.find(marker)
    if marker_index == -1:
        raise ValueError(f"Marker not found in {host_file_path}. Extraction failed.")

    encrypted_data = host_data[marker_index + len(marker):]

    decrypted_data = decrypt_data(encrypted_data, key)
    if decrypted_data is None:
        raise ValueError(f"Failed to decrypt data from {host_file_path} with the given password.")

    extracted_string = decrypted_data.decode()

    return extracted_string

def deembed_file(host_file_path, output_file_path, marker=None):
    
    if marker is None:
        marker = defaultmarker 
    else:
        marker = marker.encode()
        
    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    marker_index = host_data.find(marker)
    if marker_index == -1:
        raise ValueError(f"No embedded data found in {host_file_path}")

    cleaned_data = host_data[:marker_index]

    with open(output_file_path, 'wb') as output_file:
        output_file.write(cleaned_data)

    return output_file_path

def process_extract_file(args):
    return extract_file(args.host_file, args.password, marker=args.marker)

def process_embed_file(args):
    embed_file(args.input_file, args.host_file, args.output_file, args.password, marker=args.marker)

def process_embed_string(args):
    embed_string(args.input_string, args.host_file, args.output_file, args.password, marker=args.marker)

def process_extract_string(args):
    extract_string(args.host_file, args.password, marker=args.marker)

def process_deembed_file(args):
    deembed_file(args.host_file, args.output_file, marker=args.marker)


def main():
    parser = argparse.ArgumentParser(description='File embedding and extraction with AES encryption.')
    subparsers = parser.add_subparsers()

    embed_parser = subparsers.add_parser('embed', help='Embed a file into a host file')
    embed_parser.add_argument('input_file', help='Path to the file to embed')
    embed_parser.add_argument('host_file', help='Path to the host file')
    embed_parser.add_argument('output_file', help='Path to save the file with embedded data')
    embed_parser.add_argument('-p', '--password', help='Password for encryption', default=defaultpassword)
    embed_parser.add_argument('-m', '--marker', help='Marker for embedding data', default=defaultmarker)
    embed_parser.set_defaults(func=process_embed_file)

    extract_parser = subparsers.add_parser('extract', help='Extract an embedded file from a host file')
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

    deembed_parser = subparsers.add_parser('deembed', help='Remove embedded data from a host file')
    deembed_parser.add_argument('host_file', help='Path to the host file')
    deembed_parser.add_argument('output_file', help='Path to save the cleaned host file')
    deembed_parser.add_argument('-m', '--marker', help='Marker for removing embedded data', default=defaultmarker)
    deembed_parser.set_defaults(func=process_deembed_file)

    args = parser.parse_args()

    if not vars(args):
        parser.print_help()
    else:
        args.func(args)
        
if __name__ == "__main__":
    main()
