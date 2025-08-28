# DMA-FIRMWARE-1-1
⚠️ Aviso importante: este proyecto se comparte únicamente con fines educativos y de investigación. No se recomienda ni aprueba su uso con fines maliciosos.
=======
## Preguntas Frecuentes sobre DMA (FAQ)

**¿Qué tarjeta DMA debería comprar?**
- Si quieres ahorrar dinero, la 35T. Si prefieres más velocidad y una tarjeta más nueva, la 75T.

**¿Qué firmware necesito para mi tarjeta DMA?**
- 35T: Squirrel
- 75T: EnigmaX1

**¿Puedo usar el mismo firmware en una 35T y una 4th Gen cap DMA?**
- Sí, ambas usan el mismo chip prototipo (squirrel).

**¿Qué requisitos mínimos debe tener mi segundo PC?**
- USB 3.0, al menos 6GB de RAM.

**¿Por qué obtengo "Tiny PCIe TLP Algorithm" al hacer un speed test?**
- Suele deberse a que la placa madre del PC principal no acepta el config space del firmware DMA.

**¿Cómo flasheo mi firmware?**
- Para 35T, usa OpenOCD para programar y actualizar. Consulta la sección "How to Flash".

**¿Qué placa donante debo usar?**
- Cualquier dispositivo PCIe puede usarse como donante. Se recomienda no usar valores de dispositivos PCIe ya instalados (como GPU). Ejemplo: Intel Wifi 6 Ax200, capturadoras de video, extensiones USB, tarjetas de sonido, SATA, etc.

**¿Qué es el Firmware Locking?**
- Es el proceso de asegurar el firmware para evitar acceso, modificación o copia no autorizada.

**¿Cómo funciona el Firmware Locking?**
- Usa el valor EFUSE FUSER_DNA del chip Artix7 de tu tarjeta DMA y lo compara con un valor codificado en el firmware. Si coinciden, el firmware funciona; si no, no. Cada chip Artix7 tiene un identificador único (DNA).

Más preguntas próximamente...
### Personaliza tu script TCL (script.tcl)

El archivo `scripts/script.tcl` es un ejemplo de script para automatizar la regeneración de IPs y preparación del proyecto en Vivado.

- Cambia la ruta del comando `cd` para que apunte al directorio de tu IP core.
- Puedes agregar o modificar comandos TCL según tu flujo de trabajo.
- Este script se ejecuta automáticamente desde `generate_project.py`.
## Automatización de generación de proyecto Vivado

Puedes usar el script `scripts/generate_project.py` para ejecutar cualquier script TCL sobre tu proyecto Vivado de forma automática.

### Uso:
1. Edita las variables en el script:
   - `vivado_path`: Ruta a tu instalación de Vivado.
   - `project_dir`: Carpeta de tu proyecto Vivado.
   - `tcl_script_name`: Nombre de tu script TCL (debe estar en la carpeta `scripts/`).
2. Ejecuta el script:
   ```bash
   python scripts/generate_project.py
   ```
3. Vivado se abrirá en modo TCL y ejecutará el script indicado en el proyecto.

Esto te permite automatizar tareas como crear, abrir, modificar o sintetizar proyectos desde Python.
## Personalización rápida de IDs PCIe en core_top.v

Puedes usar el script `scripts/customize_core_top.py` para automatizar el cambio de VendorID, DeviceID, RevisionID, SubsystemID y SubsystemVendorID en el archivo `pcie_7x_0_core_top.v` generado por Vivado.

### Uso:
1. Edita la variable `file_path` en el script para que apunte a tu archivo real `pcie_7x_0_core_top.v`.
2. Ejecuta el script:
   ```bash
   python scripts/customize_core_top.py
   ```
3. Ingresa los IDs que desees cuando el script lo solicite (en hexadecimal, sin 0x).
4. El archivo será modificado automáticamente con tus valores.

Esto facilita la clonación o personalización de dispositivos PCIe en proyectos FPGA.
## Automatización: Uso del script auto_vivado.py

Este script permite automatizar el reemplazo de archivos clave y la generación del bitstream en Vivado.

