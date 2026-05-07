from PIL import Image, ImageDraw, ImageFont
import os

# Create static/images directory if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Logo 1: SMC Logo (Simple, clean)
def create_smc_logo():
    width, height = 200, 80
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Blue background
    draw.rectangle([(10, 10), (190, 70)], fill=(94, 111, 191, 255), outline=(94, 111, 191, 255))

    # White text "SMC"
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    draw.text((40, 15), "SMC", font=font, fill=(255, 255, 255, 255))

    img.save('static/images/smc-logo.png')
    print("✓ smc-logo.png created")

# Logo 2: SMC Tagline (미래의료의중심 SMC)
def create_smc_tagline():
    width, height = 400, 100
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Blue background
    draw.rectangle([(0, 0), (width, height)], fill=(255, 255, 255, 0))

    # Korean text
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Main text
    draw.text((20, 20), "미래의료의 중심", font=font_large, fill=(94, 111, 191, 255))
    draw.text((220, 45), "SMC", font=font_small, fill=(94, 111, 191, 255))

    img.save('static/images/smc-tagline.png')
    print("✓ smc-tagline.png created")

if __name__ == '__main__':
    create_smc_logo()
    create_smc_tagline()
    print("\n✓ All logos created successfully!")
