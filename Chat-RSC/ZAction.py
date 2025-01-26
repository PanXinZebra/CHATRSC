# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 07:57:17 2024

@author: panxinpower
"""

from ZStateMachineandAction import SegStateMachine
from ZSamHelper import SamHelper


class MyAction:
    sh : SamHelper;
    st : SegStateMachine;
    
    def __init__(self):
        pass;
        self.st=SegStateMachine();

    def Action1(self, keylist, theparameter):
        '''
        Run Manual selection
        theparameter==0 表示进行1-2状态的选取，不会把2刷为5
        theparameter==1 进行把2刷为5的操作 Automatic selection
        '''
        for ekey in keylist:
            if ekey in self.sh.m_fuse_masks.keys():
                row=self.sh.m_fuse_masks[ekey];
                self.st.performAction(1, theparameter, row);
                
        
    
    def Action2(self, keylist, theparameter=0, levelname='L1', selectmode=0):
        '''
        Run  Automatic selection
        
        levelname为近似类目的名字
        selectmode==0 使用KMeans
        selectmode==1 使用yolo
        
        '''
        nums=0;
        if (selectmode==0):
            pass;
            for ekey in keylist:
                row=self.sh.m_fuse_masks[ekey];
                value=row[levelname];
                for tempkey in self.sh.m_fuse_masks.keys():
                    if (tempkey in keylist):
                        continue;
                    trow=self.sh.m_fuse_masks[tempkey];
                    if (trow[levelname]==value):
                        self.st.performAction(2, theparameter, trow);
                        nums=nums+1;
        else:
           pass;
           for ekey in keylist:
               row=self.sh.m_fuse_masks[ekey];
               value=row['yolo'];
               for tempkey in self.sh.m_fuse_masks.keys():
                           
                   trow=self.sh.m_fuse_masks[tempkey];
                   if (trow['yolo']==value):
                       #print("select---%d"%(trow['id']));
                       self.st.performAction(2, theparameter, trow);
                       nums=nums+1;
        return nums;
                    
    
    def Action3(self, label=0):
        '''
        全部Select进行操作
        Assigned category label
        Perform Action 3
        '''
        keys=self.sh.m_fuse_masks.keys();
        for ekey in keys:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            self.st.performAction(3, label, erow);
            #self.st.performAct3(erow, label);
            
    def Action4(self):
        '''
        全部, 相当于数据库中的commit操作
        Confirm category label
        Perform Action 4
        '''
        keys=self.sh.m_fuse_masks.keys();
        for ekey in keys:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            self.st.performAction(4, 0, erow);
            #self.st.performAct4(erow);
            
    def Action5(self,keylist):
        '''
        Remove from selection set
        Perform Action 5
        '''
        '''
        #keys=self.sh.m_fuse_masks.keys();
        #for ekey in keys:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            self.st.performAction(5, 0, erow);
            #self.st.performAct4(erow);
        '''
        for ekey in keylist:
            erow=self.sh.m_fuse_masks[ekey];
            
            self.st.performAction(5, 0, erow);
            
            
            

    def Action6(self, keylist):
        '''
        全部, 相当于数据库中的commit操作
        Remove category label
        Perform Action 6
        '''
        keys=self.sh.m_fuse_masks.keys();
        for ekey in keylist:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            self.st.performAction(6, 0, erow);
            #self.st.performAct4(erow);

    def Action7(self,keylist):
        '''
        Input split prompts  需要重构
        '''
        keys=self.sh.m_fuse_masks.keys();
        for ekey in keylist:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            #self.st.performAction(7, 0, erow);
            
            #self.st.performAct4(erow);
            self.sh.splitFelzenszwalb(ekey);

    def Action8(self,  keylist):
        '''
        Reinitialize child segments  需要重构·
        '''
        keys=self.sh.m_fuse_masks.keys();
        for ekey in keylist:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            self.st.performAction(8, 0, erow);
            #self.st.performAct4(erow);
    
    def Action9(self,keylist): 
        '''
        Unselection  需要重构·
        '''
        keys=self.sh.m_fuse_masks.keys();
        for ekey in keylist:
            erow=self.sh.m_fuse_masks[ekey];
            #state=self.st.getState(erow);
            self.st.performAction(9, 0, erow);
            #self.st.performAct4(erow);
    
    def Action10(self,keylist): 
        print("Action 10");
     
                    
            
        
    
    
            
        
    