### 1. Prepara tus archivos personalizados
- Crea una carpeta con todos los archivos que quieras reemplazar (por ejemplo, `.coe`, `.sv`, etc.).
- Prepara tus scripts TCL (`tu_script.tcl` y `generatebitstream.tcl`) según tu flujo de Vivado.

### 2. Configura el script
Edita las siguientes variables en `scripts/auto_vivado.py`:
- `replacement_file_prefix`: Ruta a tu carpeta de archivos personalizados.
- `vivado_path`: Ruta a `vivado.bat` de tu instalación de Xilinx.
- `tcl_script_name` y `bitstream_tcl_name`: Nombres de tus scripts TCL.
- `replacement_files` y `last_replacement_files`: Mapea las rutas relativas del repo a tus archivos personalizados.

### 3. Ejecuta el script
Desde la raíz del proyecto:
```bash
python scripts/auto_vivado.py
```
El script reemplazará los archivos, ejecutará los scripts TCL y generará el bitstream automáticamente.

### 4. Personaliza según tu hardware
- Cambia las rutas y nombres de archivos según tu variante (35T, 75T, 100T, M.2, etc.).
- Adapta los scripts TCL para tu flujo de Vivado y proyecto específico.

### Consejos
- Haz backup de tus archivos originales antes de reemplazar.
- Usa control de versiones para rastrear cambios.
- Consulta la documentación de Vivado para crear tus scripts TCL.
## Checklist rápido para Shadow Config Space (Telescan + Vivado)

1. **Requisitos**
   - Telescan (para extraer la config PCIe)
   - Python (para ejecutar el convertidor)

2. **Exporta la configuración**
   - Usa Telescan para guardar el archivo `.tlscan` de tu dispositivo donante.
   - Coloca el archivo en la carpeta `telescan/` del proyecto.

3. **Convierte a .coe**
   - Ejecuta el script:
     ```bash
     python scripts/telescan_to_coe.py
     ```
     (Detecta automáticamente el primer `.tlscan` en `telescan/` y genera `output.coe` en el escritorio)

4. **Reemplaza el contenido**
   - Copia el contenido de `output.coe` en `pcileech_cfgspace.coe`.

5. **Edita los archivos Verilog**
   - En `pcileech_fifo.sv`, pon `CFGTLP ZERO DATA` en 0.
   - En `pcileech_pcie_cfg_a7.sv`, cambia DSN, Master Abort Flag y Bus Master Flag.

6. **Genera el IP core**
   - En Vivado, crea el IP core usando el nuevo `.coe`.

7. **Ajusta parámetros en Vivado**
   - En `core_top.sv`, ajusta `EXT_CFG_CAP_PTR` y `EXT_CFG_XP_CAP_PTR` al bloque donde quieres que empiece tu capability.

8. **Verifica y ajusta**
   - Asegúrate de que los encabezados y capacidades coincidan con lo que ves en Telescan.

9. **Genera bitstream y flashea**
   - Genera el bitstream y flashea la FPGA.

# Guía Completa: Personalización PCILeech DMA para Artix-7 (75T484)

Esta guía te permitirá clonar y personalizar una tarjeta PCIe usando PCILeech y una FPGA Xilinx Artix-7 XC7A75T-1CSG324C. Incluye todos los recursos, pasos y recomendaciones para adaptar el firmware, cargar dumps reales, modificar identificadores y configurar el entorno de desarrollo.

---


## Requisitos

### Hardware
- FPGA Artix-7 75T (XC7A75T-1CSG324C)
- Host PCIe (PC objetivo para clonar)
- PC con Linux (para extraer dumps de BARs)
- PC con Windows y Vivado instalado (para editar y compilar el firmware)

### Software y Recursos
- Vivado 2023.1 o compatible
- Ubuntu Live USB (ejemplo: 22.04)
- Telescan (opcional, para análisis de PCIe en Windows)
- Visual Studio Code (opcional, para edición de código)
- PCILeech Firmware Base: https://github.com/ufrisk/pcileech
- Script bar.c (ver más abajo)

---

pcileech_dma_custom/
├── dumps/
│   ├── dump2.txt
│   └── dump4.txt
├── scripts/
│   └── bar.c
├── src/
│   ├── pcileech_tlps128_bar_controller.sv
│   └── otros .sv modificados
├── README.md
└── .gitignore

