import sys
import zlib
from PIL import Image
import io
import json

def compress(input_path, output_path):
    with Image.open(input_path) as img:
        img_rgba = img.convert("RGBA")
        raw_data = img_rgba.tobytes()
        compressed_data = zlib.compress(raw_data)
        # Prepare and write metadata
        metadata = json.dumps({'size': img.size})
        with open(output_path, 'wb') as f:
            f.write(metadata.encode())
            f.write(b'\0')  # Delimiter
            f.write(compressed_data)
            
def decompress(input_path, output_path):
    with open(input_path, 'rb') as f:
        # Read metadata
        metadata = ''
        while True:
            chunk = f.read(1)
            if chunk == b'\0':
                break
            metadata += chunk.decode()
        metadata = json.loads(metadata)
        compressed_data = f.read()
    decompressed_data = zlib.decompress(compressed_data)
    img_rgba = Image.frombytes("RGBA", metadata['size'], decompressed_data)
    img_rgba.save(output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong arguments")
        sys.exit(1)
        
    action = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    if action == '-c':
        compress(input_file, output_file)
    elif action == '-d':
        decompress(input_file, output_file)
    else:
        sys.exit(1)
