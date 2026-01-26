"""Setup para watermark-remover."""

from setuptools import setup, find_packages

setup(
    name="watermark-remover",
    version="0.1.0",
    description="Elimina marcas de agua de imágenes usando YOLO + LaMa",
    author="santifer-dev",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "ultralytics>=8.0.0",
        "simple-lama-inpainting>=0.1.0",
        "Pillow>=9.0.0",
        "opencv-python>=4.7.0",
        "numpy>=1.24.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "watermark-remover=watermark_remover.cli:main",
        ],
    },
)
