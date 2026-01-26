"""CLI para eliminar marcas de agua de imágenes."""

import click
from pathlib import Path
from PIL import Image

from .detector import WatermarkDetector, create_corner_mask
from .inpainter import WatermarkInpainter


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "-o", "--output",
    type=click.Path(),
    help="Ruta de salida. Por defecto: <nombre>_clean.<ext>"
)
@click.option(
    "--confidence",
    default=0.5,
    type=float,
    help="Umbral de confianza YOLO (0.0-1.0)"
)
@click.option(
    "--padding",
    default=10,
    type=int,
    help="Píxeles extra alrededor de la marca detectada"
)
@click.option(
    "--fallback-corner",
    is_flag=True,
    default=True,
    help="Usar esquina inferior derecha si YOLO no detecta nada (por defecto: activado)"
)
@click.option(
    "--no-fallback",
    is_flag=True,
    help="Desactivar fallback de esquina"
)
@click.option(
    "--corner",
    type=click.Choice(["bottom-right", "bottom-left", "top-right", "top-left"]),
    default="bottom-right",
    help="Esquina para fallback"
)
@click.option(
    "--corner-width",
    default=0.12,
    type=float,
    help="Proporción del ancho para la máscara de esquina (0.0-1.0)"
)
@click.option(
    "--corner-height",
    default=0.08,
    type=float,
    help="Proporción del alto para la máscara de esquina (0.0-1.0)"
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Mostrar información detallada"
)
@click.option(
    "--force-corner",
    is_flag=True,
    help="Usar siempre la máscara de esquina, sin detección YOLO"
)
@click.option(
    "--method",
    type=click.Choice(["lama", "opencv"]),
    default="lama",
    help="Método de inpainting: lama (mejor calidad) u opencv (más rápido)"
)
def main(
    input_path: str,
    output: str | None,
    confidence: float,
    padding: int,
    fallback_corner: bool,
    no_fallback: bool,
    corner: str,
    corner_width: float,
    corner_height: float,
    verbose: bool,
    force_corner: bool,
    method: str,
):
    """
    Elimina marcas de agua de imágenes usando IA.

    Usa YOLO para detectar la marca y LaMa para eliminarla.
    Si YOLO no detecta nada, usa la esquina inferior derecha por defecto.

    Ejemplos:

        watermark-remover imagen.png

        watermark-remover imagen.png -o limpia.png --verbose

        watermark-remover imagen.png --force-corner --corner-width 0.15
    """
    input_path = Path(input_path)

    # Determinar ruta de salida
    if output:
        output_path = Path(output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_clean{input_path.suffix}"

    if verbose:
        click.echo(f"Procesando: {input_path}")

    # Cargar imagen
    try:
        image = Image.open(input_path).convert("RGB")
    except Exception as e:
        click.echo(f"Error al cargar imagen: {e}", err=True)
        raise SystemExit(1)

    if verbose:
        click.echo(f"Tamaño: {image.size[0]}x{image.size[1]}")

    mask = None
    use_fallback = no_fallback is False and fallback_corner

    # Detectar marca de agua con YOLO (si no se fuerza esquina)
    if not force_corner:
        if verbose:
            click.echo("Detectando marcas de agua con YOLO...")

        try:
            detector = WatermarkDetector(confidence=confidence)
            detections = detector.detect(image)

            if detections:
                if verbose:
                    click.echo(f"Detectadas {len(detections)} marca(s) de agua")
                    for i, det in enumerate(detections):
                        click.echo(f"  {i+1}. Confianza: {det['confidence']:.2f}, BBox: {det['bbox']}")

                mask = detector.create_mask(image.size, detections, padding)
            elif verbose:
                click.echo("YOLO no detectó marcas de agua")

        except Exception as e:
            if verbose:
                click.echo(f"Error en detección YOLO: {e}")
            # Continuar con fallback si está habilitado

    # Fallback: usar esquina
    if mask is None:
        if force_corner or use_fallback:
            if verbose:
                click.echo(f"Usando máscara de esquina: {corner}")

            mask = create_corner_mask(
                image.size,
                corner=corner,
                width_ratio=corner_width,
                height_ratio=corner_height,
                padding=padding,
            )
        else:
            click.echo("No se detectaron marcas de agua y fallback está desactivado", err=True)
            raise SystemExit(1)

    # Inpainting
    if verbose:
        click.echo(f"Aplicando inpainting con {method.upper()}...")

    try:
        inpainter = WatermarkInpainter(method=method)
        result = inpainter.inpaint(image, mask)
    except Exception as e:
        click.echo(f"Error en inpainting: {e}", err=True)
        raise SystemExit(1)

    # Guardar resultado
    try:
        result.save(output_path)
        click.echo(f"Guardado: {output_path}")
    except Exception as e:
        click.echo(f"Error al guardar: {e}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
