import sys
from PIL import Image
import io

def crop_image_to_size(input_image_path, output_image_path, target_size_kb):
    # Open the input image
    with Image.open(input_image_path) as img:
        # Original dimensions and aspect ratio
        orig_width, orig_height = img.size
        aspect_ratio = orig_width / orig_height

        # Initial crop dimensions (start with full image)
        crop_width = orig_width
        crop_height = orig_height

        # Binary search for optimal crop size
        min_dim = 0
        max_dim = min(orig_width, orig_height)
        while min_dim <= max_dim:
            mid_dim = (min_dim + max_dim) // 2

            # Calculate new dimensions maintaining aspect ratio
            if aspect_ratio > 1:  # Width is greater
                crop_width = mid_dim
                crop_height = int(mid_dim / aspect_ratio)
            else:  # Height is greater or equal
                crop_height = mid_dim
                crop_width = int(mid_dim * aspect_ratio)

            # Crop and save to a binary stream to check size
            img_cropped = img.crop((0, 0, crop_width, crop_height))
            img_byte_arr = io.BytesIO()
            img_cropped.save(img_byte_arr, format='PNG')
            size_kb = len(img_byte_arr.getvalue()) / 1024

            # Adjust dimensions based on size
            if size_kb > target_size_kb:
                max_dim = mid_dim - 1
            elif size_kb < target_size_kb:
                min_dim = mid_dim + 1
            else:
                break

        # Save the final cropped image
        img_cropped.save(output_image_path, format='PNG')

if __name__ == '__main__':
    # Command line arguments: input file, output file, target size in KB
    if len(sys.argv) != 4:
        print("Usage: python3 code.py input.png output.png target_size_kb")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    target_size = int(sys.argv[3])

    crop_image_to_size(input_path, output_path, target_size)
