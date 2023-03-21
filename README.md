SLD (Single Line Diagram) is a simple symbolic representation top view of highway with all the elements and objects on the sides of highway. We created the images in-house using python. Whenever a person on the field (physical survey) fills a form data get stored in the database and an image based on all the input redeading entered by the user is prepared.


The main.py contains majorly 3 types of function:
1. get_roadside(),get_crossing() : These fuctions add symbol/image at specified location from database
2. get_road(),get_divider() : These functions add straight lines in the drawing for road/divider and other constant things (doesnt require position)
3. get_annonater(), get_coordinates() : These are used cosmetics and detailing the images.


The final out is list of raw-images which are then passed to combiner.py which adds legend, logo and title to the images. The updated images are then combined to form a merged pdf using pdfmaker.py


