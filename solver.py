from PIL import Image, ImageChops, ImageEnhance
import numpy as np

# open file
base = Image.open("magic-eye.png").convert("RGB")
base_arr = np.array(base, dtype=np.float32)
width, height = base.size
offset = 0

for i in range(int(width/2)):
    offset += 1
    shifted = ImageChops.offset(base, -offset, 0).convert("RGB")
    shifted_arr = np.array(shifted, dtype=np.float32)
    mae = np.mean(np.abs(base_arr - shifted_arr))
    print(f"Error: {mae}, Offset: {offset}")

final_shift = ImageChops.offset(base, -158, 0).convert("RGB")
difference = ImageChops.difference(base, final_shift)
difference.show()

difference.save("solved.png")
print("Saved solved image to 'solved.png'")
