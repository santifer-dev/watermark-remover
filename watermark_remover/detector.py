"""Detección de marcas de agua usando YOLOv8."""

from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np


class WatermarkDetector:
    """Detector de marcas de agua usando YOLOv8."""

    def __init__(self, model_path: str | None = None, confidence: float = 0.5):
        """
        Inicializa el detector.

        Args:
            model_path: Ruta al modelo YOLO. Si es None, usa yolov8n.pt
            confidence: Umbral de confianza mínimo (0.0 - 1.0)
        """
        from ultralytics import YOLO

        if model_path and Path(model_path).exists():
            self.model = YOLO(model_path)
        else:
            # Usar modelo base YOLOv8 nano
            self.model = YOLO("yolov8n.pt")

        self.confidence = confidence

    def detect(self, image: Image.Image) -> list[dict]:
        """
        Detecta objetos en la imagen que podrían ser marcas de agua.

        Args:
            image: Imagen PIL en modo RGB

        Returns:
            Lista de detecciones con bbox [x1, y1, x2, y2] y confianza
        """
        results = self.model(image, conf=self.confidence, verbose=False)
        detections = []

        for r in results:
            for box in r.boxes:
                detections.append({
                    "bbox": box.xyxy[0].tolist(),  # [x1, y1, x2, y2]
                    "confidence": float(box.conf),
                    "class": int(box.cls) if box.cls is not None else None,
                })

        return detections

    def create_mask(
        self,
        image_size: tuple[int, int],
        detections: list[dict],
        padding: int = 10,
    ) -> Image.Image:
        """
        Crea máscara binaria a partir de las detecciones.

        Args:
            image_size: Tamaño (width, height) de la imagen
            detections: Lista de detecciones con bbox
            padding: Píxeles extra alrededor de cada detección

        Returns:
            Máscara PIL en modo L (blanco = área a eliminar)
        """
        mask = Image.new("L", image_size, 0)
        draw = ImageDraw.Draw(mask)

        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            # Aplicar padding
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(image_size[0], x2 + padding)
            y2 = min(image_size[1], y2 + padding)
            draw.rectangle([x1, y1, x2, y2], fill=255)

        return mask


def create_corner_mask(
    image_size: tuple[int, int],
    corner: str = "bottom-right",
    width_ratio: float = 0.15,
    height_ratio: float = 0.08,
    padding: int = 10,
) -> Image.Image:
    """
    Crea una máscara en una esquina de la imagen (fallback cuando YOLO no detecta).

    Args:
        image_size: Tamaño (width, height) de la imagen
        corner: Esquina a enmascarar ("bottom-right", "bottom-left", "top-right", "top-left")
        width_ratio: Proporción del ancho de la imagen para la máscara
        height_ratio: Proporción del alto de la imagen para la máscara
        padding: Píxeles extra de margen

    Returns:
        Máscara PIL en modo L
    """
    width, height = image_size
    mask_width = int(width * width_ratio)
    mask_height = int(height * height_ratio)

    mask = Image.new("L", image_size, 0)
    draw = ImageDraw.Draw(mask)

    if corner == "bottom-right":
        x1 = width - mask_width - padding
        y1 = height - mask_height - padding
        x2 = width - padding
        y2 = height - padding
    elif corner == "bottom-left":
        x1 = padding
        y1 = height - mask_height - padding
        x2 = mask_width + padding
        y2 = height - padding
    elif corner == "top-right":
        x1 = width - mask_width - padding
        y1 = padding
        x2 = width - padding
        y2 = mask_height + padding
    elif corner == "top-left":
        x1 = padding
        y1 = padding
        x2 = mask_width + padding
        y2 = mask_height + padding
    else:
        raise ValueError(f"Esquina no válida: {corner}")

    draw.rectangle([x1, y1, x2, y2], fill=255)
    return mask
