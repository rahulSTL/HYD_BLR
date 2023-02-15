from flask import Flask, request,send_file,render_template, url_for,jsonify
from selenium import webdriver
from PIL import Image
from matplotlib import pyplot as plt 
import pandas as pd
import os as os
import matplotlib.image as mpimg
import numpy as np
import os
import shutil
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time
from fpdf import FPDF
global location
global img_dir

def annonater(lol,plt,y1,y2,xl):
        plt.annotate(
        '',xy=(xl, y1), xycoords='data',
        xytext=(xl, y2), textcoords='data',color='Red',
        arrowprops=dict(arrowstyle= '<->',color='red'))
        plt.annotate(
        lol, xy=(xl+3, (y1+y2)/2), xycoords='data',color='Red',fontsize=7
        )


def get_path(object):
    path=r"objects/petrols.png"
    zoom=0.6
    if pd.isna(object):
        object='PETROL PUMP'
        # print(object)

    if object=='PETROL PUMP':
        path = r"objects/petrols.png"
        print("into the petrol pump")
        zoom=0.6
    elif "Telecom Room" in object:
        path = r"objects/toll plaza.png"
        zoom=0.08
    elif object=='BUILDING':
        path = r"objects/build.png"
        zoom=0.045
    elif object=='TREE':
        path = r"objects/tree.png"
        zoom==0.48
    elif object=='HOTEL':
        path = r"objects/hotel.png"
        zoom=0.13
    elif object=='MARKET':
        path =  r"objects/market.png"
        zoom=0.065
    elif object=='FARM':
        path = r"objects/Farms.png"
        zoom=0.145
    elif object=='WATER BODY':
        path=r"objects/pond.png"
        zoom=0.04
    elif object=='TEMPLE':
        path=r"objects/temple.png"
        zoom=0.04
    elif object=='Deep Excavation ':
        path=r"objects/excavator.png"
        zoom=0.033
    elif object=='INDUSTRY':
        path=r"objects/factory.png"
        zoom=0.025
    elif object=='TOLL PLAZA RAIKAL (NOC)':
        path=r"objects/toll plaza.png"
        zoom=0.08
    elif object=='Service Road Under Construction':
        path=r"objects/serviceroadconst.png"
        zoom=0.043
    elif object=='KRISHNA RIVER':
        path= r"objects/upper_krishna_river.png"
        zoom=0.13 
    elif object =='FOREST':
        path = r"objects/forest.png"
        zoom=0.2 
    elif object =='HILL':
        path = r"objects/hill.png"
        zoom=0.14    
    elif object =='LAKE':
        path =r"objects/pond.png"
        zoom=0.04
    elif object =='HARD ROCK & TREE':
        path =r"objects/stone.png"
        zoom=0.05   
    elif object =='AGRICULTURE LAND':
        path =r"objects/land.png"
        zoom=0.04 
    elif  object == 'TOLL PLAZA SAKAPUR (Telecom Room)' or 'TOLL PLAZA AMAKATHADU (Telecom Room)' or'TOLL PLAZA KASEPALLI (Telecom Room)' or'TOLL PLAZA MARURU (Telecom Room)' or'TOLL PLAZA BAGEPALLI (Telecom Room)' or'TOLL PLAZA PHULLUR (Telecom Room)':
        path = r"objects/toll plaza.png"
        zoom=0.08
    return (path,zoom)    



def get_crossing(crossing,len):
    path=r"objects/water_crossing.png"
    zoom=0
    path_a=r"objects/eay.png"
    zoom_a=0

    # if crossing=="WATER PIPE LINE":
    #     print(crossing)


    if crossing=="WATER PIPE LINE" and len>0:
        path=r"objects/water_crossing.png"
        zoom=0.11
        print("going into water pipe:")
        path_a=r"objects/eay.png"
        zoom_a=0.035
    elif crossing=="BRIDGE" and len>0:
        path=r"objects/Bridge_upper_part2.png"
        zoom=0.15
        print("Going into the bridge:")
        path_a=r"objects/Bridge_upper_part.png"
        zoom_a=0.15
    elif crossing=="CULVERT" and len>0:
        path=r"objects/Culvert_part2.png"
        zoom=0.15
        path_a=r"objects/Culvert_part.png"
        zoom_a=0.15
    elif crossing=="RAIL CROSSING" and len>0:
        path=r"objects/rail.png"
        zoom=0.4
        path_a=r"objects/rail.png"
        zoom_a=0.4
    elif crossing=="ROAD CROSSING" and len>0:
        path=r"objects/road_crossing.png"
        zoom=0.07
        path_a=r"objects/road_crossing.png"
        zoom_a=0.07 
    elif crossing=="UNDER PASS" and len>0:
        path=r"objects/under.png"
        zoom=0.04
        path_a=r"objects/under.png"
        zoom_a=0.04
    return (path,zoom,path_a,zoom_a)   

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("test.html")

