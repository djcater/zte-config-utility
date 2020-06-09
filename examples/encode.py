"""Encode config.xml into config.bin"""
import argparse

import zcu


def main():
    """the main function"""
    parser = argparse.ArgumentParser(description='Encode config.bin for ZTE Routers',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='Raw configuration file (config.xml)')
    parser.add_argument('outfile', type=argparse.FileType('wb'),
                        help='Output file')
    parser.add_argument('--key', type=lambda x: x.encode(), default=b'',
                        help="Key for AES encryption")
    parser.add_argument('--signature', type=lambda x: x.encode(), default=b'', required=True,
                        help='Signature string of device, e.g "ZXHN H298N"')
    parser.add_argument('--chunk-size', type=int, default=65536,
                        help='ZLIB chunk sizes (default 65536)')
    parser.add_argument('--payload-type', type=int, default=2, choices=[0, 2],
                        help='payload type (0=compressed, 2=compressed+encrypted)')

    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    key = args.key.ljust(16, b'\0')[:16]
    signature = args.signature
    chunk_size = args.chunk_size
    payload_type = args.payload_type

    encoded = zcu.zte.encode_config(infile, chunk_size, key, signature, payload_type)
    outfile.write(encoded)

if __name__ == '__main__':
    main()
