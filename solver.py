from PIL import Image, ImageChops, ImageEnhance
import numpy as np

# open file
path = input("Enter filename: ")
base = Image.open(path).convert("RGB")
base_arr = np.array(base, dtype=np.float32)
width, height = base.size
offset = 0
low_offset = 0

# buffer because initially the difference is 0
low_diff = 255
beginning_buffer = 15

# find offset with lowest difference
for i in range(int(width/2)):
    offset += 1
    shifted_arr = np.roll(base_arr, shift=-offset, axis=1)
    mae = np.mean(np.abs(base_arr - shifted_arr))
    if offset > beginning_buffer and mae < low_diff:
        low_diff = mae
        low_offset = offset
    print(f"Error: {mae}, Offset: {offset}")

final_shift = ImageChops.offset(base, -low_offset, 0).convert("RGB")
difference = ImageChops.difference(base, final_shift)
enhancer = ImageEnhance.Contrast(difference)
revealed = enhancer.enhance(5.0)

difference.save("solved.png")
print("Saved solved image to 'solved.png'")
