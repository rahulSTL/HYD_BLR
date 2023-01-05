from flask import Flask, render_template
from selenium import webdriver
from PIL import Image
from matplotlib import pyplot as plt 
import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


app = Flask(__name__)

def annonater(lol,y1,y2,xl=2500):
        plt.annotate(
        '',xy=(xl, y1+650), xycoords='data',
        xytext=(xl, y2), textcoords='data',color='Red',
        arrowprops=dict(arrowstyle= '-',color='red'))
        plt.annotate(
        lol, xy=(xl+3, (y1+y2)/2), xycoords='data',color='Red',fontsize=7
        )

def get_df(x):
    df=pd.read_excel(r'NHAI FINAL SURVEY DATA.xlsx')
    df= df.sort_values(by= "Chainage")
    df = df.loc[df["Chainage"]<=x+1000]
    df = df.loc[df["Chainage"]>=x]
    #print(df)
    return df

def get_divider(d=300):
    global y_divider1,y_divider2,y
    y_divider1=y+d/2
    y_divider2=y-d/2
    mid_div=(y_divider1+y_divider2)/2
    plt.hlines(y_divider1,x,x+len,linestyles='solid',colors='black',lw=0.85)
    plt.hlines(y_divider2,x,x+len,linestyles='solid',colors='black',lw=0.85)
    plt.hlines(mid_div,x,x+len,linestyles='dashdot',colors='black',lw=0.8)
    #annonater(y_divider1,y_divider2,x+400)



def get_road(x,d1=900,d2=900,d3=850):
    df=get_df(x)
    for i in df.index:
        smthg = df['Executable Offset From RC'][i]
    # print(smthg)
    global y_road1,y_road2
    y_road1=y_divider1+d1
    y_road2=y_divider2-d2
    plt.hlines(y_road1,x,x+len,linestyles='solid',colors='black',lw=0.8)
    plt.hlines(y_road2,x,x+len,linestyles='solid',colors='black',lw=0.8)
    #annonater(y_road1,y_divider1,x+600)
    #annonater(y_road2,y_divider2,x+600)

    ##Drawing mid-road lines
    plt.hlines(y_divider1+d1/2,x,x+len,linestyles='dashed',colors='#ADD8E6',lw=1)
    plt.hlines(y_divider2-d2/2,x,x+len,linestyles='dashed',colors='#ADD8E6',lw=1)

    ##Get ofc line
    plt.hlines(y_divider2-d2/2-d3,x,x+len,linestyles='dashed',colors='#0000FF',lw=2)
    annonater(smthg,y_divider2-d2/2,y_divider2-d2/2-d3,x+200)



def get_roadside(d1=400,d2=620):
    global y_roadside1,y_roadside2
    y_roadside1=y_road1+d1
    y_roadside2=y_road2-d2
    plt.hlines( y_roadside1,x,x+len,linestyles='solid',colors='black',lw=1.5)
    plt.hlines(y_roadside2,x,x+len,linestyles='solid',colors='black',lw=1.5)
    #annonater(y_roadside1,y_road1,x+250)    
    #annonater(y_roadside2,y_road2,x+250)   

def outer_box(d=30):
    
    yl=y_roadside1+d
    yr=y_roadside2-d
    plt.hlines(yl,x,x+len,linestyles='solid',colors='white',lw=1.5)
    plt.hlines(yr,x,x+len,linestyles='solid',colors='white',lw=1.5)       

