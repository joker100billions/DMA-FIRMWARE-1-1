# Made with <3 by RakeshMonkee, adaptado por DMN_CBA
"""
Script para personalizar IDs PCIe en pcie_7x_0_core_top.v generado por Vivado.

- Cambia la variable file_path a la ruta de tu archivo core_top.v
- Ejecuta el script y responde a los prompts con los IDs en hexadecimal (sin 0x)
"""

file_path = "C:/ruta/a/tu/pcie_7x_0_core_top.v"  # Cambia esta ruta

with open(file_path, 'r') as file:
    verilog_contents = file.read()

InputvendorID = str(input("VendorID (4 hex): "))[:4]
InputDeviceID = str(input("DeviceID (4 hex): "))[:4]
InputRevisionID = str(input("RevisionID (2 hex): "))[:2]
InputSubsystemID = str(input("SubsystemID (4 hex): "))[:4]
InputSubsystemVendorID = str(input("SubsystemVendorID (4 hex): "))[:4]

VendorID = f"CFG_VEND_ID        = 16'h{InputvendorID}"
DeviceID = f"CFG_DEV_ID         = 16'h{InputDeviceID}"
RevisionID = f"CFG_REV_ID         =  8'h{InputRevisionID}"
SubsystemVendorID = f"CFG_SUBSYS_VEND_ID = 16'h{InputSubsystemVendorID}"
SubsystemID = f"CFG_SUBSYS_ID      = 16'h{InputSubsystemID}"

verilog_contents = verilog_contents.replace("CFG_VEND_ID        = 16'h10EE", VendorID)
verilog_contents = verilog_contents.replace("CFG_DEV_ID         = 16'h0666", DeviceID)
verilog_contents = verilog_contents.replace("CFG_REV_ID         =  8'h02", RevisionID)
verilog_contents = verilog_contents.replace("CFG_SUBSYS_VEND_ID = 16'h10EE", SubsystemVendorID)
verilog_contents = verilog_contents.replace("CFG_SUBSYS_ID      = 16'h0007", SubsystemID)

with open(file_path, 'w') as file:
    file.write(verilog_contents)

print("IDs PCIe personalizados correctamente en core_top.v")
