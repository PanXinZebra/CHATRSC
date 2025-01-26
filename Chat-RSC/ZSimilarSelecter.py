# -*- coding: utf-8 -*-
'''
Created on Tue Mar 19 07:47:10 2024

@author: panxinpower
'''

from ZSamHelper import SamHelper;


'''
这段代码不要了
'''

class StateMachine:
    '''
    每一个Segment的状态机
    
    Init    初始化
    TempSelect  暂时被选取
    
    '''
    
 
    def __init__(self):
        pass;
        
    def getInitState(self):
        return 'Init';
    
    def GetState(self, row):
        '''
        获取一个Row的状态
        '''
        if ('state' not in row.keys()):
            row['state']=self.getInitState();
            row['label']=-1;
        return row['state'];
    
    
    
    def CanChangeIntoSelect(self, row):
        '''
        对应状态是否可以转换为Select
        '''
        astate=self.GetState(row);
        if (astate=='Init'):
            return True;
        if (astate=='TempSelect'):
            return True;
        return False;
    def SetSelect(self, row):
        self.GetState(row);
        row['state']='TempSelect';
        
    def UnSetSelect(self, row):
        tstate=self.GetState(row);
        row['state']='Init';
    
    def isTempSelect(self,row):
        tstate=self.GetState(row);
        if (tstate=='TempSelect'):
            return True;
        return False;
        
        
        
    
        
        
        
    
    
    
class SimilarSelecter:
    
    sh:SamHelper;
    
    st:StateMachine;
    
    def __init__(self):
        self.st=StateMachine();
        
        
    def Select(self, theid, thename):
        row=self.sh.m_fuse_masks[theid];
        value=row[thename];
        
        idlist=[];
        for key in self.sh.m_fuse_masks.keys():
           
            trow=self.sh.m_fuse_masks[key];
            self.st.UnSetSelect(trow);
            if (not(value==trow[thename])):
                continue;
                
            if (self.st.CanChangeIntoSelect(trow)):
                pass;
                idlist.append(key);
                self.st.SetSelect(trow);
            print(key);
    
    
        
        
                
    
    
    
        
        
            
            
        
        