@app.route('/', methods=["POST", "GET"])
def my_form():
     df=pd.read_excel(r'NHAI FINAL SURVEY DATA.xlsx')
     if request.method == "POST":
         st=request.form["n1"]
         en=request.form["n2"]
        #  df=pd.read_excel(r'NHAI FINAL SURVEY DATA.xlsx')
         df= df.sort_values(by= "Chainage")
         xmin=int(st)
         xmax=int(en)
         print("Entered values are:",xmin,xmax)
         levels=int((xmax-xmin)/3000)
        #  levels=1
         x1=xmin
         print(df['Executable Offset From RC'][0])
         for i in range(0,levels):
                fig,axs=plt.subplots(nrows=3,ncols=1,figsize=(20,10))
                for j in range(0,3):
                    x1+=1000

                    df_filter=df[df['Chainage']<x1]
                    # print(df1.info())
                    df_filter=df_filter[df_filter['Chainage']>=x1-1000]
                    # print(df1.info())
                    axis_counter = 0
                    y,x,len=0,202000,1000
                    d=300
                    y_divider1=y+d/2
                    y_divider2=y-d/2
                    mid_div=(y_divider1+y_divider2)/2
                    #plt.hlines is used to draw the lines
                    axs[j].hlines(y_divider1,x1-len,x1,linestyles='solid',colors='black',lw=0.85)
                    axs[j].hlines(y_divider2,x1-len,x1,linestyles='solid',colors='black',lw=0.85)
                    axs[j].hlines(mid_div,x1-len,x1,linestyles='dashdot',colors='black',lw=0.8)
                    axs[j].axis('off')
                    # annonater("",axs[j],y_divider1,y_divider2,x1-600)
                


                    d1,d2,d3=900,900,850
                    y_road1=y_divider1+d1
                    y_road2=y_divider2-d2
                    axs[j].hlines(y_road1,x1-len,x1,linestyles='solid',colors='black',lw=0.8)
                    axs[j].hlines(y_road2,x1-len,x1,linestyles='solid',colors='black',lw=0.8)

                    ##Drawing mid-road lines
                    axs[j].hlines(y_divider1+d1/2,x1-len,x1,linestyles='dashed',colors='#ADD8E6',lw=1)
                    axs[j].hlines(y_divider2-d2/2,x1-len,x1,linestyles='dashed',colors='#ADD8E6',lw=1)


                    print(df_filter)
                    offset=21

                    ##Get ofc line
                    axs[j].hlines(y_divider2-d2/2-d3,x1-len,x1,linestyles='dashed',colors='#0000FF',lw=2)
                    annonater(offset,axs[j],y_divider2-d2/2,y_divider2-d2/2-d3,x1-200)

                    d1,d2=400,620
                    y_roadside1=y_road1+d1
                    y_roadside2=y_road2-d2
                    axs[j].hlines( y_roadside1,x1-len,x1,linestyles='solid',colors='black',lw=1.5)
                    axs[j].hlines(y_roadside2,x1-len,x1,linestyles='solid',colors='black',lw=1.5)  

                    d=30
                    yl=y_roadside1+d
                    yr=y_roadside2-d
                    axs[j].hlines(yl,x1-len,x1,linestyles='solid',colors='white',lw=1.5)
                    axs[j].hlines(yr,x1-len,x1,linestyles='solid',colors='white',lw=1.5) 

                    d=150
                    for iter in df_filter.index:  
                        obs=df_filter['Observation Detail'][iter]
                        test="object is "+str(obs)
                        print(test)
                        if(test=='object is nan'):
                            continue
                        path1,zoom1 = get_path(obs)
                        img = mpimg.imread(path1)
                        xx = df['Chainage'][iter]+20
                        yy = y_roadside2-d-10
                        imagebox1 = OffsetImage(img,zoom1)
                        ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
                        axs[j].add_artist(ab1)

                    d=320
                    yr=y_roadside2-d
                    yr1=y_roadside2-d-290
                    for i in df_filter.index:
                        if (pd.isna(df_filter['Observation Detail'][i])) and pd.isna(df_filter['Crossing Type'][i]) :
                            axs[j].text(float(df_filter['Chainage'][i]),yr,float(df_filter['Chainage'][i]/1000),fontsize = 6,color='Black')
                        else:
                            axs[j].text(float(df_filter['Chainage'][i]),yr1,float(df_filter['Chainage'][i]/1000),fontsize = 6,color='Black')

                    bit=1
                    for iter in df_filter.index:  
                        crossing=df_filter['Crossing Type'][iter]
                        cross_len=df_filter['Crossing Length'][iter]
                        if(crossing=='ROAD CROSSING'):
                            bit=0
                        test= "crossing is "+str(crossing)
                        print(test)
                        if(test=='crossing is nan'):
                            print("into it")
                            continue
                        path1,zoom1,path2,zoom2 = get_crossing(crossing,cross_len)
                        print(path1,zoom1,path2,zoom2)
                        img1 = mpimg.imread(path1)
                        img2=mpimg.imread(path2)
                        xx1 = df['Chainage'][iter]+20
                        yy1 = y_roadside2-10
                        xx2 = df['Chainage'][iter]+20
                        yy2 = y_roadside2+d-10+2700
                        imagebox1 = OffsetImage(img1,zoom1)
                        imagebox2 = OffsetImage(img2,zoom2)
                        ab1 = AnnotationBbox(imagebox1, (xx1, yy1), frameon = False)
                        ab2 = AnnotationBbox(imagebox2, (xx2, yy2), frameon = False)
                        axs[j].add_artist(ab1)
                        if(bit==1):
                            axs[j].add_artist(ab2)
                location='static/images/line_'+ str(time.time())+'.png'
                plt.savefig(location)      
                    # print(levels)
    #  plt.show()
    #  plt.savefig('static/line.png')

    #  location='static/line_'+ str(time.time())+'.png'
    #  plt.savefig(location)
     img_dir = 'static/images' # replace with the path to your image directory
     image_list = os.listdir(img_dir)
     return render_template('display.html', image_list=image_list)
    #  return render_template("display.html",image_url=location)


@app.route('/download')
def download():
    # filename ='static/line.png'
    filename='static/final.pdf'
    return send_file(filename, as_attachment=True)
img_dir = 'static/images'    
for filename in os.listdir(img_dir):
        file_path = os.path.join(img_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    # return 'Folder has been emptied.'
if __name__ == '__main__':
   app.run(debug=True)