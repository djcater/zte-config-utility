"""Encryption and decryption helper functions"""

import struct
from io import BytesIO
from Crypto.Cipher import AES

from . import constants

def decrypt(aes_block, aes_key):
    encrypted_data = b''
    while True:
        aes_chunk = struct.unpack('>3I', aes_block.read(12))
        encrypted_data += aes_block.read(aes_chunk[0])
        if aes_chunk[2] == 0:
            break
    aes_cipher = AES.new(aes_key)
    decrypted_data = BytesIO()
    decrypted_data.write(aes_cipher.decrypt(encrypted_data))
    decrypted_data.seek(0)
    return decrypted_data

def encrypt(data, aes_key, chunk_size):
    # 16 byte alignment
    if len(data) % 16 > 0:
        data = data + (16 - len(data) % 16)*b'\0'

    encrypted_data = AES.new(aes_key).encrypt(data)

    encrypted_data_length = len(encrypted_data)

    header = b''
    header += struct.pack('>I', constants.PAYLOAD_MAGIC)
    header += struct.pack('>I', 2) # aes encryption
    header += struct.pack('>3I', *(0, encrypted_data_length + 72, chunk_size))
    header += struct.pack('>10I', *10*(0,))
    header += struct.pack('>3I', *(encrypted_data_length, encrypted_data_length, 0))

    return header + encrypted_data
