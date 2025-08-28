# Made with <3 by RakeshMonkee, adaptado por DMN_CBA
"""
Script para automatizar la ejecución de un script TCL en Vivado para generar o modificar un proyecto.

- Cambia vivado_path a la ruta de tu instalación de Vivado
- Cambia project_dir a la carpeta de tu proyecto
- Cambia tcl_script_name al nombre de tu script TCL
"""
import os
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))

vivado_path = r"D:/Xilinx/Vivado/2023.2/bin/vivado.bat"  # Cambia esta ruta
project_dir = r"C:/ruta/a/tu/proyecto"                   # Cambia esta ruta
tcl_script_name = "script.tcl"                           # Cambia por tu script TCL

tcl_script_path = os.path.join(script_dir, tcl_script_name)

command = [vivado_path, "-mode", "tcl", "-source", tcl_script_path, "-notrace"]

subprocess.run(command, cwd=project_dir)
