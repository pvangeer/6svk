from PIL import ImageFont
import os


def measure_text(text: str, font_size: int):
    """
    Returns the predicted width and height of a given text in pixels.

    Parameters:
        text (str): The text to measure.
        font_path (str): Path to the .ttf font file (e.g., Arial.ttf).
        font_size (int): Font size in pixels.

    Returns:
        (width, height): Tuple of predicted text dimensions in pixels.
    """

    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "ARIAL.TTF"), font_size)

    # This requires pillow >= 8.0. Otherwise we should use font.getsize(text)
    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]

    return width, height