def get_objects_roadside(d,x):
    #yl=y_roadside1+d
    yr=y_roadside2-3*d
    df=get_df(x) 
    ax = plt.gca()
    #print(df.index)
    #print(df,len(df.index))
    for i in df.index: 
        if (pd.isna(df['Observation Detail'][i])) :
            pass
        elif df['Observation Detail'][i] == 'PETROL PUMP':
            path = r"petrols.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.6)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'TOLL PLAZA SAKAPUR (Telecom Room)' or df['Observation Detail'][i] == 'TOLL PLAZA AMAKATHADU (Telecom Room)' or df['Observation Detail'][i] == 'TOLL PLAZA KASEPALLI (Telecom Room)' or df['Observation Detail'][i] == 'TOLL PLAZA MARURU (Telecom Room)' or df['Observation Detail'][i] == 'TOLL PLAZA BAGEPALLI (Telecom Room)' or df['Observation Detail'][i] == 'TOLL PLAZA PHULLUR (Telecom Room)':
            path = r"toll plaza.png"
            path1 = r"hut.png"
            img = mpimg.imread(path)
            img1 = mpimg.imread(path1)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.08)
            imagebox2 = OffsetImage(img1,zoom=0.11)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ab2 = AnnotationBbox(imagebox2, (xx+40, yy), frameon = False)
            ax.add_artist(ab1)
            ax.add_artist(ab2)
        elif df['Observation Detail'][i] == 'BUILDING':
            path = r"build.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.045)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'TREE':
            path = r"tree.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.48)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'HOTEL':
            path = r"hotel.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.13)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'MARKET':
            path = r"market.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.065)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'FARM':
            path = r"Farms.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.145)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'FOREST':
            path = r"forest.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.2)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'HILL':
            path = r"hill.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.14)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'POND':
            path = r"pond.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.04)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'LAKE':
            path = r"pond.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.04)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'HARD ROCK & TREE':
            path = r"stone.png"
            path1 = r"tree.png"
            img = mpimg.imread(path)
            img1 = mpimg.imread(path1)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.05)
            imagebox2 = OffsetImage(img1,zoom=0.41)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ab2 = AnnotationBbox(imagebox2,(xx+30,yy),frameon=False)
            ax.add_artist(ab1)
            ax.add_artist(ab2)
        elif df['Observation Detail'][i] == 'AGRICULTURE LAND':
            path = r"land.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.04)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'WATER BODY':
            path = r"pond.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.04)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'KRISHNA RIVER':
            path = r"upper_krishna_river.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d+310
            imagebox1 = OffsetImage(img,zoom=0.13)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'TEMPLE':
            path = r"temple.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.04)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'Deep Excavation ':
            path = r"excavator.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d+30
            imagebox1 = OffsetImage(img,zoom=0.033)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'Service Road Under Construction':
            path = r"serviceroadconst.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.043)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'INDUSTRY':
            path = r"factory.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.025)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'Telecom Room':
            # print('hi')
            path = r"hutt.png"
            img = mpimg.imread(path)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d
            imagebox1 = OffsetImage(img,zoom=0.02)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ax.add_artist(ab1)
        elif df['Observation Detail'][i] == 'TOLL PLAZA RAIKAL (NOC)':
            path = r"toll plaza.png"
            path1 = r"noc.png"
            img = mpimg.imread(path)
            img1 = mpimg.imread(path1)
            xx = df['Chainage'][i]+20
            yy = y_roadside2-d-10
            imagebox1 = OffsetImage(img,zoom=0.08)
            # imagebox2 = OffsetImage(img1,zoom=0.11)
            imagebox2 = OffsetImage(img1,zoom=0.09)
            ab1 = AnnotationBbox(imagebox1, (xx, yy), frameon = False)
            ab2 = AnnotationBbox(imagebox2, (xx+40, yy), frameon = False)
            ax.add_artist(ab1)
            ax.add_artist(ab2)
  
def get_chainage(d,x):
    df=get_df(x)
    yr=y_roadside2-d
    yr1=y_roadside2-d-290

    for i in df.index:
        if (pd.isna(df['Observation Detail'][i])) and pd.isna(df['Crossing Type'][i]) :
            plt.text(float(df['Chainage'][i]),yr,float(df['Chainage'][i]/1000),fontsize = 6,color='Black')
        else:
            plt.text(float(df['Chainage'][i]),yr1,float(df['Chainage'][i]/1000),fontsize = 6,color='Black')

def get_culvert(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="CULVERT" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'Culvert.png'), zoom = 0.15)
            i1=OffsetImage(mpimg.imread(r'culvert_part.png'), zoom = 0.09)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1+150), frameon = False)
            a1=AnnotationBbox(i1, (tx1, ty1-170), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'Culvert2.png'), zoom = 0.15)
            i2=OffsetImage(mpimg.imread(r'culvert_part2.png'), zoom = 0.09)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-105), frameon = False)
            # a2=AnnotationBbox(i2, (tx2, ty2+170), frameon = False)
            a2=AnnotationBbox(i2, (tx2, ty2+420), frameon = False)
            plt.text(tx2+13, ty2-360,"Culvert\nL=",fontsize=5)
            plt.text(tx2+23, ty2-400,df['Crossing Length'][i],fontsize=6)
            ax.add_artist(ab1)
            ax.add_artist(a1)
            ax.add_artist(ab2)
            ax.add_artist(a2)
            
