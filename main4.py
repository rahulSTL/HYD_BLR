from flask import Flask, render_template
from selenium import webdriver
from PIL import Image
from matplotlib import pyplot as plt 
import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


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
        print(object)

    if object=='PETROL PUMP':
        path = r"objects/petrols.png"
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
    return (path,zoom)    


df=pd.read_excel(r'NHAI FINAL SURVEY DATA.xlsx')
df= df.sort_values(by= "Chainage")
xmin=22000
xmax=535000
levels=(xmax-xmin)/3000
levels=1
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
                axs[0].text(float(df_filter['Chainage'][i]),yr,float(df_filter['Chainage'][i]/1000),fontsize = 6,color='Black')
            else:
                axs[0].text(float(df_filter['Chainage'][i]),yr1,float(df_filter['Chainage'][i]/1000),fontsize = 6,color='Black')




plt.show()

print(levels)