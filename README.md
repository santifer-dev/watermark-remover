# Watermark Remover

[![en](https://img.shields.io/badge/lang-en-blue.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](README.es.md)

CLI tool to remove watermarks from images using artificial intelligence.

## Features

- **Automatic detection** with YOLO - detects watermarks without manual configuration
- **LaMa inpainting** - realistically reconstructs the image
- **Smart fallback** - uses image corner if nothing is detected
- **Alternative OpenCV method** - faster option for simple cases

## Example

| Before | After |
|:------:|:-----:|
| <img src="examples/before.png" width="400"> | <img src="examples/after.png" width="400"> |

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

# Adjust corner mask size
watermark-remover image.png --force-corner --corner-width 0.15 --corner-height 0.10

# Use fast method (OpenCV)
watermark-remover image.png --method opencv
```

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

## Requirements

- Python 3.10+
- ~2GB RAM (for LaMa model)

The LaMa model (~200MB) is automatically downloaded to `~/.cache/torch/` on first use.

## License

MIT
