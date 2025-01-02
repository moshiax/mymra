import argparse
import os
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

MARKER = b'MQAZWERPASDZXW'

def generate_password_key(password):
    return sha256(password.encode()).digest()

def encrypt_data(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return iv + encrypted_data

def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    try:
        decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    except (ValueError, KeyError):
        return None
    return decrypted_data

def embed_file(input_file_path, host_file_path, output_file_path, password):
    key = generate_password_key(password)

    with open(input_file_path, 'rb') as input_file:
        input_data = input_file.read()

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    file_name = os.path.basename(input_file_path)
    file_extension = os.path.splitext(file_name)[1][1:] or "DMM"
    metadata = f"{file_name}:{file_extension}".encode()

    encrypted_metadata = encrypt_data(metadata, key)
    encrypted_data = encrypt_data(input_data, key)

    combined_data = host_data + MARKER + encrypted_metadata + MARKER + encrypted_data

    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)

    print(f"Inserted {file_name} in {output_file_path} with password {password}")

def extract_file(host_file_path, password):
    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    marker_index = host_data.find(MARKER)
    if marker_index == -1:
        print(f"Failed to extract from {host_file_path} with password {password}")
        return None

    metadata_start = marker_index + len(MARKER)
    metadata_end = host_data.find(MARKER, metadata_start)
    if metadata_end == -1:
        print(f"Failed to extract from {host_file_path} with password {password}")
        return None

    encrypted_metadata = host_data[metadata_start:metadata_end]
    encrypted_data = host_data[metadata_end + len(MARKER):]

    decrypted_metadata = decrypt_data(encrypted_metadata, key)
    if decrypted_metadata is None:
        print(f"Failed to extract from {host_file_path} with password {password}")
        return None

    try:
        file_name, file_extension = decrypted_metadata.decode().split(':')
        if not file_extension:
            file_extension = 'DMM'
    except ValueError:
        print(f"Failed to extract from {host_file_path} with password {password}")
        return None

    file_name = f"{file_name}.{file_extension}" if not file_name.endswith(f".{file_extension}") else file_name

    decrypted_data = decrypt_data(encrypted_data, key)
    if decrypted_data is None:
        print(f"Failed to extract from {host_file_path} with password {password}")
        return None

    with open(file_name, 'wb') as output_file:
        output_file.write(decrypted_data)

    print(f"Extracted {file_name} from {host_file_path} with password {password}")
    return file_name

def embed_string(input_string, host_file_path, output_file_path, password):
    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    encrypted_data = encrypt_data(input_string.encode(), key)

    combined_data = host_data + MARKER + encrypted_data

    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)

    print(f"Embedded string into {output_file_path} with password {password}")

def extract_string(host_file_path, password):
    key = generate_password_key(password)

    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    marker_index = host_data.find(MARKER)
    if marker_index == -1:
        print(f"Failed to extract string from {host_file_path} with password {password}")
        return None

    encrypted_data = host_data[marker_index + len(MARKER):]

    decrypted_data = decrypt_data(encrypted_data, key)
    if decrypted_data is None:
        print(f"Failed to extract string from {host_file_path} with password {password}")
        return None

    extracted_string = decrypted_data.decode()
    print(f"Extracted string: {extracted_string}")
    return extracted_string

def deembed_file(host_file_path, output_file_path):
    with open(host_file_path, 'rb') as host_file:
        host_data = host_file.read()

    marker_index = host_data.find(MARKER)
    if marker_index == -1:
        print(f"Failed. No embedded data found in {host_file_path}")
        return None

    cleaned_data = host_data[:marker_index]

    with open(output_file_path, 'wb') as output_file:
        output_file.write(cleaned_data)

    print(f"Removed embedded data from {host_file_path} and saved to {output_file_path}")

def process_extract_file(args):
    return extract_file(args.host_file, args.password)

def process_embed_file(args):
    embed_file(args.input_file, args.host_file, args.output_file, args.password)

def process_embed_string(args):
    embed_string(args.input_string, args.host_file, args.output_file, args.password)

def process_extract_string(args):
    extract_string(args.host_file, args.password)

def process_deembed_file(args):
    deembed_file(args.host_file, args.output_file)

def main():
    parser = argparse.ArgumentParser(description='File embedding and extraction with AES encryption.')
    subparsers = parser.add_subparsers()

    embed_parser = subparsers.add_parser('embed', help='Embed a file into a host file')
    embed_parser.add_argument('input_file', help='Path to the file to embed')
    embed_parser.add_argument('host_file', help='Path to the host file')
    embed_parser.add_argument('output_file', help='Path to save the file with embedded data')
    embed_parser.add_argument('-p', '--password', help='Password for encryption', default='RAMRANCHREALLYROCKS')
    embed_parser.set_defaults(func=process_embed_file)

    extract_parser = subparsers.add_parser('extract', help='Extract an embedded file from a host file')
    extract_parser.add_argument('host_file', help='Path to the host file')
    extract_parser.add_argument('-p', '--password', help='Password for decryption', default='RAMRANCHREALLYROCKS')
    extract_parser.set_defaults(func=process_extract_file)

    embed_string_parser = subparsers.add_parser('embed_string', help='Embed a string into a host file')
    embed_string_parser.add_argument('input_string', help='String to embed')
    embed_string_parser.add_argument('host_file', help='Path to the host file')
    embed_string_parser.add_argument('output_file', help='Path to save the file with embedded string')
    embed_string_parser.add_argument('-p', '--password', help='Password for encryption', default='RAMRANCHREALLYROCKS')
    embed_string_parser.set_defaults(func=process_embed_string)

    extract_string_parser = subparsers.add_parser('extract_string', help='Extract an embedded string from a host file')
    extract_string_parser.add_argument('host_file', help='Path to the host file')
    extract_string_parser.add_argument('-p', '--password', help='Password for decryption', default='RAMRANCHREALLYROCKS')
    extract_string_parser.set_defaults(func=process_extract_string)

    deembed_parser = subparsers.add_parser('deembed', help='Remove embedded data from a host file')
    deembed_parser.add_argument('host_file', help='Path to the host file')
    deembed_parser.add_argument('output_file', help='Path to save the cleaned host file')
    deembed_parser.set_defaults(func=process_deembed_file)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
