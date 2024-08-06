import os
import sys

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def decrypt_bytes(encrypted_data, password="u8DurGE2", salt="6BBGizHE"):
    # Derive key and IV using PBKDF2
    salt_bytes = salt.encode('utf-8')
    key_iv = PBKDF2(password, salt_bytes, dkLen=32, count=1000)
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


def decrypt_file(file_path, output_path, password="u8DurGE2", salt="6BBGizHE"):
    # Read the encrypted file
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()

    # Decrypt the data
    decrypted_data = decrypt_bytes(encrypted_data, password, salt)

    # Write the decrypted data to the output file
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)


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
