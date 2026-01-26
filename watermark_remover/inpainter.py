"""Inpainting de imágenes usando LaMa u OpenCV."""

import os
from PIL import Image
import numpy as np

# Forzar CPU
os.environ["CUDA_VISIBLE_DEVICES"] = ""


class WatermarkInpainter:
    """Elimina marcas de agua usando LaMa u OpenCV."""

    def __init__(self, method: str = "lama"):
        """
        Inicializa el inpainter.

        Args:
            method: "lama" para mejor calidad, "opencv" para compatibilidad
        """
        self.method = method
        self._lama_model = None

    def inpaint(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        """
        Elimina la marca de agua de la imagen usando inpainting.

        Args:
            image: Imagen PIL en modo RGB
            mask: Máscara PIL en modo L (blanco = área a eliminar)

        Returns:
            Imagen PIL con la marca de agua eliminada
        """
        if self.method == "lama":
            return self._inpaint_lama(image, mask)
        else:
            return self._inpaint_opencv(image, mask)

    def _get_lama_model(self):
        """Descarga y carga el modelo LaMa (TorchScript)."""
        if self._lama_model is not None:
            return self._lama_model

        import torch
        from torch.hub import download_url_to_file, get_dir

        # Ruta del modelo
        hub_dir = get_dir()
        model_dir = os.path.join(hub_dir, "checkpoints")
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "big-lama.pt")

        # Descargar si no existe
        if not os.path.exists(model_path):
            url = "https://github.com/enesmsahin/simple-lama-inpainting/releases/download/v0.1.0/big-lama.pt"
            print("Descargando modelo LaMa...")
            download_url_to_file(url, model_path, progress=True)

        # Cargar modelo TorchScript
        print("Cargando modelo LaMa...")
        model = torch.jit.load(model_path, map_location=torch.device("cpu"))
        model.eval()

        self._lama_model = model
        return model

    def _inpaint_lama(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        """Inpainting con LaMa."""
        import torch

        model = self._get_lama_model()

        # Preprocesar imagen
        img_np = np.array(image.convert("RGB")).astype(np.float32)
        mask_np = np.array(mask.convert("L")).astype(np.float32)

        # Normalizar a [0, 1]
        img_tensor = torch.from_numpy(img_np).permute(2, 0, 1).unsqueeze(0) / 255.0
        mask_tensor = torch.from_numpy(mask_np).unsqueeze(0).unsqueeze(0) / 255.0

        # Binarizar máscara (>0.5 = área a eliminar)
        mask_tensor = (mask_tensor > 0.5).float()

        # Inferencia
        with torch.no_grad():
            result = model(img_tensor, mask_tensor)

        # Postprocesar
        result_np = result[0].permute(1, 2, 0).cpu().numpy()
        result_np = np.clip(result_np * 255, 0, 255).astype(np.uint8)

        return Image.fromarray(result_np)

    def _inpaint_opencv(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        """Inpainting con OpenCV (fallback rápido)."""
        import cv2

        # Convertir a numpy
        img_np = np.array(image)
        mask_np = np.array(mask)

        # OpenCV usa BGR
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # Inpainting con Navier-Stokes
        result_bgr = cv2.inpaint(img_bgr, mask_np, inpaintRadius=7, flags=cv2.INPAINT_NS)

        # Convertir de vuelta a RGB
        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

        return Image.fromarray(result_rgb)


class OpenCVInpainter:
    """Inpainter simple usando OpenCV."""

    def inpaint(self, image: Image.Image, mask: Image.Image) -> Image.Image:
        """Elimina la marca usando OpenCV inpainting."""
        import cv2

        img_np = np.array(image)
        mask_np = np.array(mask)

        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        result_bgr = cv2.inpaint(img_bgr, mask_np, inpaintRadius=7, flags=cv2.INPAINT_NS)
        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB)

        return Image.fromarray(result_rgb)
