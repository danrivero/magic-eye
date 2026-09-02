from PIL import Image, ImageOps, ImageDraw
import numpy as np

def make_magic_eye(
    path, 
    pattern_path=None, 
    image_height=None, 
    image_width=None, 
    popout=True, 
    guide=False,
    pattern_width = 100,
    max_disparity=30,
    output_path="new_magic_eye.png"
):
    # open file
    base = Image.open(path).convert("L")
    width, height = base.size

    # preparing depth map
    # check canvas size
    if image_width is None or image_height is None:
        image_width, image_height = width, height

    if image_height < height or image_width < width:
        print("FATAL ERROR! Dimensions too small!")
        return

    canvas = Image.new("L", (image_width, image_height), color=0)

    paste_x = (image_width - width) // 2
    paste_y = (image_height - height) // 2
    canvas.paste(base, (paste_x, paste_y))
    base = canvas

    if popout == False:
        base = ImageOps.invert(base)

    base_arr = np.array(base, dtype=np.float32) / 255.0

    output_arr = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    if pattern_path:
        return
    else:
        output_arr[:, :pattern_width] = np.random.randint(
            0, 256, (image_height, pattern_width, 3), dtype=np.uint8
        )

    for y in range(image_height):
        for x in range(pattern_width, image_width):
            d = base_arr[y, x]
            sep = pattern_width - int(d * max_disparity)
            output_arr[y, x] = output_arr[y, x - sep]

    result_img = Image.fromarray(output_arr)

    if guide:
        draw = ImageDraw.Draw(result_img)
        dot_y = 30
        dot_r = 5
        center_x = image_width // 2

        dot1_x = center_x - (pattern_width // 2)
        dot2_x = center_x + (pattern_width // 2)

        for x in (dot1_x, dot2_x):
            draw.ellipse([x - dot_r, dot_y - dot_r, x + dot_r, dot_y + dot_r], fill=(0, 0, 0))

    result_img.save(output_path)
    result_img.show()

if __name__ == "__main__":
    path = input("Enter base filename: ")

    res = input("Use custom pattern? (Y/N) ")
    pattern_path = None
    if res == "Y" or res == "y":
        pattern_path = input("Enter pattern filename: ")

    res = input("Specify canvas size? (Y/N) ")
    image_width = None
    image_height = None
    if res == "Y" or res == "y":
        image_width = int(input("Enter width in px: "))
        image_height = int(input("Enter height in px: "))
        
    res = input("Pop out (1) or push back (2)? ")
    popout = False
    if res == "1":
        popout = True
    
    res = input("Include guide dots? (Y/N) ")
    guide = False
    if res == "Y" or res == "y":
        guide = True

    make_magic_eye(path, pattern_path, image_height, image_width, popout, guide)