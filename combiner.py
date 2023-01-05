from PIL import Image
import os
#Read the two images

img_path=r"C:\Users\sri.krishna\Documents\GitHub\HYD_BLR\images_sld1"
for i in os.listdir(img_path):
    image1 = Image.open(os.path.join(img_path,i))
    #image1.show()
    # "C:\Users\Aditya.gupta\Desktop\Fun Projects\testing related\static\legend.jpg"
    image2 = Image.open('updated-1.jpg')
    image3=Image.open('sld.png')
    image4=Image.open('stl.png')
    #image2.show()
    #resize, first image
    # im = Image.open(r"C:\Users\Admin\Pictures\geeks.png")
    width, height = image1.size
    #print(image1.size)
    print(i)
    left = 900
    image1 = image1.crop((left, 200, 7680-600, height-100))
    image2 = image2.resize((1226, 2840))
    image1_size = image1.size
    image2_size = image2.size
    image3 = image3.resize((5000, 400))
    image4 = image4.resize((900, 400))
    new_image = Image.new('RGB',(width, height), (255,255,255))
    new_image.paste(image1,(0,350))
    new_image.paste(image2,(image1_size[0]-100,700))
    new_image.paste(image3,(image1_size[0]-5000,200))
    new_image.paste(image4,(image1_size[0]-80,150))
    fig_name="updated1//"+i
    new_image.save(fig_name,"PNG")
    # new_image.show()