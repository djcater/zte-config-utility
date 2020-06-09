"""Decode config.bin into config.xml"""
import argparse

import zcu

def main():
    """the main function"""
    parser = argparse.ArgumentParser(description='Decode config.bin from ZTE Routers',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='Encoded configuration file (config.bin)')
    parser.add_argument('outfile', type=argparse.FileType('wb'),
                        help='Output file (config.xml)')
    parser.add_argument('--key', type=lambda x: x.encode(), default=b'',
                        help="Key for AES decryption")
    args = parser.parse_args()

    key = args.key.ljust(16, b'\0')[:16]

    infile = args.infile
    outfile = args.outfile

    decoded = zcu.zte.decode_config(infile, key)
    outfile.write(decoded)

if __name__ == '__main__':
    main()
