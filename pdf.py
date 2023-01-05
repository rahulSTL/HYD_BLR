import os
from PIL import Image
from fpdf import FPDF

# Set the directory containing the images
image_dir = r"C:\Users\sri.krishna\Documents\GitHub\HYD_BLR\updated1\\"

# Create a new PDF document
pdf = FPDF('L', 'mm', (297, 420))

# Set page size to A3
#pdf.set_page_format('A3')
#pdf.set_page_orientation('L')

# Add a new page to the PDF
pdf.add_page()


# Iterate through all the image files in the directory
count=0
for file in os.listdir(image_dir):
    # Open an image file
    with Image.open(os.path.join(image_dir, file)) as im:
        # Get the width and height of the image
        print("Loop started",count)
        width, height = im.size

        # Calculate the width and height ratios
        width_ratio = width / pdf.w
        height_ratio = height / pdf.h
        print("Lood in process",count)
        # Use the larger ratio to scale the image
        if width_ratio > height_ratio:
            pdf.image(os.path.join(image_dir, file), x=0, y=40, w=pdf.w, h=height / width_ratio)
        else:
            pdf.image(os.path.join(image_dir, file), x=0, y=0, w=width / height_ratio, h=pdf.h)
        print("Process loob in initition phase before adding page",count)
        # Add a new page for the next image
        pdf.add_page()
        print("Process ended for 1 page",count)
        count+=1

# Save the PDF
print("Saving started")
pdf.output(r"C:\Users\sri.krishna\Desktop\final_solution.pdf")