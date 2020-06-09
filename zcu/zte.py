"""Various helper functions to read/write zte configuration"""
from os import stat
import struct

from . import constants
from . import compression
from . import encryption

def read_header(infile):
    """expects to be at position 0 of the file, returns side of header"""
    header_magic = struct.unpack('>4I', infile.read(16))
    if header_magic == constants.ZTE_MAGIC:
        # 128 byte header
        header = struct.unpack('>28I', infile.read(112))
        assert header[2] == 4
        header_length = header[13]
        signed_config_size = header[14]
        file_size = stat(infile.name).st_size
        assert header_length + signed_config_size == file_size
    else:
        # no extra header so return to start of the file
        infile.seek(0)
    return infile.tell()

def read_signature(infile):
    """expects to be at the start of the signature magic, returns signature"""
    signature_header = struct.unpack('>3I', infile.read(12))
    assert signature_header[0] == constants.SIGNATURE_MAGIC
    # _ = signature_header[1] # 0 ?
    signature_length = signature_header[2]
    signature = infile.read(signature_length)
    return signature

def read_payload_type(infile):
    """expects to be at the start of the payload magic"""
    payload_header = struct.unpack('>15I', infile.read(60))
    assert payload_header[0] == constants.PAYLOAD_MAGIC
    payload_type = payload_header[1]
    # payload_length = payload_header[3]
    # payload_chunk_size = payload_header[4]
    return payload_type

def add_header(payload, signature, payload_type):
    """creates a 'full' payload of (header), signature and payload"""
    signature_length = len(signature)
    full_payload = b''
    if payload_type == 2:
        full_payload_length = len(payload) + 12 + signature_length
        full_payload += struct.pack('>4I', *constants.ZTE_MAGIC)
        full_payload += struct.pack('>28I', *(0, 0, 4, 0,
                                              0, 0, 0, 0,
                                              0, 0, 0, 64,
                                              131072, 128, full_payload_length, 0,
                                              0, 0, 0, 0,
                                              0, 0, 0, 0,
                                              0, 0, 0, 0))

    # add signature
    full_payload += struct.pack('>3I', *(constants.SIGNATURE_MAGIC, 0, signature_length))
    full_payload += signature
    # add payload
    full_payload += payload

    return full_payload

def decode_config(infile, key):
    """expects to be at the start of the file"""
    read_header(infile)
    read_signature(infile)
    payload_type = read_payload_type(infile)

    if payload_type == 2:
        infile = encryption.decrypt(infile, key)
        payload_type = read_payload_type(infile)

    assert payload_type == 0

    return compression.decompress(infile)

def encode_config(infile, chunk_size, key, signature, payload_type):
    """convert a raw file into a zte binary via zlib/aes"""
    payload_data = compression.compress(infile, chunk_size)

    if payload_type == 2:
        payload_data = encryption.encrypt(payload_data, key, chunk_size)

    return add_header(payload_data, signature, payload_type)