def get_bridge(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="BRIDGE" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2
            
            # plt.text(tx2, ty2-500,"Bridge\nL=",fontsize=5)
            # plt.text(tx2+50, ty2-450,df['Crossing Length'][i],fontsize=6)
            imagebox1 = OffsetImage(mpimg.imread(r'bridge_up_new.png'), zoom = 0.15)
            i1=OffsetImage(mpimg.imread(r'Bridge_upper_part.png'), zoom = 0.09)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1+100), frameon = False)
            a1=AnnotationBbox(i1, (tx1, ty1-250), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'bridge_down_new.png'), zoom = 0.15)
            i2=OffsetImage(mpimg.imread(r'Bridge_upper_part2.png'), zoom = 0.09)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-150), frameon = False)
            # ab2 = AnnotationBbox(imagebox2, (tx2, ty2-50), frameon = False)
            # a2=AnnotationBbox(i2, (tx2, ty2+200), frameon = False)
            a2=AnnotationBbox(i2, (tx2, ty2+480), frameon = False)
            ax.add_artist(ab1)
            ax.add_artist(a1)
            ax.add_artist(ab2)
            plt.text(tx2-12, ty2-350,"Bridge\nL=",fontsize=5)
            plt.text(tx2-2, ty2-350,df['Crossing Length'][i],fontsize=6)
            ax.add_artist(a2)

def get_canal(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="CANAL CROSSING" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'canals.png'), zoom = 0.05)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1-150), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'canals.png'), zoom = 0.05)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-100), frameon = False)
            plt.text(tx2+18, ty2-450,"Canal\nL=",fontsize=5)
            plt.text(tx2+30, ty2-450,df['Crossing Length'][i],fontsize=6)
            ax.add_artist(ab1)
            ax.add_artist(ab2)

def get_road_crossing(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="ROAD CROSSING" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'road_crossing.png'), zoom = 0.07)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1-150), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'road_crossing.png'), zoom = 0.07)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-100), frameon = False)
            plt.text(tx2+18, ty2-450,"road\nL=",fontsize=5)
            plt.text(tx2+30, ty2-450,df['Crossing Length'][i],fontsize=6)
            #ax.add_artist(ab1)
            ax.add_artist(ab2)

def get_river_crossing(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="RIVER CROSSING" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'river_crossing.png'), zoom = 0.05)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1-200), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'river_crossing.png'), zoom = 0.05)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-180), frameon = False)
            plt.text(tx2+18, ty2-450,"river\nL=",fontsize=5)
            plt.text(tx2+30, ty2-450,df['Crossing Length'][i],fontsize=6)
            ax.add_artist(ab1)
            ax.add_artist(ab2)

def get_under_pass(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="UNDER PASS" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'under.png'), zoom = 0.04)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1-200), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'under.png'), zoom = 0.04)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-180), frameon = False)
            plt.text(tx2+18, ty2-450,"underpass\nL=",fontsize=5)
            plt.text(tx2+30, ty2-450,df['Crossing Length'][i],fontsize=6)
            ax.add_artist(ab1)
            ax.add_artist(ab2)

def get_water_pipe(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="WATER PIPE LINE" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'water_crossing.png'), zoom = 0.11)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1-200), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'eay.png'), zoom = 0.035)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-180), frameon = False)
            #ax.add_artist(ab1)
            ax.add_artist(ab2)

