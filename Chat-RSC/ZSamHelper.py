# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 09:10:37 2024

@author: panxinpower
"""
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
from segment_anything import SamPredictor
import matplotlib.pyplot as plt
import numpy as np;
import cv2;
from sklearn.cluster import KMeans
from skimage.filters import sobel
from skimage.color import rgb2gray
from ultralyticsplus import YOLO, render_result


from skimage import io, color, segmentation

class SamHelper:
    '''
    p系列是系统内部的所有内容，或者不需要更改的内容。
    p_blockwidth，每个子块最大的大小
    p_model_type  SAM模型名
    p_model_path  SAM模型位置
    
    p_levels 使用Kmeans获得的结果的数量
    p_levelnum 使用使用Kmeans级别书
    
    p_selectresult  使用p_predictor预测适合会产生3个结果，它表示默认第几个结果
    '''
    p_blockwidth = 64*6;
    #p_blockwidth = 64*2;
    p_model_type = "vit_b";
    p_model_path="K:\\sam\\model\\sam_vit_b_01ec64.pth";
    p_device = "cuda";
    p_sam=[];
    p_is_gpu=True;
    p_mask_generator=[];
    p_mask_generator2=[];
    p_predictor=[];
    
    p_levels=[5,4];
    #p_levels=[5];
    p_levelnum=2;
    
    p_reselectnum=200;
    p_reselectsize=100;
    
    
    
    p_selectresult=0;
    
    
    '''
    
    '''
    image_filename=""
    p_yolomodel_path='K:\\sam\\yolovis\\best.pt';
    #yolo标签的图像
    p_yololabelimge=None;
    
    '''
    m系列参数是需要存盘的
    m_hss  图像有多少行
    m_lss  图像有多少列
    m_image  影像
    m_childimges 子影像块列表
    m_childpoints 子影像块起始点
    m_childwhs   子影像块大小；
    m_childnum    子影像块数量
    
    #m_childembd   embedding图列表，弃用
    m_embdimg  这个图是一个整个embedding图是一个整个的图
    
    m_dimension   embedding的维度
    
    m_fuse_index 融合后的结果数量
    m_fuse_masks 融合后的mask列表
    m_fuse_idimg 融合后ID构成的影像
    '''
    m_hss=0;
    m_lss=0;
    m_image : np.ndarray;
    
    m_childimges=[];
    m_childpoints=[];
    m_childwhs=[];
    m_childnum=0;
    
    #m_childembd=[];这个弃用了
    m_embdimg: np.ndarray;
    
    m_dimension=256;
    
    m_fuse_index=0;
    m_fuse_masks={};
    m_fuse_idimg : np.ndarray;
    
    m_defaultcluster=5;
    
    
    '''
    模型存盘
    k_kmeansmodel   kmeansmodel的个数。
    '''
    k_kmeansmodel=[];
    
    
    def __init__(self):
        
        self.p_sam = sam_model_registry[self.p_model_type](checkpoint=self.p_model_path)
        if (self.p_is_gpu):
            device = "cuda"
            self.p_sam.to(device=device)
        #self.p_mask_generator = SamAutomaticMaskGenerator(self.p_sam,
        #                                                  pred_iou_thresh=0.0);    
        
        #负责提供segment的sam
        self.p_mask_generator = SamAutomaticMaskGenerator(self.p_sam,
                                                  pred_iou_thresh=0.86,
                                                  stability_score_thresh=0.92,
                                                  crop_n_layers=1,
                                                  crop_n_points_downscale_factor=2,
                                                  min_mask_region_area=100
                                                  );    
        #负责提供vector的sam
        self.p_mask_generator2= SamAutomaticMaskGenerator(model=self.p_sam,
                                                          points_per_side=64,
                                                          );
   
        
        
        self.p_predictor = SamPredictor(self.p_sam);
        print("Sam loaded");

    def loadImg(self, image_filename):
        '''
        加载影像，并且划分为块。
        '''
        pass;
        self.image_filename=image_filename;
        image_array = cv2.cvtColor(cv2.imread(image_filename), cv2.COLOR_BGR2RGB);
        [self.m_hss,self.m_lss,bds]=np.shape(image_array);
        self.p_yololabelimge=np.zeros((self.m_hss,self.m_lss),dtype="int")-1;
        
        #低于30% blockwidth，那么就合并到前一个块
        mhn=int(self.m_hss/self.p_blockwidth+0.7);
        mln=int(self.m_lss/self.p_blockwidth+0.7);
        #至少有一块
        if (mhn==0):
            mhn=1;
        if (mln==0):
            mln=1;
        self.m_image=image_array;
        
        
        self.m_childimges=[];
        self.m_childpoints=[];
        self.m_childwhs=[];
        self.m_childnum=0;
        
        
        for ii in range(mhn):
            for jj in range(mln):
                starth=ii*self.p_blockwidth;
                hsize=self.p_blockwidth;
                startl=jj*self.p_blockwidth;
                lsize=self.p_blockwidth;
                if (ii==(mhn-1)):
                    hsize=self.m_hss-starth;
                if (jj==(mln-1)):
                    lsize=self.m_lss-startl;
                childimg=image_array[starth:starth+hsize,startl:startl+lsize,:];
        
                self.m_childimges.append(childimg);
                self.m_childpoints.append([starth,startl]);
                self.m_childwhs.append([hsize,lsize]);
        self.m_childnum=len(self.m_childwhs);
                

    
    
    def SegmentAll(self):
        
        self.m_childembd=[];
        
        self.m_fuse_index=0;
        self.m_fuse_masks={};
        
        self.EmbdAll();
        
        for ii in range(self.m_childnum):
            image_array=self.m_childimges[ii];
            my_masks = self.p_mask_generator.generate(image_array)      
            
            #self.p_predictor.set_image(image_array)
            #my_embeding_tensor=self.p_predictor.get_image_embedding();
            #my_embeding = my_embeding_tensor.cpu().numpy();
            
            #这里换成整体图
            
            fuse_startpos=self.m_childpoints[ii];
            
            #self.m_dimension=np.shape(my_embeding)[1];
            
            
            self.m_fuse_index=self.msk_buildfromsam(ii, self.m_fuse_index, fuse_startpos, self.m_fuse_masks, image_array, 0, my_masks)
            
            #self.m_childembd.append(my_embeding);
            
            self.ObtainFuseIdImage();
        
        
        #整体Embd
        
    def EmbdAll(self):
        '''
        有覆盖的一个个子图进行处理,获得更加无缝衔接的Embding
        '''
        
        
        '''''oklist=[];
        fklist=[];
        dklist=[];'''
        
        pass;
        self.m_embdimg=np.zeros((self.m_hss,self.m_lss,self.m_dimension),dtype="float32");
        
        blocksize=self.p_blockwidth;
        gap=int(self.p_blockwidth/4);
        if (gap%2!=0):
            gap=gap+1;
        gap=int(gap);
        #print("Gap=%d"%gap)
        
        starth=0;
        startl=0;
        
        while (starth<self.m_hss):
            startl=0;
            hw=0;
            while (startl<self.m_lss):
                ssh=starth
                ssl=startl
                hw=ssh+blocksize;
                lw=ssl+blocksize;
                
                if (hw>self.m_hss):
                    hw=self.m_hss;
                if (lw>self.m_lss):
                    lw=self.m_lss;
                
                ssh=int(ssh);
                hw=int(hw);
                ssl=int(ssl);
                lw=int(lw);
                #print("{%d,%d,%d,%d}"%(ssh,hw,ssl,lw));
                hnums=hw-ssh;
                lnums=lw-ssl;
                
                #print("剪切位置{%d->%d,%d->%d} hnums %d, lnums %d"%(ssh,hw,ssl,lw,hnums,lnums));
                
                
                
                
                childimg=self.m_image[ssh:hw,ssl:lw,:];
                
                
                
                #fklist.append(childimg);
                
                self.p_predictor.set_image(childimg)
                my_embeding_tensor=self.p_predictor.get_image_embedding();
                my_embeding = my_embeding_tensor.cpu().numpy();
                
                
                #print(np.shape(my_embeding));
                #重新缩放
                bigeembimage=[];
                #注意OpenCV 是列+行， 而不是行列
                #new_shape=[lw-ssl,hw-ssh]  这个new_shape没有用了。
                
                
                #embeding 是方形的，不是方的会填充颜色补充成方的
                if (hnums>lnums):
                    resize_shape=[hnums,hnums];
                else:
                    resize_shape=[lnums,lnums];
                
                #print("---回放大小%d,%d"%(hw-ssh,lw-ssl));
                
                #dklist.append(my_embeding[0,1,:,:]);
                
                for i in range(self.m_dimension):
                    a_img=my_embeding[0,i,:,:];
                    
                    b_img = cv2.resize(a_img, resize_shape)
                    
                    #把方形的进行剪切
                    b_img=b_img[0:hnums,0:lnums];
                    
                    
                    bigeembimage.append(b_img);
                my_embeding=np.stack(bigeembimage,2);
                #print(np.shape(my_embeding));
                
                #oklist.append(my_embeding[:,:,0]);
                
                
                copysh=gap/2;
                copysl=gap/2;
                copysh=int(copysh);
                copysl=int(copysl);
                
                if (ssh==0):
                    copysh=0;
                if (ssl==0):
                    copysl=0;
                
                copyeh=hnums;
                copyel=lnums;
                #print(np.shape(my_embeding));
                             
                #print("--复制起始点  H： %d %d; L：%d %d"%(copysh,copyeh,copysl,copyel));
                
                #print("--目标起始点 H： %d %d; L：%d %d"%(starth+copysh,starth+copyeh,startl+copysl,startl+copyel));
                
                
                self.m_embdimg[starth+copysh:starth+copyeh,startl+copysl:startl+copyel,:]=my_embeding[copysh:copyeh,copysl:copyel,:];
                
                
                if (lw>=self.m_lss):
                    break;
                
                startl=startl+blocksize-gap;
            
            
            if (hw>=self.m_hss):
                break;
            starth=starth+blocksize-gap;
            
            
        print("OK--");
        print(np.shape(self.m_embdimg));
            
        

        
        
        
    def AssignLable(self, row):
        '''
        给一行赋予标签值
        '''
        for ii in range(self.p_levelnum):
            thename="L%d"%ii;
            kmeans = self.k_kmeansmodel[ii];
            
            vector=row['embedding'];
            
            lablel=kmeans.predict(vector.reshape(1,-1));
            row[thename]=lablel[0];
            
       
        
            
    def ClusterAll(self,defaultcluster=5):
       
        self.k_kmeansmodel=[];
        
        self.m_defaultcluster=defaultcluster;
        
        snm=len(self.m_fuse_masks);
        trainx=np.zeros((snm,self.m_dimension),dtype='float32');

        keys=self.m_fuse_masks.keys();
        ii=0;
        #id有可能被删
        for xx in keys:
            row=self.m_fuse_masks[xx];
            trainx[ii,:]=row['embedding'];
            ii=ii+1;
            
        
        for ii in range(self.p_levelnum):
            thename="L%d"%ii;
            kmeans = KMeans(n_clusters=self.m_defaultcluster*self.p_levels[ii], random_state=0, n_init="auto").fit(trainx);
            labels=kmeans.labels_;
            
            keys=self.m_fuse_masks.keys();
            mm=0;
            for xx in keys:
                row=self.m_fuse_masks[xx];
                row[thename]=labels[mm];
                mm=mm+1;
            print("Success: "+thename);
            
            self.k_kmeansmodel.append(kmeans);
        
        #新添加Yolo选择    
        self.YoloAll(self.image_filename);
        
        '''
        kmeans = KMeans(n_clusters=p_clusternumber*3, random_state=0, n_init="auto").fit(trainx);
        labels=kmeans.labels_;
        '''    
    
            
    def ObtainFuseIdImage(self):
        '''建立ID图，方便定位'''
        self.m_fuse_idimg=np.zeros((self.m_hss,self.m_lss),dtype="int");
        keys=self.m_fuse_masks.keys();
        for xx in keys:
            row=self.m_fuse_masks[xx];
            aa=row['pth'];
            bb=row['ptl'];
            cid=row['id'];
            self.m_fuse_idimg[aa,bb]=cid;
            
    def ObtainKmeansImage(self, levelname='L3'):
        KmeansImage=np.zeros((self.m_hss,self.m_lss),dtype="int");
        keys=self.m_fuse_masks.keys();
        for xx in keys:
            row=self.m_fuse_masks[xx];
            aa=row['pth'];
            bb=row['ptl'];
            tid=row[levelname];
            KmeansImage[aa,bb]=tid;
        return KmeansImage;
        
    
    
    
    def msk_buildfromsam(self,source_img,fuse_index,fuse_startpos,fuse_masks,image_array,my_embeding,my_masks):
        '''
        id              id of mask
        bbox            外围框架, 附带分块偏移
        point_coords   中心点距离, 附带分块偏移
        points         总计的点数, 附带分块偏移
        pth            点的行, 总的图上
        ptl            点的列
        embedding      属性均值的均值
        oripth  原始的行 ，在子图上, 这个对应切块
        oriptl  原始的列
        sourceimg   原始的是第几个子图
        ''' 
        [nhss,nlss,nbds]=np.shape(image_array);
        #[v,nembnumber,nw,nh]=np.shape(my_embeding);
        nmasknumber=len(my_masks);
        
        #bigeembimage=[];
           
        #opencv 的格式是 YX的
        #new_shape=[nlss,nhss]
        
        '''
        for i in range(nembnumber):
            a_img=my_embeding[0,i,:,:];
            b_img = cv2.resize(a_img, new_shape)
            bigeembimage.append(b_img);
        
        bigemb=np.stack(bigeembimage);
        '''
        privateimg=np.zeros((nhss,nlss),dtype="int")-1;
        
        privatemsk=np.zeros((nhss,nlss),dtype="int")-1;
        
        for i in range(nmasknumber):
            aaa=my_masks[i]['segmentation'];
            aa2=np.where(aaa==True)
            privatemsk[aa2[0],aa2[1]]=i;
            
            
        
        for i in range(nmasknumber):
            
            aa2=np.where(privatemsk==i)
            if (len(aa2[0])==0):
                #print("Empty!");
                fuse_index=fuse_index+1;
                #因为前次实验，所以尽量保持两次实验的ID是一样的，即便是空的，自增1
                continue;
            
            row={};
            bbox=my_masks[i]['bbox'];
            point_coords=my_masks[i]['point_coords'][0];
            row['id']=fuse_index;
            cid=fuse_index;
            fuse_index=fuse_index+1;
            row['sourceimg']=source_img;
            row['bbox']=[bbox[0]+fuse_startpos[0],bbox[1]+fuse_startpos[1],bbox[2],bbox[3]];
            a1=point_coords[0]+fuse_startpos[0];
            a2=point_coords[1]+fuse_startpos[1];
            row['point_coords']=[a1,a2];
            row['points']=my_masks[i]['area'];
            
            ##需要重构这段代码 SAM直接输出的Mask有重重叠
            #aaa=my_masks[i]['segmentation'];
            #aa2=np.where(aaa==True)
            
            #row['pth']=aa2[0];
            #row['ptl']=aa2[1];
            #row['oripth']=np.copy(aa2[0]);
            #row['oriptl']=np.copy(aa2[1]);
            ##---------------------------------
            
            #重构之后的代码
            #aa2=np.where(privatemsk==i)
            row['pth']=aa2[0];
            row['ptl']=aa2[1];
            row['oripth']=np.copy(aa2[0]);
            row['oriptl']=np.copy(aa2[1]);
            #--------------------------------------------
            
            
            
            
            privateimg[aa2[0],aa2[1]]=cid;
            
            #映射到自己子图片块上, 有偏移位置
            row['pth']=row['pth']+fuse_startpos[0];
            row['ptl']=row['ptl']+fuse_startpos[1];
            #----------------------------------------------------------
            
            
            
            kkk=self.m_embdimg[row['pth'],row['ptl'],:];
            kkk2=np.average(kkk,0);
            row['embedding']=kkk2;
                      
            fuse_masks[cid]=row;
        #有背景，将背景改为一个ID
        
        aa2=np.where(privatemsk==-1)
        
        if (len(aa2[0])!=0):
            row={};
            row['id']=fuse_index;
            cid=fuse_index;
            fuse_index=fuse_index+1;
            row['sourceimg']=source_img;
            row['pth']=aa2[0];
            row['ptl']=aa2[1];
            row['oripth']=np.copy(aa2[0]);
            row['oriptl']=np.copy(aa2[1]);
            
            privateimg[aa2[0],aa2[1]]=cid;
            #映射到自己子图片块上, 有偏移位置
            row['pth']=row['pth']+fuse_startpos[0];
            row['ptl']=row['ptl']+fuse_startpos[1];
            
            kkk=self.m_embdimg[row['pth'],row['ptl'],:];
            kkk2=np.average(kkk,0);
            row['embedding']=kkk2;
            
            fuse_masks[cid]=row;
          
                                 
        return fuse_index;
    
    
    def resplit(self,theid):
        '''
        再更细的分一遍，效果不好
        '''
        row=self.m_fuse_masks[theid];
        source_img=row['sourceimg'];
        img=self.m_childimges[source_img];
        [hss,lss,bds]=np.shape(img);
        img2=np.zeros((hss,lss,bds),dtype='int');
        hhh=row['oripth'];
        lll=row['oriptl'];
        img2[hhh,lll,:]=1;
        img3=img*img2;
        img3=np.uint8(img3);
        
        
        
        #self.p_mask_generator2.min_mask_region_area=100;
        #self.p_mask_generator2.point_grids=self.randomSelectPoints(hhh,lll);
        
        my_masks = self.p_mask_generator2.generate(img3);
        
        fuse_startpos=self.m_childpoints[source_img];
        
        self.m_fuse_index=self.importMaskV2(img3,my_masks,hhh,lll,fuse_startpos,self.m_fuse_index,source_img,self.m_fuse_masks);
        
        self.m_fuse_masks.pop(theid);
        
        self.ObtainFuseIdImage();
    
    def resplit2(self,theid, pt1):
        '''
        以一个点为起点分一遍, pt1 为起始点
        '''
        row=self.m_fuse_masks[theid];
        source_img=row['sourceimg'];
        img=self.m_childimges[source_img];
        [hss,lss,bds]=np.shape(img);
        img2=np.zeros((hss,lss,bds),dtype='int');
        hhh=row['oripth'];
        lll=row['oriptl'];
        img2[hhh,lll,:]=1;
        img3=img*img2;
        img3=np.uint8(img3);
        
        
        
        #self.p_mask_generator2.min_mask_region_area=100;
        #self.p_mask_generator2.point_grids=self.randomSelectPoints(hhh,lll);
        
        input_point = np.array([pt1])
        input_label = np.array([1])
        self.p_predictor.set_image(img3);
        my_masks, scores, logits = self.p_predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
            )
        
        my_masks=my_masks[self.p_selectresult];
        aa2=np.where(my_masks==True);
        
        
        row={};
        row['id']=self.m_fuse_index;
        cid=self.m_fuse_index;
        
        row['sourceimg']=source_img;

        row['pth']=aa2[0];
        row['ptl']=aa2[1];
        row['oripth']=np.copy(aa2[0]);
        row['oriptl']=np.copy(aa2[1]);
        
        fuse_startpos=self.m_childpoints[source_img];
        
        row['pth']=row['pth']+fuse_startpos[0];
        row['ptl']=row['ptl']+fuse_startpos[1];
        
        kkk=self.m_embdimg[row['pth'],row['ptl'],:];
        kkk2=np.average(kkk,0);
        row['embedding']=kkk2;
        self.AssignLable(row);
        self.m_fuse_masks[self.m_fuse_index]=row;
        
        self.m_fuse_index=self.m_fuse_index+1;
        #print(aa2[0].shape);
        
        #把这个抠掉
        therow=self.m_fuse_masks[theid];
        imgx=np.zeros((hss,lss),dtype='uint');
        imgx[hhh,lll]=1;
        imgx[aa2[0],aa2[1]]=0
        aa2=np.where(imgx==1);
        
        if (aa2[0].shape[0]==0):
            self.m_fuse_masks.pop(theid);
            #print("Remove");
        else:
            therow['pth']=aa2[0];
            therow['ptl']=aa2[1];
            therow['oripth']=np.copy(aa2[0]);
            therow['oriptl']=np.copy(aa2[1]);
            therow['pth']=therow['pth']+fuse_startpos[0];
            therow['ptl']=therow['ptl']+fuse_startpos[1];
            kkk=self.m_embdimg[therow['pth'],therow['ptl'],:];
            kkk2=np.average(kkk,0);
            therow['embedding']=kkk2;
            self.AssignLable(therow);
            #print(aa2[0].shape);

        self.ObtainFuseIdImage();
        
    
        
    def resplit3(self,theid, pt1,pt2):
        '''
        以一个点为起点分一遍, pt1 为起始点
        '''
        row=self.m_fuse_masks[theid];
        source_img=row['sourceimg'];
        img=self.m_childimges[source_img];
        [hss,lss,bds]=np.shape(img);
        img2=np.zeros((hss,lss,bds),dtype='int');
        hhh=row['oripth'];
        lll=row['oriptl'];
        img2[hhh,lll,:]=1;
        img3=img*img2;
        img3=np.uint8(img3);
        
        
        
        #self.p_mask_generator2.min_mask_region_area=100;
        #self.p_mask_generator2.point_grids=self.randomSelectPoints(hhh,lll);
        
        input_point = np.array([pt1,pt2])
        input_label = np.array([1,0])
        
        self.p_predictor.set_image(img3);
        my_masks, scores, logits = self.p_predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
            )
        
        my_masks=my_masks[self.p_selectresult];
        aa2=np.where(my_masks==True);
        
        
        row={};
        row['id']=self.m_fuse_index;
        cid=self.m_fuse_index;
        
        row['sourceimg']=source_img;

        row['pth']=aa2[0];
        row['ptl']=aa2[1];
        row['oripth']=np.copy(aa2[0]);
        row['oriptl']=np.copy(aa2[1]);
        
        fuse_startpos=self.m_childpoints[source_img];
        
        row['pth']=row['pth']+fuse_startpos[0];
        row['ptl']=row['ptl']+fuse_startpos[1];
        
        kkk=self.m_embdimg[row['pth'],row['ptl'],:];
        kkk2=np.average(kkk,0);
        row['embedding']=kkk2;
        self.AssignLable(row);
        self.m_fuse_masks[self.m_fuse_index]=row;
        
        self.m_fuse_index=self.m_fuse_index+1;
        #print(aa2[0].shape);
        
        #把这个抠掉
        therow=self.m_fuse_masks[theid];
        imgx=np.zeros((hss,lss),dtype='uint');
        imgx[hhh,lll]=1;
        imgx[aa2[0],aa2[1]]=0
        aa2=np.where(imgx==1);
        
        if (aa2[0].shape[0]==0):
            self.m_fuse_masks.pop(theid);
            #print("Remove");
        else:
            therow['pth']=aa2[0];
            therow['ptl']=aa2[1];
            therow['oripth']=np.copy(aa2[0]);
            therow['oriptl']=np.copy(aa2[1]);
            therow['pth']=therow['pth']+fuse_startpos[0];
            therow['ptl']=therow['ptl']+fuse_startpos[1];
            kkk=self.m_embdimg[therow['pth'],therow['ptl'],:];
            kkk2=np.average(kkk,0);
            therow['embedding']=kkk2;
            self.AssignLable(therow);
            #print(aa2[0].shape);

        self.ObtainFuseIdImage();
      
    def resplit4(self,theid, ptlistlist):
        '''
        以一个点为起点分一遍, ptlistlist 为一个由多个List构成，每个list对应一个Lable
        尚未完全完成，ptlist1 和 ptlist2需要重新映射坐标；
        '''
        row=self.m_fuse_masks[theid];
        source_img=row['sourceimg'];
        img=self.m_childimges[source_img];
        
        
        [hss,lss,bds]=np.shape(img);
        
        
        img2=np.zeros((hss,lss),dtype='int');
        hhh=row['oripth'];
        lll=row['oriptl'];
        img2[hhh,lll]=1;
        
        
        maskimg=img2
        targetimg=img;
        
        
        #self.p_mask_generator2.min_mask_region_area=100;
        #self.p_mask_generator2.point_grids=self.randomSelectPoints(hhh,lll);
        
        theptlist=[];
        thelablelist=[];
        thelablevalue=1;
        
        for el in ptlistlist:
            for ep in el:
                
                theptlist.append(ep);
                thelablelist.append(thelablevalue);
            thelablevalue=0;
                
        '''
        for ep in ptlist1:
            theptlist.append(ep);
            thelablelist.append(1);
        for ep in ptlist2:
            theptlist.append(ep);
            thelablelist.append(0)
        '''
        
        
        input_point = np.array(theptlist);
        input_label = np.array(thelablelist);
        
        self.p_predictor.set_image(targetimg);
        my_masks, scores, logits = self.p_predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            #mask_input=maskimg,
            #multimask_output=True,
            multimask_output=False,
            )
        
        my_masks=my_masks[self.p_selectresult];
        my_masks=my_masks*img2;
        aa2=np.where(my_masks==1);
        
        
        row={};
        row['id']=self.m_fuse_index;
        cid=self.m_fuse_index;
        
        row['sourceimg']=source_img;

        row['pth']=aa2[0];
        row['ptl']=aa2[1];
        row['oripth']=np.copy(aa2[0]);
        row['oriptl']=np.copy(aa2[1]);
        
        fuse_startpos=self.m_childpoints[source_img];
        
        row['pth']=row['pth']+fuse_startpos[0];
        row['ptl']=row['ptl']+fuse_startpos[1];
        
        kkk=self.m_embdimg[row['pth'],row['ptl'],:];
        kkk2=np.average(kkk,0);
        row['embedding']=kkk2;
        self.AssignLable(row);
        self.m_fuse_masks[self.m_fuse_index]=row;
        
        self.m_fuse_index=self.m_fuse_index+1;
        #print(aa2[0].shape);
        
        #把这个抠掉
        therow=self.m_fuse_masks[theid];
        imgx=np.zeros((hss,lss),dtype='uint');
        imgx[hhh,lll]=1;
        imgx[aa2[0],aa2[1]]=0
        aa2=np.where(imgx==1);
        
        if (aa2[0].shape[0]==0):
            self.m_fuse_masks.pop(theid);
            #print("Remove");
        else:
            therow['pth']=aa2[0];
            therow['ptl']=aa2[1];
            therow['oripth']=np.copy(aa2[0]);
            therow['oriptl']=np.copy(aa2[1]);
            therow['pth']=therow['pth']+fuse_startpos[0];
            therow['ptl']=therow['ptl']+fuse_startpos[1];
            kkk=self.m_embdimg[therow['pth'],therow['ptl'],:];
            kkk2=np.average(kkk,0);
            therow['embedding']=kkk2;
            self.AssignLable(therow);
            #print(aa2[0].shape);

        self.ObtainFuseIdImage();
      
    
    def randomSelectPoints(self,hhh,lll):
        nnum=hhh.shape[0];
        
        if (self.p_reselectnum>nnum):
            x=2;
        else:
            x = self.p_reselectnum;
            
        n = nnum;
        #x = self.p_reselectnum;

        # 生成 1-n 的排列
        perm = np.random.permutation(n)
        
        # 取前 x 个元素
        random_nums = perm[:x]
        
        
        a1=hhh[random_nums];
        a2=lll[random_nums];
        
        points=[];
        
        for ii in range(x):
            pt=np.array([a2[ii],a1[ii]]);
            points.append(pt);
        
        return points;
                
        
    def splitSLIC(self,theid, labelnum=15, runidimage=True, thecompactness=20):
        #使用SLIC算法进行进一步划分, 在大图划分是需要指定的较大，而小图的时候指定为5就可以了，runidimage在整个图像构建阶段不需要运行ObtainFuseIdImage，所以选false
        #所以典型的调用方式是 大图背景 15，True，  小图切分 5，False
        

        row=self.m_fuse_masks[theid];
        source_img=row['sourceimg'];
        img=self.m_childimges[source_img];
        [hss,lss,bds]=np.shape(img);
        img2=np.zeros((hss,lss,bds),dtype='int');
        hhh=row['oripth'];
        lll=row['oriptl'];
        img2[hhh,lll,:]=1;
        img3=img*img2;
        img3=np.uint8(img3);
        
        
        
        mask = img2[:,:,0] > 0
        
        
        
        # 使用SLIC算法对参与计算的部分进行聚类
        segments_slic = segmentation.slic(img3,n_segments=labelnum, compactness=20, enforce_connectivity=True, sigma=100, mask=mask, start_label=1)
        
        # 将SLIC聚类结果可视化
        #segment_img = color.label2rgb(segments_slic, img3, kind='avg')
        

        
        # 可视化聚类效果
        '''
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(img3)
        plt.title('Original Image')
        
        plt.subplot(1, 2, 2)
        plt.imshow(segment_img)
        plt.title('SLIC Clustering Result')
        '''
        #my_masks = self.p_mask_generator2.generate(img3);sh
        
        fuse_startpos=self.m_childpoints[source_img];
        
        self.m_fuse_index=self.importMaskV3(img3,segments_slic,hhh,lll,fuse_startpos,self.m_fuse_index,source_img,self.m_fuse_masks);
        
        self.m_fuse_masks.pop(theid);
        
        if (runidimage):
            self.ObtainFuseIdImage();
    
    def splitFelzenszwalb(self,theid, labelnum=15, runidimage=True, thecompactness=20):
        #使用felzenszwalb算法进行进一步划分, 在大图划分是需要指定的较大，而小图的时候指定为5就可以了，runidimage在整个图像构建阶段不需要运行ObtainFuseIdImage，所以选false
        #所以典型的调用方式是 大图背景 15，True，  小图切分 5，False
        

        row=self.m_fuse_masks[theid];
        source_img=row['sourceimg'];
        img=self.m_childimges[source_img];
        [hss,lss,bds]=np.shape(img);
        img2=np.zeros((hss,lss,bds),dtype='int');
        hhh=row['oripth'];
        lll=row['oriptl'];
        img2[hhh,lll,:]=1;
        img3=img*img2;
        img3=np.uint8(img3);
        
        
        
        mask = img2[:,:,0] > 0
        
        
        gradient = sobel(rgb2gray(img3))
        #segments_watershed = watershed(gradient, markers=250, compactness=0.001)
        # 使用SLIC算法对参与计算的部分进行聚类
        segments_slic = segmentation.felzenszwalb(img3, scale=100, sigma=0.5, min_size=50)
        segments_slic=(segments_slic+1)*(mask+0);
        
        # 将SLIC聚类结果可视化
        #segment_img = color.label2rgb(segments_slic, img3, kind='avg')
        

        
        # 可视化聚类效果
        '''
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(img3)
        plt.title('Original Image')
        
        plt.subplot(1, 2, 2)
        plt.imshow(segment_img)
        plt.title('SLIC Clustering Result')
        '''
        #my_masks = self.p_mask_generator2.generate(img3);sh
        
        fuse_startpos=self.m_childpoints[source_img];
        
        self.m_fuse_index=self.importMaskV3(img3,segments_slic,hhh,lll,fuse_startpos,self.m_fuse_index,source_img,self.m_fuse_masks);
        
        self.m_fuse_masks.pop(theid);
        
        if (runidimage):
            self.ObtainFuseIdImage();


        
        
    
        
    def importMaskV2(self,image_array,my_masks,hhh,lll,fuse_startpos,fuse_index,source_img,fuse_masks):
        #从Sam结果里面导入
        [nhss,nlss,nbds]=np.shape(image_array);
        nmasknumber=len(my_masks);
        
        #背景是0
        privateimg=np.zeros((nhss,nlss),dtype="int");
        
        #把不需要部分至为负数
        negimg=np.zeros((nhss,nlss),dtype="int")-50000;
        negimg[hhh,lll]=0;
        
        idd=1;
        for i in range(nmasknumber):
            
            aaa=my_masks[i]['segmentation'];
            aa2=np.where(aaa==True)
            aa2[0]; #hhh
            aa2[1]; #lll
            privateimg[aa2[0],aa2[1]]=idd;
            idd=idd+1;
        
        privateimg=privateimg+negimg;
        
        lables=np.unique(privateimg);
        
        
        
        for label in lables:
            if (label<0):
                continue;
            
            row={};
            row['id']=fuse_index;
            cid=fuse_index;
            fuse_index=fuse_index+1;
            row['sourceimg']=source_img;
            
            aa2=np.where(privateimg==label)
            aa2[0]; #hhh
            aa2[1]; #lll
            
            row['pth']=aa2[0];
            row['ptl']=aa2[1];
            row['oripth']=np.copy(aa2[0]);
            row['oriptl']=np.copy(aa2[1]);
            
            
            
            row['pth']=row['pth']+fuse_startpos[0];
            row['ptl']=row['ptl']+fuse_startpos[1];
            
            kkk=self.m_embdimg[row['pth'],row['ptl'],:];
            kkk2=np.average(kkk,0);
            row['embedding']=kkk2;
            
            fuse_masks[cid]=row;
            print('Add %d--%d'%(fuse_index,len(aa2[0])));
        
        privateimg[hhh,lll]=0;
        
        self.mmimg=privateimg;
        
        
        return fuse_index;
    
    
    def importMaskV3(self,image_array,my_masks,hhh,lll,fuse_startpos,fuse_index,source_img,fuse_masks):
        #从SLIC的结果中导入    
        [nhss,nlss,nbds]=np.shape(image_array);
   
        lables=np.max(my_masks);
        privateimg=my_masks;
            
        for label in range(1,lables):
            
            aa2=np.where(privateimg==label)
            aa2[0]; #hhh
            aa2[1]; #lll
            
            if (len(aa2[0])==0):
                continue;
            
            row={};
            row['id']=fuse_index;
            cid=fuse_index;
            fuse_index=fuse_index+1;
            row['sourceimg']=source_img;
            
            
            
            row['pth']=aa2[0];
            row['ptl']=aa2[1];
            row['oripth']=np.copy(aa2[0]);
            row['oriptl']=np.copy(aa2[1]);
            
            
            
            row['pth']=row['pth']+fuse_startpos[0];
            row['ptl']=row['ptl']+fuse_startpos[1];
            
            kkk=self.m_embdimg[row['pth'],row['ptl'],:];
            kkk2=np.average(kkk,0);
            row['embedding']=kkk2;
            
            
            self.AssignLable(row);
                
            fuse_masks[cid]=row;
            #print('Add %d--%d'%(fuse_index,len(aa2[0])));
        
        privateimg[hhh,lll]=0;
        self.mmimg=privateimg;
        return fuse_index;
   
    def YoloAll(self,imagefile):
        #这个直接在ClusterAll后面调用了，使得前后代码一致
        print("perform Yolo");
        # load model
        yolomodel = YOLO(self.p_yolomodel_path);

        # set model parameters
        yolomodel.overrides['conf'] = 0.25  # NMS confidence threshold
        yolomodel.overrides['iou'] = 0.45  # NMS IoU threshold
        yolomodel.overrides['agnostic_nms'] = False  # NMS class-agnostic
        yolomodel.overrides['max_det'] = 1000  # maximum number of detections per image

       

        # perform inference
        results = yolomodel.predict(imagefile)
        print('start---1');
        boxes=results[0].boxes;
        aalist=[];
        for xyxy, conf, cls in zip(boxes.xyxy, boxes.conf, boxes.cls):
            bb=[];
            bb.append(xyxy.cpu().numpy())
            bb.append(conf.cpu().numpy())
            bb.append(cls.cpu().numpy());
            aalist.append(bb);
            
        for ecl in aalist:
            shh=np.uint32(ecl[0][1]);
            sl=np.uint32(ecl[0][0]);
            eh=np.uint32(ecl[0][3]);
            el=np.uint32(ecl[0][2]);
            lb=np.uint32(ecl[2].reshape(1)[0]);
            self.p_yololabelimge[shh:eh,sl:el]=lb;
        
        print('start---2');
        cc=self.p_yololabelimge;
        keys=self.m_fuse_masks.keys();
        for xx in keys:
            print('start---2N');
            row=self.m_fuse_masks[xx];
            aa=row['pth'];
            bb=row['ptl'];
            values=cc[aa,bb];
            uqt=np.unique(values,return_counts=True)
            uqv=-1;
            uqn=0;
            sums=0;
            for (vv,nn) in zip(uqt[0],uqt[1]):
                sums=sums+nn;
                if vv!=-1:
                    if nn>uqn:
                        uqn=nn;
                        uqv=vv;
            
            sums=uqn/sums;
            
            if (sums>0.5):
                print('An object');
                row['yolo']=uqv;
            else:
                row['yolo']=-1;
        
     

if __name__ == "__main__":
   
    image_filename=r"K:\sam\img\img30.bmp";
    sh=SamHelper();
    sh.loadImg(image_filename);
    sh.SegmentAll();
    sh.ClusterAll();
    #img=sh.ObtainKmeansImage('L1');
    '''
    bb=np.int32(sh.m_embdimg[:,:,0]*256);
    plt.imshow(bb)
    plt.show()'''
    
    
        