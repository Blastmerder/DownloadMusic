from PIL import Image


def crop(path, new_path: str = None, crop_by: int = 1):
    img = Image.open(path)
    pos1 = (img.width - img.height) // 2 + 60
    if crop_by == 0:
        box = (0, 60, img.width - pos1 * 2, img.height - 60)
    elif crop_by == 1:
        box = (pos1, 60, img.width-pos1, img.height-60)
    else:
        box = (pos1 * 2, 60, img.width, img.height-60)

    img2 = img.crop(box)
    img2.save(path) if new_path is None else img2.save(new_path)

