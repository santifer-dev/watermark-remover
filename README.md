# Watermark Remover

**[:gb: English](#the-problem)** | **[:es: Español](#es-español)**

> CLI tool to remove watermarks from images using artificial intelligence.

---

## The Problem

Profile photos from LinkedIn, stock images, and other sources often come with annoying watermarks. Manually removing them is tedious and time-consuming.

## The Solution

A CLI tool that uses AI to automatically detect and remove watermarks, reconstructing the image realistically.

---

## Example

| Before | After |
|:------:|:-----:|
| <img src="examples/before.png" width="400"> | <img src="examples/after.png" width="400"> |

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-00FFFF?style=flat&logo=yolo&logoColor=black)
![PyTorch](https://img.shields.io/badge/LaMa-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)

---

## Features

- **Automatic detection** with YOLO - detects watermarks without manual configuration
- **LaMa inpainting** - realistically reconstructs the image
- **Smart fallback** - uses image corner if nothing is detected
- **Alternative OpenCV method** - faster option for simple cases

---

## Installation

```bash
# Clone the repository
git clone https://github.com/santifer-dev/watermark-remover.git
cd watermark-remover

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install
pip install -e .
```

---

## Usage

```bash
# Basic usage
watermark-remover image.png

# Specify output
watermark-remover image.png -o clean_image.png

# Verbose mode (see details)
watermark-remover image.png -v

# Force corner cleaning (no YOLO detection)
watermark-remover image.png --force-corner

# Use fast method (OpenCV)
watermark-remover image.png --method opencv
```

---

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output file path | `<name>_clean.<ext>` |
| `--confidence` | YOLO confidence threshold (0.0-1.0) | 0.5 |
| `--padding` | Extra pixels around the watermark | 10 |
| `--fallback-corner` | Use corner if YOLO doesn't detect | Enabled |
| `--no-fallback` | Disable corner fallback | - |
| `--corner` | Corner for fallback | bottom-right |
| `--corner-width` | Width ratio (0.0-1.0) | 0.12 |
| `--corner-height` | Height ratio (0.0-1.0) | 0.08 |
| `--force-corner` | Use corner without YOLO detection | - |
| `--method` | Inpainting method: `lama` or `opencv` | lama |
| `-v, --verbose` | Show detailed information | - |

---

## Requirements

- Python 3.10+
- ~2GB RAM (for LaMa model)

The LaMa model (~200MB) is automatically downloaded to `~/.cache/torch/` on first use.

---

## License

MIT

---

---

# :es: Español

> Herramienta CLI para eliminar marcas de agua de imágenes usando inteligencia artificial.

---

## El Problema

Las fotos de perfil de LinkedIn, imágenes de stock y otras fuentes suelen venir con molestas marcas de agua. Eliminarlas manualmente es tedioso y consume mucho tiempo.

## La Solución

Una herramienta CLI que usa IA para detectar y eliminar marcas de agua automáticamente, reconstruyendo la imagen de forma realista.

---

## Ejemplo

| Antes | Después |
|:------:|:-----:|
| <img src="examples/before.png" width="400"> | <img src="examples/after.png" width="400"> |

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![YOLO](https://img.shields.io/badge/YOLO-00FFFF?style=flat&logo=yolo&logoColor=black)
![PyTorch](https://img.shields.io/badge/LaMa-EE4C2C?style=flat&logo=pytorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat&logo=opencv&logoColor=white)

---

## Características

- **Detección automática** con YOLO - detecta marcas de agua sin configuración manual
- **Inpainting LaMa** - reconstruye la imagen de forma realista
- **Fallback inteligente** - usa la esquina de la imagen si no detecta nada
- **Método OpenCV alternativo** - opción más rápida para casos simples

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/santifer-dev/watermark-remover.git
cd watermark-remover

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Instalar
pip install -e .
```

---

## Uso

```bash
# Uso básico
watermark-remover image.png

# Especificar salida
watermark-remover image.png -o imagen_limpia.png

# Modo verbose (ver detalles)
watermark-remover image.png -v

# Forzar limpieza de esquina (sin detección YOLO)
watermark-remover image.png --force-corner

# Usar método rápido (OpenCV)
watermark-remover image.png --method opencv
```

---

## Opciones

| Opción | Descripción | Por defecto |
|--------|-------------|-------------|
| `-o, --output` | Ruta del archivo de salida | `<nombre>_clean.<ext>` |
| `--confidence` | Umbral de confianza YOLO (0.0-1.0) | 0.5 |
| `--padding` | Píxeles extra alrededor de la marca | 10 |
| `--fallback-corner` | Usar esquina si YOLO no detecta | Habilitado |
| `--no-fallback` | Desactivar fallback de esquina | - |
| `--corner` | Esquina para fallback | bottom-right |
| `--corner-width` | Ratio de ancho (0.0-1.0) | 0.12 |
| `--corner-height` | Ratio de alto (0.0-1.0) | 0.08 |
| `--force-corner` | Usar esquina sin detección YOLO | - |
| `--method` | Método de inpainting: `lama` u `opencv` | lama |
| `-v, --verbose` | Mostrar información detallada | - |

---

## Requisitos

- Python 3.10+
- ~2GB RAM (para el modelo LaMa)

El modelo LaMa (~200MB) se descarga automáticamente en `~/.cache/torch/` en el primer uso.

---

## Licencia

MIT

---

## Let's Connect

[![Website](https://img.shields.io/badge/santifer.io-000?style=for-the-badge&logo=safari&logoColor=white)](https://santifer.io)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/santifer)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:hola@santifer.io)
