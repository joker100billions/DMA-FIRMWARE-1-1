#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plantilla de automatización para reemplazo de archivos y generación de bitstream Vivado
Personaliza las rutas y archivos según tu proyecto y hardware.
"""
import os
import shutil
import subprocess
import threading
import tempfile
import time

# CONFIGURACIÓN DEL USUARIO
replacement_file_prefix = r'C:/ruta/a/tus/archivos_de_reemplazo'  # Cambia esta ruta
vivado_path = r'D:/Xilinx/Vivado/2023.2/bin/vivado.bat'           # Cambia esta ruta

tcl_script_name = 'tu_script.tcl'                                 # Cambia por tu script TCL
bitstream_tcl_name = 'generatebitstream.tcl'                      # Cambia por tu script TCL de bitstream

replacement_files = {
    # Rutas relativas en el repo : ruta absoluta de tu archivo personalizado
    'IP/pcileech_bar_zero4k.coe': os.path.join(replacement_file_prefix, 'pcileech_bar_zero4k.coe'),
    'IP/pcileech_cfgspace.coe': os.path.join(replacement_file_prefix, 'pcileech_cfgspace.coe'),
    'src/pcileech_fifo.sv': os.path.join(replacement_file_prefix, 'pcileech_fifo.sv'),
    'src/pcileech_pcie_cfg_a7.sv': os.path.join(replacement_file_prefix, 'pcileech_pcie_cfg_a7.sv'),
    # Agrega más archivos según tu necesidad
}

last_replacement_files = {
    # Archivo core_top.v final : tu versión personalizada
    'pcileech_squirrel/pcileech_squirrel.srcs/sources_1/ip/pcie_7x_0/source/pcie_7x_0_core_top.v': os.path.join(replacement_file_prefix, 'pcie_7x_0_core_top.v')
}

def replace_files(base_dir, replacements):
    for relative_path, replacement_path in replacements.items():
        target_path = os.path.join(base_dir, relative_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copyfile(replacement_path, target_path)

def run_vivado(vivado_path, working_dir, tcl_file):
    subprocess.run([vivado_path, '-mode', 'tcl', '-source', tcl_file], cwd=working_dir)

def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Descarga y descomprime el repo de PCILeech-FPGA manualmente o aquí
        # repo_dir = download_and_extract_repo('https://github.com/ufrisk/pcileech-fpga/archive/refs/tags/v4.15.zip', temp_dir)
        repo_dir = r'C:/ruta/a/tu/PCIeSquirrel'  # Cambia por la ruta local del repo

        # Reemplaza archivos iniciales
        replace_files(repo_dir, replacement_files)

        # Ejecuta el primer script TCL
        run_vivado(vivado_path, repo_dir, tcl_script_name)

        # Reemplaza archivos finales (core_top.v)
        replace_files(repo_dir, last_replacement_files)

        # Ejecuta el script TCL de bitstream
        run_vivado(vivado_path, repo_dir, bitstream_tcl_name)

        print('Proceso completado. Bitstream generado.')

if __name__ == '__main__':
    main()
