# Watermark Remover

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](README.es.md)

Herramienta CLI para eliminar marcas de agua de imágenes usando inteligencia artificial.

## Características

- **Detección automática** con YOLO - detecta marcas de agua sin configuración manual
- **Inpainting con LaMa** - reconstruye la imagen de forma realista
- **Fallback inteligente** - usa la esquina de la imagen si no se detecta nada
- **Método OpenCV alternativo** - opción más rápida para casos simples

## Ejemplo

| Antes | Después |
|:-----:|:-------:|
| <img src="examples/before.png" width="400"> | <img src="examples/after.png" width="400"> |

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

## Uso

```bash
# Uso básico
watermark-remover imagen.png

# Especificar salida
watermark-remover imagen.png -o imagen_limpia.png

# Modo verbose (ver detalles)
watermark-remover imagen.png -v

# Forzar limpieza de esquina (sin detección YOLO)
watermark-remover imagen.png --force-corner

# Ajustar tamaño de la máscara de esquina
watermark-remover imagen.png --force-corner --corner-width 0.15 --corner-height 0.10

# Usar método rápido (OpenCV)
watermark-remover imagen.png --method opencv
```

## Opciones

| Opción | Descripción | Default |
|--------|-------------|---------|
| `-o, --output` | Ruta del archivo de salida | `<nombre>_clean.<ext>` |
| `--confidence` | Umbral de confianza YOLO (0.0-1.0) | 0.5 |
| `--padding` | Píxeles extra alrededor de la marca | 10 |
| `--fallback-corner` | Usar esquina si YOLO no detecta | Activado |
| `--no-fallback` | Desactivar fallback de esquina | - |
| `--corner` | Esquina para fallback | bottom-right |
| `--corner-width` | Proporción del ancho (0.0-1.0) | 0.12 |
| `--corner-height` | Proporción del alto (0.0-1.0) | 0.08 |
| `--force-corner` | Usar esquina sin detección YOLO | - |
| `--method` | Método de inpainting: `lama` o `opencv` | lama |
| `-v, --verbose` | Mostrar información detallada | - |

## Requisitos

- Python 3.10+
- ~2GB RAM (para el modelo LaMa)

El modelo LaMa (~200MB) se descarga automáticamente en `~/.cache/torch/` la primera vez que se usa.

## Licencia

MIT