## Estructura Recomendada del Proyecto

```
DMA/
├── dumps/
│   ├── dump2.txt
│   └── dump4.txt
├── scripts/
│   └── bar.c
├── src/
│   ├── pcileech_tlps128_bar_controller.sv
│   ├── pcileech_pcie_cfg_a7.sv
│   ├── pcileech_tlps128_cfgspace_shadow.sv
│   └── ...otros .sv modificados
├── README.md
└── .gitignore
```

---


## Paso 1: Extracción de Recursos (Dumps) desde Linux

1. Crea un Live USB de Ubuntu y bootea desde él en el host objetivo.

2. Copia el siguiente archivo `bar.c` al escritorio o USB:

```c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc < 2) { printf("Usage: ./bar <resource>"); return 1; }
    int fd = open(argv[1], O_RDONLY);
    if (fd < 0) { perror("open"); return 1; }
    void *map = mmap(0, 0x1000, PROT_READ, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) { perror("mmap"); return 1; }
    uint32_t *p = (uint32_t *)map;
    for (int i = 0; i < 0x1000/4; i++) printf("%08X\n", p[i]);
    munmap(map, 0x1000); close(fd); return 0;
}
```


3. Compílalo en Linux:

```bash
gcc bar.c -o bar
```


4. Descubre el recurso correcto (ejemplo):

```bash
ls /sys/bus/pci/devices/0000:XX:XX.X/
```


5. Ejecuta para obtener los dumps de los BARs:

```bash
sudo ./bar /sys/bus/pci/devices/0000:XX:XX.X/resource2 > dump2.txt
sudo ./bar /sys/bus/pci/devices/0000:XX:XX.X/resource4 > dump4.txt
```


6. Copia los archivos dump2.txt y dump4.txt a la carpeta `dumps/` de tu proyecto en Windows.

---


## Paso 2: Análisis del Dump y Adaptación del Firmware

1. Abre los archivos dump2.txt y dump4.txt y verifica cuál contiene datos válidos (no vacíos o ceros).
2. En `src/pcileech_tlps128_bar_controller.sv`, localiza la instancia de `pcileech_bar_impl_zerowrite4k i_bar0`.
   - Modifica la implementación del BAR para inicializar la memoria con los datos del dump correspondiente.
   - Puedes usar un archivo .coe o inicialización directa en el módulo de memoria.

---


## Paso 3: Modificación de Identificadores (ID) y Serial Number

1. Edita `src/pcileech_pcie_cfg_a7.sv`:
    - Busca la línea:
       ```verilog
       rw[127:64]  <= 64'h0000000101000A35;    // +008: cfg_dsn
       ```
       y reemplázala por tu DSN real (ejemplo):
       ```verilog
       rw[127:64]  <= 64'h684CE00001000000;    // +008: cfg_dsn
       // CAMBIAR AQUÍ: Reemplazar por tu DSN real
       ```
    - Busca la línea:
       ```verilog
       rw[20]      <= 0; // CFGSPACE_STATUS_REGISTER_AUTO_CLEAR [master abort flag]
       ```
       y cámbiala a:
       ```verilog
       rw[20]      <= 1; // CFGSPACE_STATUS_REGISTER_AUTO_CLEAR [master abort flag]
       // CAMBIAR AQUÍ: Poner en 1 para habilitar Master Abort
       ```
2. Si existe `pcileech_ids.sv`, modifica VID, PID y SubIDs para que coincidan con tu tarjeta donante.

---


## Paso 4: Configuración de la IP PCIe en Vivado

1. Abre Vivado y carga el proyecto.
2. Ve al IP `pcie_7x_0`.
3. Activa los BAR necesarios:

   * Ejemplo: BAR0 desactivado, BAR2 y BAR4 activados (según los dumps que obtuviste)
   * Tamaño: según el dump (ejemplo: 4K o 16K)
4. Ajusta:

   * Max Payload Size: 128 o 256 (según Telescan o el dispositivo donante)
   * Max Read Request Size: igual que el donante
   * Extended Tag Field: activa si el donante lo tiene

---


