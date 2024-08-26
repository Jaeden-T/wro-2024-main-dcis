
# Open the original large image
from PIL import Image, ImageDraw
import PIL
import math
PIL.Image.MAX_IMAGE_PIXELS = 9331200000
# Variables for original image size and DPI
original_image_path = "WRO-2024_FutureEngineers_Playfield_1 (1).jpg"
original_dpi = 180.0  # Use a float value for DPI

# Variables for page size and DPI
page_width_mm = 297  # in mm
page_height_mm = 420  # in mm
page_dpi = 180.0  # Use a float value for DPI

# Convert page dimensions from mm to pixels using floating point arithmetic
page_width_px = math.floor(page_width_mm * page_dpi / 25.4 + 0.5)  # Add 0.5 and then floor to round to nearestnteger
page_height_px = math.floor(page_height_mm * page_dpi / 25.4 + 0.5)  # Add 0.5 and then floor to round to nearestinteger

# Open the original image
image = Image.open(original_image_path)
image_width_px, image_height_px = image.size

# Calculate the number of pages in X and Y directions using floating point arithmetic
num_pages_x = math.ceil(image_width_px / page_width_px)  # Use ceil to round up to nearest integer
num_pages_y = math.ceil(image_height_px / page_height_px)  # Use ceil to round up to nearest integer

# Split the image and handle whitespace
for i in range(num_pages_x):
    for j in range(num_pages_y):
        # Calculate the box for each page (left, upper, right, lower)
        left = i * page_width_px
        upper = j * page_height_px
        right = min(left + page_width_px, image_width_px)  # Use min to find minimum of two values
        lower = min(upper + page_height_px, image_height_px)  # Use min to find minimum of two values

        # Crop the image to the current page size using floating point arithmetic
        cropped_image = image.crop((left, upper, right, lower))

        # Create a blank page with the correct size and a gray background
        page_image = Image.new("RGB", (page_width_px, page_height_px), "#808080")

        # Paste the cropped image onto the blank page
        page_image.paste(cropped_image, (0, 0))

        # Save the page
        page_image.save(f"V-3page_{i+1}_{j+1}.jpg")

print(page_width_px, page_height_px, num_pages_x, num_pages_y)
print("Page total in pixels (x) and page height in pixels")
print(page_width_px * num_pages_x, page_height_px * num_pages_y)