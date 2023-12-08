import os
import sys
from PIL import Image

def resize_image(input_path, output_path, target_size_kb):
    # Open the image
    with Image.open(input_path) as img:
        # Set initial quality
        quality = 95
        step = 5
        min_quality = 10

        # Loop to adjust image quality to achieve target file size
        while True:
            # Save image with current quality to a temporary file
            img.save(output_path, 'JPEG', quality=quality)

            # Check the size of the saved file
            if os.path.getsize(output_path) < target_size_kb * 1024 or quality <= min_quality:
                break  # Exit loop if file size is small enough or quality is too low

            # Decrease the quality for the next iteration
            quality -= step

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 code.py <image_path> <target_size_kb>")
        sys.exit(1)

    image_path = sys.argv[1]
    target_size_kb = int(sys.argv[2])
    
    if not os.path.isfile(image_path):
        print(f"Error: {image_path} does not exist.")
        sys.exit(1)

    # Create output file name
    base_name, ext = os.path.splitext(image_path)
    output_path = f"{base_name}_{target_size_kb}KB.jpg"

    resize_image(image_path, output_path, target_size_kb)
    print(f"Image saved as {output_path}")

if __name__ == "__main__":
    main()
