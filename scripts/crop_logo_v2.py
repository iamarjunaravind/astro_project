from PIL import Image

def crop_image(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        
        # Get the alpha channel
        alpha = img.split()[-1]
        
        # Also consider near-white pixels as background if they are almost fully opaque
        # but the user sees them as "white space"
        # We'll create a mask where alpha > 0 AND color is not white
        datas = img.getdata()
        
        new_alpha = []
        for item in datas:
            # If pixel is very close to white (e.g., > 250 in all channels)
            if item[0] > 250 and item[1] > 250 and item[2] > 250:
                new_alpha.append(0) # Make it transparent
            else:
                new_alpha.append(item[3]) # Keep original alpha
        
        img.putalpha(Image.new("L", img.size, 0)) # reset alpha
        img.putdata([(item[0], item[1], item[2], a) for item, a in zip(datas, new_alpha)])
        
        # Now get bbox of the new alpha channel
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
            img.save(output_path)
            print(f"Successfully cropped to {bbox}")
        else:
            print("No bounding box found, image might be fully transparent.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import os
    input_file = r"c:\Users\abc\Documents\Cu\astro_project - Copy (5) - Copy - Copy\static\img\logo.png"
    output_file = r"c:\Users\abc\Documents\Cu\astro_project - Copy (5) - Copy - Copy\static\img\logo_cropped_v2.png"
    crop_image(input_file, output_file)