## Paso 5: Síntesis y Generación de Bitstream

1. Ejecuta "Generate Output Products" para el IP PCIe.

   * Opcion: `Out of context per IP`
2. Corre la Synthesis principal.
3. Corrige errores de módulos o puertos si aparecen (por ejemplo: `rst`, `valid`, etc.)
4. Ejecuta Implementation
5. Genera `bitstream.bit`

---


## Paso 6: Programación (Flash) y Pruebas

1. Usa OpenOCD o tu herramienta para flashear

```bash
openocd -f board.cfg -c "init; pld load 0 bitstream.bit; exit"
```

2. En Windows, revisa en el Device Manager si aparece como el dispositivo clonado.
3. Realiza pruebas de lectura/escritura sobre los BARs para verificar el funcionamiento.

---


---


## Implementación de Shadow Configuration Space (Shadow CFG) y Writemask

Esta sección te guía paso a paso para implementar el Shadow Configuration Space en tu proyecto PCILeech DMA, siguiendo la guía de Silverr12.

### 1. Extraer la configuración PCIe del donante
- Usa Telescan en Windows para guardar la configuración PCIe de tu dispositivo donante en un archivo `.tlscan`.

### 2. Convertir el dump a formato .coe
- Descarga el script [`telescan_to_coe.py`](https://github.com/Rakeshmonkee/DMA/blob/main/.tlscan%20to%20.coe/telescan_to_coe.py).
- Ejecuta el script sobre tu archivo `.tlscan` para obtener un archivo `.coe` compatible con Xilinx:
   ```bash
   python telescan_to_coe.py tu_archivo.tlscan pcileech_cfgspace.coe
   ```

### 3. Reemplazar el archivo de configuración
- Copia el archivo `.coe` generado como `pcileech_cfgspace.coe` en la carpeta IP o src de tu proyecto Vivado.

### 4. Ajustar takeover en el core PCIe
- En Vivado, abre el archivo `pcie_7x_0_core_top`.
- Cambia los parámetros `EXT_CFG_CAP_PTR` y `EXT_CFG_XP_CAP_PTR` a `0A` (o el valor adecuado según el offset donde el shadow cfg debe tomar control).
   - Cálculo: offset en hex / 4 → en hex (ejemplo: para offset 0x28, 0x28/4 = 0xA).

### 5. (Opcional pero recomendado) Implementar writemask
- En `pcileech_fifo.sv`, cambia la línea:
   ```verilog
   rw[206] <= 1'b0;  // CFGTLP PCIE WRITE ENABLE
   ```
   a:
   ```verilog
   rw[206] <= 1'b1;  // CFGTLP PCIE WRITE ENABLE
   ```
- Descarga el script [`writemask.it`](https://github.com/Simonrak/writemask.it) y úsalo para generar el archivo `pcileech_cfgspace_writemask.coe` a partir de tu `.coe`:
   - Sigue las instrucciones del repositorio para el uso del script.
- Reemplaza el archivo de writemask en tu proyecto.

### 6. Generar bitstream y probar
- Genera el bitstream en Vivado.
- Flashea la FPGA y verifica el funcionamiento.

---

### Recursos útiles
- [Guía original de Silverr12](https://github.com/Silverr12/DMA-CFW-Guide/blob/main/Shadow_cfg_space.md)
- [Script telescan_to_coe.py](https://github.com/Rakeshmonkee/DMA/blob/main/.tlscan%20to%20.coe/telescan_to_coe.py)
- [Script writemask.it](https://github.com/Simonrak/writemask.it)

---

**Consejos adicionales:**
- Revisa siempre los comentarios `// CAMBIAR AQUÍ` en los archivos `.sv` para saber dónde personalizar.
- Haz backup de los archivos originales antes de modificar.
- Usa control de versiones (Git) para llevar registro de los cambios.

---

**Autor:** DMN_CBA
Creado para el ecosistema **DMN_SHOP** y la comunidad hispana interesada en investigación avanzada FPGA/DMA/PCIe.

Para uso educativo y de investigación. No se recomienda su uso con fines maliciosos.

© 2025 DMN_ENGINE | Demon_Cuba | Todos los derechos reservados.


