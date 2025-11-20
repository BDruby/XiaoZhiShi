import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from flask import current_app

def generate_og_image(title, author_name, category_name, site_name="XiaoZhiShi"):
    """
    Generates an Open Graph image for a post.
    
    Args:
        title (str): The title of the post.
        author_name (str): The name of the author.
        category_name (str): The name of the category.
        site_name (str): The name of the site.
        
    Returns:
        Image: A PIL Image object.
    """
    # Canvas settings
    width = 1200
    height = 630
    background_color = (240, 249, 255)  # Light blue-ish white (primary-50 equivalent)
    
    # Create base image
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)
    
    # Add a subtle gradient (optional, keeping it simple for now with a solid bg + accent)
    # Let's add a decorative bar at the top
    draw.rectangle([(0, 0), (width, 20)], fill=(14, 165, 233)) # primary-500
    
    # Fonts
    # Try to load a nice font, fallback to default
    try:
        # Windows usually has arial.ttf
        font_path = "arial.ttf" 
        # You might want to bundle a font file in your static folder for consistency
        # e.g., os.path.join(current_app.root_path, 'static', 'fonts', 'Inter-Bold.ttf')
        
        title_font = ImageFont.truetype(font_path, 70)
        meta_font = ImageFont.truetype(font_path, 40)
        site_font = ImageFont.truetype(font_path, 30)
    except IOError:
        title_font = ImageFont.load_default()
        meta_font = ImageFont.load_default()
        site_font = ImageFont.load_default()

    # Text Colors
    title_color = (17, 24, 39) # gray-900
    meta_color = (75, 85, 99) # gray-600
    accent_color = (2, 132, 199) # primary-600
    
    # Layout calculations
    padding = 80
    
    # Draw Site Name (Top Left)
    draw.text((padding, padding), site_name, font=site_font, fill=accent_color)
    
    # Draw Title (Centered Vertically-ish)
    # Wrap text
    wrapper = textwrap.TextWrapper(width=20) # Adjust width based on font size
    title_lines = wrapper.wrap(title)
    
    # Calculate total height of title block
    line_height = 80 # Approximate for 70px font
    total_title_height = len(title_lines) * line_height
    
    start_y = (height - total_title_height) // 2 - 40 # Shift up a bit
    
    for line in title_lines:
        # Center text horizontally
        # getbbox returns (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), line, font=title_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        draw.text((x, start_y), line, font=title_font, fill=title_color)
        start_y += line_height
        
    # Draw Meta Info (Bottom)
    # Author | Category
    meta_text = f"{author_name}  •  {category_name}"
    bbox = draw.textbbox((0, 0), meta_text, font=meta_font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height - padding - 40
    
    draw.text((x, y), meta_text, font=meta_font, fill=meta_color)
    
    return img
