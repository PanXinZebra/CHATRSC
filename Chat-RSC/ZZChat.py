# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 09:29:09 2025

@author: panxinpower
"""

'''
实现交谈功能
'''
from ZSamHelper import SamHelper;
from ZAction import MyAction;
from ZRender import MyRender;
from ZLLMQuanwen import *;
import pickle


class Chatter:
    sh : SamHelper;
    act : MyAction;
    render : MyRender;
    
    
    def __init__(self):
        self.sh=None;
        self.act=None;
        self.render=None;
    
    
    def Chat(self, chatstring):
        [rs,thesh]=run_llm_content(chatstring,self.act);
        
        if thesh==None:
            pass;
        else:
            #初始化
            self.sh=thesh;
            self.act=MyAction();
            self.act.sh=thesh;
            self.render=MyRender();
            self.render.sh=thesh;
        
        print(rs);
        if (rs=="RELOAD"):
            self.load();
            rs="Reload previous data";
            print("-------------------------------------------------------");
            
        
        
        self.Rend();
        self.Save();
        return rs;

    def InitChat(self):
        pass;
    
    def Rend(self):
        if (self.render==None):
            return;
        self.render.SaveImage();
        self.render.saveSelectImage();  #没有select也需要显示
        self.render.saveClassificationImage();  #没有classfy结果也需要显示
        self.render.saveIDBorderImage(); #存储带边的image
        self.render.saveEmbdingImage(); #存储 Embedding和 带边的 Embedding img
    def Save(self):
        pass;
        if (self.sh==None):
            return;
        with open('K:\\sam\\renderresult\\my_instance.pickle', 'wb') as file:
            pickle.dump(self.sh, file)
            print('Save complete');
    def load(self):
        try:
            with open('K:\\sam\\renderresult\\my_instance.pickle', 'rb') as file:
                thesh = pickle.load(file)
            self.sh=thesh;
            self.act=MyAction();
            self.act.sh=thesh;
            self.render=MyRender();
            self.render.sh=thesh;
            print('Load complete');
        except:
            pass;
        

        

        


