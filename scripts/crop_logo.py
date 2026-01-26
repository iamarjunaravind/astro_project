from PIL import Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

def crop_logo(input_path, output_path):
    try:
        im = Image.open(input_path)
        im = im.convert("RGBA")
        cropped = trim(im)
        cropped.save(output_path)
        print(f"Successfully cropped {input_path} to {output_path}")
    except Exception as e:
        print(f"Error cropping logo: {e}")

if __name__ == "__main__":
    input_file = r"c:\Users\abc\Documents\Cu\astro_project - Copy (5) - Copy - Copy\static\img\logo.png"
    output_file = r"c:\Users\abc\Documents\Cu\astro_project - Copy (5) - Copy - Copy\static\img\logo_cropped.png"
    crop_logo(input_file, output_file)
