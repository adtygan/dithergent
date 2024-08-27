import sys
from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
MAX_WIDTH = 500  # Maximum width of the output image

def grayify(image):
    return image.convert('L')

def pixels_to_ascii(image):
    pixels = image.getdata()
    return "".join([ASCII_CHARS[pixel//25] for pixel in pixels])

def resize_image(image, new_width):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def image_to_ascii(image_path):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Unable to open image file {image_path}.")
        print(e)
        return None

    # Resize image if it's too large
    if image.width > MAX_WIDTH:
        image = resize_image(image, MAX_WIDTH)

    gray_image = grayify(image)
    ascii_str = pixels_to_ascii(gray_image)

    # Create a new image for the ASCII art
    font = ImageFont.load_default()
    bbox = font.getbbox('A')
    char_width, char_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    img_width, img_height = image.size
    output_image = Image.new('L', (img_width * char_width, img_height * char_height), color=255)
    draw = ImageDraw.Draw(output_image)

    for i, char in enumerate(ascii_str):
        x = (i % img_width) * char_width
        y = (i // img_width) * char_height
        draw.text((x, y), char, font=font, fill=0)

    return output_image

def main():
    if len(sys.argv) < 2:
        print("Usage: python renderer.py <image_path> <output_path>")
        return

    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "render.png"

    ascii_img = image_to_ascii(image_path)
    if ascii_img:
        ascii_img.save(output_path)
        print("\n" + "=" * 40)
        print(f"🌊🌊🌊🌊🌊🌊 Render Complete 🌊🌊🌊🌊🌊🌊")
        print(f"[Output] {output_path}")
        print("=" * 40 + "\n")

if __name__ == "__main__":
    main()
