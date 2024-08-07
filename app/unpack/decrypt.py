import os
import sys

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

PASSWORD = "u8DurGE2"
SALT = "6BBGizHE"

def decrypt_bytes(encrypted_data):
    # Derive key and IV using PBKDF2
    salt_bytes = SALT.encode('utf-8')
    key_iv = PBKDF2(PASSWORD, salt_bytes, dkLen=32, count=1000)
    key = key_iv[:16]
    iv = key_iv[16:32]

    # Initialize AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)

    # Remove padding
    pad_len = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_len]

    return decrypted_data


def decrypt_file(file_path: str, output_path: str):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_bytes(encrypted_data)

    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

def decrypt_folder(
    input_folder: str,
    output_folder: str,
    recursive: bool = True,
    mkdir: bool = True,
    resume_on_error: bool = False,
    out_failed_files: list[str]|None = None
):
    """
    :param out_failed_files: output list of failed files
    """
    if not os.path.exists(output_folder) and mkdir:
        os.makedirs(output_folder)

    files = os.listdir(input_folder)
    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        if os.path.isdir(input_path):
            if recursive:
                decrypt_folder(
                    input_path,
                    output_path,
                    recursive=recursive,
                    mkdir=mkdir,
                    resume_on_error=resume_on_error,
                    out_failed_files=out_failed_files
                )
        else:
            try:
                decrypt_file(input_path, output_path)
            except:
                if not resume_on_error:
                    raise
                else:
                    if out_failed_files is not None:
                        out_failed_files.append(input_path)


def encrypt_bytes(data):
    # Derive key and IV using PBKDF2
    salt_bytes = SALT.encode('utf-8')
    key_iv = PBKDF2(PASSWORD, salt_bytes, dkLen=32, count=1000)
    key = key_iv[:16]
    iv = key_iv[16:32]

    # Initialize AES cipher
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Add padding to the data
    pad_len = AES.block_size - (len(data) % AES.block_size)
    padded_data = data + bytes([pad_len] * pad_len)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)

    return encrypted_data

def encrypt_file(file_path, output_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted_data = encrypt_bytes(data)

    with open(output_path, 'wb') as f:
        f.write(encrypted_data)

def encrypt_folder(input_folder, output_folder, recursive=True, mkdir=True):
    if not os.path.exists(output_folder) and mkdir:
        os.makedirs(output_folder)

    files = os.listdir(input_folder)
    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        if os.path.isdir(input_path):
            if recursive:
                encrypt_folder(input_path, output_path, recursive=recursive, mkdir=mkdir)
        else:
            encrypt_file(input_path, output_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python decrypt.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if os.path.isdir(input_file) and os.path.isdir(output_file):
        # Scan input folder for files
        for filename in os.listdir(input_file):
            # Construct input and output file paths
            input_path = os.path.join(input_file, filename)
            output_path = os.path.join(output_file, filename)
            
            # Decrypt the file
            decrypt_file(input_path, output_path)
    else:
        decrypt_file(input_file, output_file)
