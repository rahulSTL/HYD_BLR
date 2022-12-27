from fpdf import FPDF
import os

pdf = FPDF()
pdf.set_auto_page_break(0)

img_list = [x for x in os.listdir("updated")]

for img in img_list:
    pdf.add_page()
    image = "updated\\"+img
    pdf.image(image,w=200,h=120)


pdf.output("will_it.pdf")
print("completed")