def get_rail_crossing(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Crossing Type'][i]=="RAIL CROSSING" and df['Crossing Length'][i]>0:
            tx1, ty1 = df['Chainage'][i]+20,y_roadside1
            tx2, ty2 = df['Chainage'][i]+20,y_roadside2

            imagebox1 = OffsetImage(mpimg.imread(r'rail.png'), zoom = 0.4)
            ab1 = AnnotationBbox(imagebox1, (tx1, ty1-200), frameon = False)

            imagebox2 = OffsetImage(mpimg.imread(r'rail.png'), zoom = 0.4)
            ab2 = AnnotationBbox(imagebox2, (tx2, ty2-180), frameon = False)
            plt.text(tx2+18, ty2-450,"rail crossing\nL=",fontsize=5)
            plt.text(tx2+30, ty2-450,df['Crossing Length'][i],fontsize=6)
            ax.add_artist(ab1)
            ax.add_artist(ab2)
            

def get_serviceroad(x):
    df=get_df(x)
    ax = plt.gca()
    for i in df.index:
        if df['Service Road Name'][i]=="Yes":
            tx1, ty1 = df['Chainage'][i]+20,y_road1
            tx2, ty2 = df['Chainage'][i]+20,y_road2

            if df['Service Road Side'][i]=="LHS":
                imagebox1 = OffsetImage(mpimg.imread(r'Culvert.png'), zoom = 0.15)
                ab1 = AnnotationBbox(imagebox1, (tx1, ty1+200), frameon = False)
                plt.text(tx1+20, ty1+120,"Service Road\nw=",fontsize=5)
                ax.add_artist(ab1)

            if df['Service Road Side'][i]=="RHS":
                imagebox2 = OffsetImage(mpimg.imread(r'Culvert2.png'), zoom = 0.15)
                #i2=OffsetImage(mpimg.imread(r'culvert_part2.png'), zoom = 0.15)
                ab2 = AnnotationBbox(imagebox2, (tx2, ty2-220), frameon = False)
                #a2=AnnotationBbox(i2, (tx2, ty2+170), frameon = False)
                plt.text(tx2+20, ty2-180,"Service Road\nw=",fontsize=5)
                ax.add_artist(ab2)

def coords(x=1980,y=3100):
        global len
        plt.text(x, y, 'N: XXX-XXX-XXX', fontsize = 9)
        plt.text(x, y-130, 'E: XXX-XXX-XXX', fontsize = 9)
        plt.text(x+len-5,y, 'N: XXX-XXX-XXX', fontsize = 9)
        plt.text(x+len-5, y-130, 'E: XXX-XXX-XXX', fontsize = 9)                        
            
def get_fixed_things(x):
    #plt.text(x+860,650,"To Mansar>>",fontsize=9,color='Blue' ,weight='bold')
    #plt.text(x,-550,"<< To Kurai",fontsize=9,color='Blue',weight='bold')
    plt.text(x+250,-550,"<< NH-44 >>",fontsize=7,color='green')
    plt.text(x+800,-550,"<< NH-44 >>",fontsize=7,color='green')
    plt.text(x+750,300,"<< NH-44 >>",fontsize=7,color='green')
    plt.text(x+200,300,"<< NH-44 >>",fontsize=7,color='green')
    #plt.text(x+500,650,"BT Road",fontsize=6,color='Green')
    plt.text(x+500,-100,"<<Divider>>",fontsize=6,color='Black')
    #plt.text(x+700,-550,"BT Road",fontsize=7,color='Green')
    #plt.text(x+350,1100,"Gravel",fontsize=6,color='Green')
    #plt.text(x+500,1100,"Gravel",fontsize=6,color='Green')
    #plt.text(x+900,-1300,"Gravel",fontsize=6,color='Green')
    #plt.text(x+500,-1300,"Gravel",fontsize=6,color='Green')          



def get_soil(d,x):
    df=get_df(x)
    for i in df.index:
        plt.text(float(df['Chainage'][i]),y_roadside2-d,df['Strata Type'][i],fontsize = 5,color='Black')

global y_divider1,y_divider2,y_road1,y_road2,y_roadside1,y_roadside2,x,len,y,ok,d
# y,x,len=0,375000,1000
y,x,len=0,202000,1000
d=0

while x < 534720:
    fig=plt.figure(figsize=(350,153))  
    ax = plt.gca()
    ax.set_xlim(x-190, x+len+190)
    plt.subplot(311)
    #plt.plot(x,y)
    plt.axis('off')
    get_divider()
    get_road(x,900,900,850)
    get_roadside()
    outer_box()
    get_objects_roadside(150,x)
    get_chainage(320,x)
    get_culvert(x)
    get_bridge(x)
    get_canal(x)
    get_road_crossing(x)
    get_river_crossing(x)
    get_under_pass(x)
    get_water_pipe(x)
    get_rail_crossing(x)
    get_fixed_things(x)
    #---------------------
    x = x+1000
    plt.subplot(312)
    #plt.plot(x,y)
    plt.axis('off')
    get_divider()
    get_road(x,900,900,850)
    get_roadside()
    outer_box()
    get_objects_roadside(150,x)
    get_chainage(320,x)
    get_culvert(x)
    get_bridge(x)
    get_canal(x)
    get_road_crossing(x)
    get_river_crossing(x)
    get_under_pass(x)
    get_water_pipe(x)
    get_rail_crossing(x)
    get_fixed_things(x)
    #-----
    x = x+1000
    plt.subplot(313)
    #plt.plot(x,y)
    get_divider()
    get_road(x,900,900,850)
    get_roadside()
    outer_box()
    get_objects_roadside(150,x)
    get_chainage(320,x)
    get_culvert(x)
    get_bridge(x)
    get_canal(x)
    get_road_crossing(x)
    get_river_crossing(x)
    get_under_pass(x)
    get_water_pipe(x)
    get_rail_crossing(x)
    get_fixed_things(x)
    x=x+1000
    fig1 = plt.gcf()
    #plt.draw()
    plt.axis('off')
    # mng = plt.get_current_fig_manager()
    # mng.full_screen_toggle()
    # plt.get_current_fig_manager().window.state('zoomed')
    # figManager = plt.get_current_fig_manager()
    # figManager.window.showMaximized()
    plt.show()
    name_fig="images_sld1/sld"+str(int((x-3000)/1000))
    fig1.savefig(name_fig, dpi=600)




















