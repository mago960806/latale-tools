from PIL import Image

image = Image.open("Snipaste_2022-02-03_23-31-33.png")

count = 0

h, w = (36, 36)

for i in range(8):
    for j in range(8):
        box = (j * h, i * h, (j + 1) * w, (i + 1) * w)
        new_image = image.crop(box)
        count += 1
        # new_image.save(f"images/ITEMETC_ICON12/{count}.BMP")
        new_image.save(f"{count}.BMP")
