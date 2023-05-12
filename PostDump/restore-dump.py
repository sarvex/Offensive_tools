#!/usr/bin/env python3

import sys
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Restore Dump')
    parser.add_argument('infile', help='input file path')
    parser.add_argument('--output', help='output file')
    parser.add_argument('--type', help='restore, decrypt, both')
    parser.add_argument('--key', help='XOR encryption key [default 0x6f]')

    args = parser.parse_args()

    key = 0x6f if args.key is None else args.key
    output = args.infile if args.output is None else Path(args.output)
    return (Path(args.infile), output, args.type, key)



def validate_args(infile, action):
    if not infile.is_file():
        sys.exit(f'"{infile}" is not a file.')

    if action not in ["restore", "decrypt", "both"]:
        sys.exit(f'"{action}" is not a good type')


def decrypt(file1_b):
    size = len(file1_b) 
    xord_byte_array = bytearray(size)

    for i in range(size):
        xord_byte_array[i] = file1_b[i] ^ 0x6f

    return xord_byte_array


def restoreSig(file1_b):
    # restore signature -> PMDM
    file1_b[0] = ord("M")
    file1_b[1] = ord("D")
    file1_b[2] = ord("M")
    file1_b[3] = ord("P")

    # restore version -> 42899
    file1_b[4] = 0x93
    file1_b[5] = 0xa7

    # restore ImplementationVersion -> 0
    file1_b[6] = 0x00
    file1_b[7] = 0x00

    return file1_b


if __name__ == '__main__':
    (infile, output, type, key) = parse_args()
    validate_args(infile, type)
    file1_b = bytearray(open(infile, 'rb').read())

    if type == "restore":
        data = restoreSig(file1_b)
        open(f'{output}.restored', 'wb').write(data)
        print(
            "[*] %s decrypted!\n[*] Saved to \033[1;33m%s\033[1;m."
            % (infile, f'{output}.restored')
        )

    elif type == "decrypt":
        data = decrypt(file1_b)
        open(f'{output}.decrypted', 'wb').write(data)
        print(
            "[*] %s signature restored!\n[*] Saved to \033[1;33m%s\033[1;m."
            % (infile, f'{output}.decrypted')
        )

    else:
        data = decrypt(file1_b)
        print(f"[*] {infile} decrypted.")
        data2 = restoreSig(data)
        open(f'{output}.both', 'wb').write(data2)
        print(f"[*] {infile} signatured restored.")
        print("[*] %s Saved to \033[1;33m%s\033[1;m." % (infile, f'{output}.both'))

