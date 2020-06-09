"""Compression and decompression helper functions"""

import zlib
import struct

from . import constants

def _decompress(infile):
    decompressed_data = b''
    crc = 0
    while True:
        aes_header = struct.unpack('>3I', infile.read(12))
        decompressed_length = aes_header[0]
        compressed_length = aes_header[1]
        compressed_chunk = infile.read(compressed_length)
        crc = zlib.crc32(compressed_chunk, crc)
        decompressed_chunk = zlib.decompress(compressed_chunk)
        assert decompressed_length == len(decompressed_chunk)
        decompressed_data += decompressed_chunk
        if aes_header[2] == 0:
            break
    return (decompressed_data, crc)

def decompress(infile):
    """decompress without crc check"""
    decompressed_data, _ = _decompress(infile)
    return decompressed_data

def decompress_with_crc_check(infile, header):
    """decompress and perform crc checks"""
    assert header[0] == constants.PAYLOAD_MAGIC
    assert header[6] == (zlib.crc32(struct.pack('>6I', *header[:6])) & 0xffffffff)

    decompressed_data, crc = decompress(infile)

    assert header[5] == (crc & 0xffffffff)
    assert header[2] == len(decompressed_data)
    return decompressed_data

def _compress_blocks(infile, chunk_size):
    compressed_data = b''
    total_uncompressed_length = 0
    total_compressed_length = 60
    number_of_chunks = 0
    crc = 0
    while True:
        data = infile.read(chunk_size)
        uncompressed_length = len(data)
        if uncompressed_length == 0:
            break

        total_uncompressed_length += uncompressed_length
        number_of_chunks += 1

        compressed_chunk = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        crc = zlib.crc32(compressed_chunk, crc) & 0xffffffff

        compressed_length = len(compressed_chunk)

        if uncompressed_length < chunk_size:
            more_chunks = 0
        else:
            total_compressed_length += len(compressed_chunk) + 12
            more_chunks = total_compressed_length

        compressed_data += struct.pack('>3I', uncompressed_length, compressed_length, more_chunks)
        compressed_data += compressed_chunk

    stats = {
        'crc': crc,
        'total_uncompressed_length': total_uncompressed_length,
        'number_of_chunks': number_of_chunks,
        'total_compressed_length': total_compressed_length
    }

    return (compressed_data, stats)

def compress(infile, chunk_size):
    """compress and add header"""
    compressed_data, stats = _compress_blocks(infile, chunk_size)

    header = struct.pack('>6I',
                         constants.PAYLOAD_MAGIC,
                         0, # no encryption, only zlib compression
                         stats['total_uncompressed_length'],
                         stats['total_compressed_length'] if stats['number_of_chunks'] > 0 else 0,
                         chunk_size,
                         stats['crc'])
    payload = b''
    payload += header
    payload += struct.pack('>I', zlib.crc32(header) & 0xffffffff)
    payload += struct.pack('>8I', *8*(0,))
    payload += compressed_data

    return payload
