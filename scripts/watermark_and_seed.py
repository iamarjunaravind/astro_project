
import os
import sys
import django
import glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from django.core.files import File
from django.conf import settings
import shutil

# Setup Django
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "astro_project.settings")
django.setup()

from astromall.models import Product, ProductImage, Category

ARTIFACT_DIR = r"c:\Users\abc\.gemini\antigravity\brain\d2fae389-3c8e-4489-a737-c416ac22f7b9"
MEDIA_DIR = os.path.join(settings.MEDIA_ROOT, 'product_images')

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

def get_latest_image(keyword):
    search_pattern = os.path.join(ARTIFACT_DIR, f"{keyword}*.png")
    files = glob.glob(search_pattern)
    if not files:
        return None
    return max(files, key=os.path.getctime)

LOGO_PATH = os.path.join(ARTIFACT_DIR, 'logo.png')

def process_image(image_path, output_name):
    try:
        img = Image.open(image_path).convert("RGBA")
        
        # Add Logo Watermark
        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH).convert("RGBA")
            # Resize logo to 20% of image width
            logo_width = int(img.width * 0.2)
            logo_ratio = logo_width / float(logo.width)
            logo_height = int(float(logo.height) * float(logo_ratio))
            logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
            
            # Position: Top Right
            position = (img.width - logo_width - 20, 20)
            
            # Transparency
            # Create a new image for the watermark layer
            watermark = Image.new('RGBA', img.size, (0,0,0,0))
            watermark.paste(logo, position, mask=logo)
            
            # Blend
            img = Image.alpha_composite(img, watermark)

        # Add Text "SreeMantra Certified"
        draw = ImageDraw.Draw(img)
        # Try to use a default font or load one
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
            
        text = "SreeMantra Certified"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        
        # Position: Center
        text_pos = ((img.width - text_w) / 2, (img.height - text_h) / 2)
        
        # Shadow
        draw.text((text_pos[0]+2, text_pos[1]+2), text, font=font, fill=(0,0,0, 128))
        draw.text(text_pos, text, font=font, fill=(255,255,255, 200))
        
        output_path = os.path.join(MEDIA_DIR, output_name)
        img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=90)
        return output_path
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

# Mapping now supports a LIST of source keys for variations
MAPPING = {
    'Ruby': ['ruby_gemstone', 'ruby_velvet', 'ruby_wood'],
    'Emerald': ['emerald_gemstone', 'emerald_velvet', 'emerald_wood'],
    'Yellow Sapphire': ['yellow_sapphire', 'yellow_sapphire_velvet', 'yellow_sapphire_wood'],
    'Blue Sapphire': ['blue_sapphire', 'blue_sapphire_velvet', 'blue_sapphire_wood'],
    'Pearl': ['pearl_gemstone', 'pearl_gemstone', 'pearl_gemstone'], # Fallback
    'Rudraksha': ['five_mukhi_rudraksha', 'one_mukhi_rudraksha', 'five_mukhi_rudraksha'], # Mix
    '1 Mukhi': ['one_mukhi_rudraksha', 'one_mukhi_rudraksha', 'one_mukhi_rudraksha'],
    '5 Mukhi': ['five_mukhi_rudraksha', 'five_mukhi_rudraksha', 'five_mukhi_rudraksha'],
    'Conch': ['conch_shell', 'conch_shell', 'conch_shell'],
    'Yantra': ['shree_yantra', 'shree_yantra', 'shree_yantra'],
    'Shankh': ['conch_shell', 'conch_shell', 'conch_shell'],
    # Generics for missing coverage
    'Homam': ['emerald_wood', 'ruby_wood', 'yellow_sapphire_wood'], # Fallback placeholder as we lack Homam images
    'Pooja': ['shree_yantra', 'conch_shell', 'one_mukhi_rudraksha']  # Fallback mix
}

def seed_products():
    products = Product.objects.all()
    print(f"Found {products.count()} products.")

    for product in products:
        # Determine image source list
        source_keys = None
        for key in MAPPING:
            if key.lower() in product.name.lower() or key.lower() in product.category.name.lower():
                source_keys = MAPPING[key]
                break
        
        # Default Fallback if completely unknown
        if not source_keys:
             source_keys = ['shree_yantra', 'conch_shell', 'ruby_gemstone']
             print(f"No mapping found for {product.name}, using generic fallback.")

        print(f"Processing {product.name} with keys: {source_keys}...")

        # Clear old gallery images first
        ProductImage.objects.filter(product=product).delete()

        processed_paths = []
        for idx, key in enumerate(source_keys):
            # Get Source Image Path
            source_path = get_latest_image(key)
            if not source_path:
                print(f"  Source image not found for key {key}, using first available or skipping.")
                # Try fallback to first key in list if current missing
                if source_keys[0] != key:
                     source_path = get_latest_image(source_keys[0])
                
                if not source_path: continue

            # Unique filename: productID_variationIndex_key.jpg
            final_filename = f"{product.id}_v{idx}_{key}.jpg"
            final_path = process_image(source_path, final_filename)
            
            if final_path:
                processed_paths.append((final_filename, final_path))

        if not processed_paths:
            print("  No images processed successfully.")
            continue

        # Asset 1 -> Main Image
        main_name, main_path = processed_paths[0]
        with open(main_path, 'rb') as f:
            product.image.save(main_name, File(f), save=False)
        
        # Asset 1, 2, 3 -> Gallery (Create ProductImage for ALL, including main one if desired, or just extras)
        # Requirement: "add 3 different images". Usually implies Main + Gallery.
        # Let's add ALL processed paths to ProductImage gallery for full carousel support
        for p_name, p_path in processed_paths:
             img_obj = ProductImage(product=product)
             with open(p_path, 'rb') as f:
                 img_obj.image.save(f"gallery_{p_name}", File(f))
             img_obj.save()

        # Update Description
        if "Original Certified" not in product.description:
            product.description = (
                f"Original Certified {product.name}.\n\n"
                "100% Authentic and Lab Tested via SreeMantra.\n"
                "Energized by our expert Pandits before dispatch.\n"
                "Premium Quality with Certification Card included.\n\n"
                f"{product.description}"
            )
        
        product.save()
        print(f"  Updated {product.name} with {len(processed_paths)} images.")

if __name__ == "__main__":
    seed_products()
