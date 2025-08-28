#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script: TeleScan PE PCIE config space '.tlscan' to Vivado '.coe' file converter.

Args:
    1) source '.tlscan' file path.
    2) destination '.coe` file path.

Format:
https://docs.xilinx.com/r/en-US/ug896-vivado-ip/Using-a-COE-File
"""
import os
import sys
import datetime
import xml.etree.ElementTree


# Si no se pasa argumento, buscar el primer .tlscan en telescan/
if len(sys.argv) >= 2:
    src_path = os.path.normpath(sys.argv[1])
else:
    telescan_dir = os.path.join(os.path.dirname(__file__), '..', 'telescan')
    telescan_dir = os.path.abspath(telescan_dir)
    found = False
    if os.path.isdir(telescan_dir):
        for fname in os.listdir(telescan_dir):
            if fname.lower().endswith('.tlscan'):
                src_path = os.path.join(telescan_dir, fname)
                found = True
                print(f'Usando archivo detectado: {src_path}')
                break
    if not found:
        print('No se encontró ningún archivo .tlscan en la carpeta telescan/.')
        sys.exit(1)

if len(sys.argv) >= 3:
    dst_path = os.path.normpath(sys.argv[2])
else:
    dst_path = os.path.normpath(os.path.expanduser("~/Desktop") + "/output.coe")

# Load and parse the XML format '.tlscan' file
try:
    tree = xml.etree.ElementTree.parse(str(src_path))
    bytes_elem = tree.find('.//bytes')
    if bytes_elem is None or bytes_elem.text is None:
        raise ValueError('No <bytes> element or empty in the .tlscan file!')
    bs = bytes_elem.text
except Exception as e:
    print(f'Error parsing .tlscan file: {e}')
    sys.exit(1)

# Make one 8,192 char long hex bytes string
bs = ''.join(bs.split())
if len(bs) != 8192:
    print(f'Error: Expected 8192 character (4096 hex byte) string, got {len(bs):,}!')
    sys.exit(1)

# Write out ".coe" file
with open(dst_path, 'w') as fp:
    fp.write(f'\n; Converted to COE from "{src_path}" on {datetime.datetime.now()}\n')
    fp.write('memory_initialization_radix=16;\nmemory_initialization_vector=\n')

    for y in range(16):
        fp.write(f'\n; {(y * 256):04X}\n')
        for x in range(16):
            fp.write(f'{bs[0:8]},{bs[8:16]},{bs[16:24]},{bs[24:32]},\n')
            bs = bs[32:]
    fp.write('\n; Script firmado por DMN_CBA (Demon_Cuba)\n')
