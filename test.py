from fpdf import FPDF
import os

pdf = FPDF()
pdf.set_auto_page_break(0)

img_list = [x for x in os.listdir("updated1")]

for img in img_list:
    pdf.add_page()
    image = "updated1\\"+img
    # surface.set_size(842, 595)
    pdf.image(image,w=210,h=297)
    # surface.set_size(842, 595)


pdf.output("checking.pdf")
print("compltd")