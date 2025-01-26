# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 09:46:29 2024

@author: panxinpower
"""
from ZSamHelper import SamHelper;
from ZStateMachineandAction import SegStateMachine;
import numpy as np;
import cv2;
import json;
from skimage.segmentation import mark_boundaries
from skimage.io import *;
from skimage import exposure, io
from ZCategoryLables import *;

class MyRender:
    '''
    将所有结果刷到一个路径下
    好让显示器能显示出结果
    sh对应于 Samhelper
    savepath 对应于存储路径
    
    m_imgpath 主图像路径
    m_idpath  id图的路径
    m_ctpath 轮廓路径
    '''
    
    #选择的颜色
    #BGR颜色+不透明
    selectcolor=np.array([232,162,0,255]);
    
    #颜色是 蓝 绿 红
    #0,建筑，蓝色, 1，汽车，黄色 2,树木,绿色， 3草地，淡蓝色
    classcolor1=np.array([[200,0,0,100],[0,255,255,100],[0,255,0,100],[255,255,0,100],[255,255,255,100]]);
    classcolor2=np.array([[255,0,0,255],[0,255,255,255],[0,255,0,255],[255,255,0,255],[255,255,255,255]]);
    
    sh:SamHelper;
    st:SegStateMachine;
    
    m_savepath="K:\\sam\\renderresult\\";
    m_imgpath="";
    m_idpath="";
    m_ctpath="";
    m_selectimgpath="";
    m_classificationimgpath="";
    
    m_borderimgpath="";
    
    m_embdimgpath1="";
    m_embdimgpath2="";
    
    m_segments:dict();
    
    def __init__(self):
        pass;
        
        self.m_imgpath=self.m_savepath+"main.jpg";
        self.m_idpath=self.m_savepath+"id.text";
        self.m_ctpath=self.m_savepath+"ct.text";
        self.m_selectimgpath=self.m_savepath+"select.png";
        self.m_classificationimgpath=self.m_savepath+"class.png";
        
        self.m_borderimgpath=self.m_savepath+"border.jpg";
        
        self.m_embdimgpath1=self.m_savepath+"embd1.jpg";
        self.m_embdimgpath2=self.m_savepath+"embd2.jpg";
        
        self.st=SegStateMachine();
    
        categorylabel=CategoryLabels();
        self.classcolor1=categorylabel.classcolor1;
        self.classcolor2=categorylabel.classcolor2;
        

            
    def GetBorder(self):
        '''
        获取边的列表
        '''
        pass;
        self.m_segments=dict();
        '''
        id              id of mask
        bbox            外围框架, 附带分块偏移
        point_coords   中心点距离, 附带分块偏移
        points         总计的点数, 附带分块偏移
        pth            点的行, 总的图上
        ptl            点的列
        embedding      属性均值的均值
        oripth  原始的行 ，子图上
        oriptl  原始的列
        sourceimg   原始的是第几个子图
        ''' 
        for x in self.sh.m_fuse_masks.keys():
            pass;
            row=self.sh.m_fuse_masks[x];
            pth=row['pth'];
            ptl=row['ptl'];
            
            num=len(pth);
            tlist=[];
            for ii in range(num):
                tlist.append(ptl[ii]);
                tlist.append(pth[ii]);
            self.m_segments[row['id']]=tlist;
               
               
                
                
            
        
    
    def SaveImage(self):
        
        img_bgr = cv2.cvtColor(self.sh.m_image, cv2.COLOR_RGB2BGR)
        
        cv2.imwrite(self.m_imgpath, img_bgr);
        
        #np.save(self.m_idpath, self.sh.m_fuse_idimg);
        #with open( self.m_idpath, "w") as f:
        #    json.dump(self.sh.m_fuse_idimg.tolist(), f);
                
        
        oklist=[];
        [hss,lss]=np.shape(self.sh.m_fuse_idimg);
        oklist.append(str([hss,lss]));
        for ii in range(hss):
            aa= self.sh.m_fuse_idimg[ii,:];
            
            #这就话有问题，数据太长了记录不下来。
            #bb= str(aa).replace('\n',' ');
            bb=", ".join([str(x) for x in aa.tolist()])
            
            
            oklist.append(bb);
        okreal='\n'.join([str(x) for x in oklist]);
        with open(self.m_idpath, 'w') as f:
            f.write(okreal);
            
            
        #str(aa).replace('\n',' ')
        
        
        
        #----------------------------
        '''[hss,lss]=np.shape(self.sh.m_fuse_idimg);
        #str(aa).replace('\n',' ')
        
        labels=np.unique(self.sh.m_fuse_idimg);
        mysegments = {}
        for label in labels:
            mask = np.zeros(self.sh.m_fuse_idimg.shape[:2], dtype=np.uint8)
            mask[self.sh.m_fuse_idimg == label] = 255
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            ct=[];
            for x in contours:
                ptlist=[]
                #theptnum=len(x)
                for y in x:
                    ptlist.append(y[0][0]); #x
                    ptlist.append(y[0][1]); #y
                ct.append(ptlist);
            mysegments[label]=ct;    '''
        self.GetBorder();
        
        
        
        aa=self.m_segments;
        mylist=[];    
        for key in aa.keys():
            my_string = ' '.join([str(x) for x in aa[key]])
            my_string=str(key)+", "+my_string;
            mylist.append(my_string);
        
        realstring='\n'.join([str(x) for x in mylist]);
        
        with open(self.m_ctpath, 'w') as f:
            f.write(realstring);
    
    def saveSelectImage(self):
        pass;
        
        img=np.zeros((self.sh.m_hss,self.sh.m_lss,4),dtype="uint8");
        
        #BGR颜色+不透明
        color1=self.selectcolor;#np.array([108,177,250,255])
        for key in self.sh.m_fuse_masks.keys():
            row=self.sh.m_fuse_masks[key];
            if (self.st.getState(row)==2):
                #print(row['id']);
                hhh=row['pth'];
                lll=row['ptl'];
                
                img[hhh,lll,:]=color1
        
        #添加网纹
        #img[:,:,3]=0;
        #添加网纹
        img[0::4,:,3]=0;
        img[1::4,:,3]=0;
        
        
        #img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.m_selectimgpath, img);
    
    def saveClassificationImage(self):
        pass;
        
        img=np.zeros((self.sh.m_hss,self.sh.m_lss,4),dtype="uint8");
        
        #BGR颜色+不透明
        #color1=self.classcolor1;#np.array([108,177,250,255])
        #color2=self.classcolor2;#np.array([108,177,250,255])
        for key in self.sh.m_fuse_masks.keys():
            row=self.sh.m_fuse_masks[key];
            if (self.st.getState(row)==3):
                #print("-----------------------%d"%(row['id']));
                hhh=row['pth'];
                lll=row['ptl'];
                
                #print(row)
                if 'label' in row:
                    #print("-####$$-------------%d"%(row['id']));
                    mylbl=row['label'];
                    img[hhh,lll,:]=self.classcolor1[mylbl];
                    
                                   
            
            if (self.st.getState(row)==4):
                #print("-----------------------%d"+row['id']);
                hhh=row['pth'];
                lll=row['ptl'];
                
                if 'label' in row:
                    mylbl=row['label'];
                    img[hhh,lll,:]=self.classcolor2[mylbl];
        

        
        
        #img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(self.m_classificationimgpath, img);
        
    
    def saveIDBorderImage(self):
        #存储边界影像
        #self.m_borderimgpath
        img=self.sh.m_image;
        sid=self.sh.m_fuse_idimg;
        bdimg=mark_boundaries(img, sid);
        bdimg=np.uint8(bdimg*255);
        imsave(self.m_borderimgpath,bdimg);
            
    def saveEmbdingImage(self):
        #存储Embedding的Image，主要是为了写论文方便
        pass;
        
        kk=self.sh.m_embdimg[:,:,[0,1,2]];
        minx1=np.min(kk[:,:,0])
        minx2=np.min(kk[:,:,1])
        minx3=np.min(kk[:,:,2])
        maxx1=np.max(kk[:,:,0])
        maxx2=np.max(kk[:,:,1])
        maxx3=np.max(kk[:,:,2])

        kk[:,:,0]=(kk[:,:,0]-minx1)/(maxx1-minx1)*255;
        kk[:,:,1]=(kk[:,:,1]-minx2)/(maxx2-minx2)*255;
        kk[:,:,2]=(kk[:,:,2]-minx3)/(maxx3-minx3)*255;

        kk=np.uint8(kk);
        
        
        image=kk
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

        # 对每个通道应用直方图均衡化
        r_equalized = exposure.equalize_hist(r)
        g_equalized = exposure.equalize_hist(g)
        b_equalized = exposure.equalize_hist(b)

        # 合并均衡化后的通道
        equalized_image = np.stack((r_equalized, g_equalized, b_equalized), axis=-1)
        equalized_image= np.uint8(equalized_image*255);
        
        
        imsave(self.m_embdimgpath1,equalized_image);
        
        
        
        
        sid=self.sh.m_fuse_idimg;
        bdimg=mark_boundaries(equalized_image, sid);
        bdimg=np.uint8(bdimg*255);
        imsave(self.m_embdimgpath2,bdimg);
            
            

        


if __name__ == "__main__":
    pass;
    myrender=MyRender();
    myrender.sh=sh;
    myrender.SaveImage();
    #myrender.saveSelectImage();
    
    
    
    
    
    
    
    
    