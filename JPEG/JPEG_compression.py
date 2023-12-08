from PIL import Image
import sys
DEFAULT_QUALITY = 75

# quality values range from 1 - 95 (values above 95 increase file size with minimal gain in quality)

def compress_image(input_path, output_path, quality):
    image = Image.open(input_path)
    image.save(output_path, 'JPEG', quality=quality)

def decompress_image(input_path, output_path):
    compressed_image = Image.open(input_path)
    compressed_image.save(output_path)
    
if __name__ == "__main__":
    action = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    
    if action == "-c":
        quality = int(sys.argv[4])
        compress_image(input_path, output_path, quality)
    elif action == "-d":
        decompress_image(input_path, output_path)
    else:
        sys.exit(1)