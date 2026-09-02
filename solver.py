from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def solve_magic_eye(path, output_path="solved.png", beginning_buffer=15):
    # open file
    base = Image.open(path).convert("RGB")
    base_arr = np.array(base, dtype=np.float32)
    width, height = base.size

    offset = 0
    # stores offset corresponding to lowest difference
    low_offset = 0
    # initial max difference
    low_diff = 255

    # find offset with lowest difference
    for i in range(int(3*width/4)):
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

    revealed.save("solved.png")
    print("Saved solved image to 'solved.png'")

if __name__ == "__main__":
    path = input("Enter filename: ")
    solve_magic_eye(path)
