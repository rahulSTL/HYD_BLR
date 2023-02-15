from flask import Flask, request,send_file,render_template, url_for,jsonify
import os as os

app = Flask(__name__)

@app.route('/')
def display_images():
    img_dir = 'static/images' # replace with the path to your image directory
    image_list = os.listdir(img_dir)
    return render_template('display_images.html', image_list=image_list)
if __name__ == '__main__':
   app.run(debug=True)    