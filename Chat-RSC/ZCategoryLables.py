# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:00:23 2025

@author: panxinpower
"""
import numpy as np;

class CategoryLabels:
    namelist=["building","car", "tree","vegetation", "road"];
    
    #颜色是 蓝 绿 红
    #0,建筑，蓝色, 1，汽车，黄色 2,树木,绿色， 3草地，淡蓝色
    classcolor1=np.array([[200,0,0,100],[0,255,255,100],[0,255,0,100],[255,255,0,100],[255,255,255,100]]);
    classcolor2=np.array([[255,0,0,255],[0,255,255,255],[0,255,0,255],[255,255,0,255],[255,255,255,255]]);
    
    def getCategory(self, thename):
        thevalue=0;
        
        for i in range(len(self.namelist)):
            if self.namelist[i] in thename.lower():
                thevalue=i;
                break;
        return  thevalue;
        