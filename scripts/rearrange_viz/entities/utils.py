from PIL import Image, ImageChops


def add_tint_to_rgb(image, tint_color):
    """
    Adds a tint color to the RGB channels of an image while preserving the alpha channel.

    Parameters:
        image (PIL.Image.Image): The original image.
        tint_color (tuple): The RGB color tuple (r, g, b) to be applied as a tint.

    Returns:
        PIL.Image.Image: The tinted image with preserved alpha channel.
    """
    # Extract the alpha channel from the original image
    r, g, b, alpha = image.split()

    # Create a solid color image of the same size as the original image
    tint = Image.new("RGB", image.size, tint_color)

    # Composite the RGB channels with the tint color
    tinted_rgb = ImageChops.screen(tint.convert("RGB"), image.convert("RGB"))

    # Return the composite image with original alpha channel
    return Image.merge(
        "RGBA",
        (
            tinted_rgb.split()[0],
            tinted_rgb.split()[1],
            tinted_rgb.split()[2],
            alpha,
        ),
    )
