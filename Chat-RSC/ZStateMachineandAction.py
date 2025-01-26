# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:43:35 2024

@author: panxinpower
"""
import numpy as np;


class SegStateMachine:
    '''
    分割的状态机
    状态包括以下内容：
    1. Initial state
    2. Selected state
    3. Specified category label state
    4. Confirmed label state
    5. Chosed from selected state
    6. Splited state
    7. Selected labeled segment state
    8. Selected confirmed segment state
    
    
    Actions
    1. Manual selection
    2. Automatic selection
    3. Assigned category label
    4. Confirm category label
    5. Remove from selection set
    6. Remove category label
    7. Input split prompts 
    8. Reinitialize child segments
    9. Unselection
    
    Action对应以下Action
    
    '''
    
    
    def __init__(self):
        pass;
        
    def getState(self, row):
        if ('state' not in row.keys()):
            row['state']=1;
            row['oldstate']=1;
            row['label']=-1;
            '''是否是当前正在选择的segment'''
            row['currentselect']=0;
        return row['state'];
    
    def getStateName(self, row):
        statenum=self.getState(row);
        resultstr=self.translateStateName(statenum);
        return resultstr;
    
    def translateStateName(self,statenum):
        '''
        将状态编号翻译为名字
        '''
        resultstr='';
        if (statenum==1):
            resultstr='Initial state';
        if (statenum==2):
            resultstr='Selected state';
        if (statenum==3):
            resultstr='Specified category label state';
        if (statenum==4):
            resultstr='Confirmed label state';
        if (statenum==5):
            resultstr='Chosed from selected state';
        if (statenum==6):
            resultstr='Splited state';
        if (statenum==7):
            resultstr='Selected labeled segment state';
        if (statenum==8):
            resultstr='Selected confirmed segment state';
        return resultstr;
    
    def performAction(self, theaction, theparameter, row):
        '''
        在Act1 的时候 theparameter=0 表示不进行选择集中的重选
                     theparameter=1 表示在选择集中进行重选，获得重选的集合。
        '''
        #print("Perform%d"%(theaction));
        pass;
        if (theaction==1):
            self.performAct1(row,theparameter);
        
        if (theaction==2):
            self.performAct2(row);
            
        if (theaction==3):
            self.performAct3(row,theparameter);
            
        if (theaction==4):
            self.performAct4(row);
            
        if (theaction==5):
            self.performAct5(row);
            
        if (theaction==6):
            self.performAct6(row);
            
        if (theaction==7):
            self.performAct7(row);
            
        if (theaction==8):
            self.performAct8(row);
        
        if (theaction==9):
            self.performAct9(row);
            
    
    def performAct1(self,row,theparameter):
        '''
        执行 Manual selection
        
        theparameter=1表示确定是在选择集中进行重选，否则相当于对于一个对象反复的点击选择
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        if (oldstate==1):
            newstate=2;
        
        
        if (oldstate==2 and theparameter==1):
            newstate=5;
            
            
        if (oldstate==3):
            newstate=7;
        if (oldstate==4):
            newstate=8;
            
        if (oldstate==newstate):
            return;
        row['state']=newstate;
        
        row['oldstate']=oldstate;
        
        '''用于Perform Unselection'''
        row['currentselect']=1;
        
    def performAct2(self,row):
        '''
        执行 Automatic selection
        进行大范围选取， 比Action1少两个状态转换
        '''
        
        oldstate=self.getState(row);
        newstate=oldstate;
        if (oldstate==1):
            newstate=2;
        
        #if (oldstate==2):
        #    newstate=5;
        
        if (oldstate==3):
            newstate=7;
            
        #if (oldstate==4):
        #    newstate=8;
            
        #if (oldstate==newstate):
        #    return;
        #print("set-state=%d"%(newstate));
        row['state']=newstate;
        row['oldstate']=oldstate;
        #print("state===%d"%(newstate));
        
        '''用于Perform Unselection'''
        row['currentselect']=1;
        
    def performAct3(self,row,theparameter):
        '''
        执行 Assigned category label
        需要类目标签
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        
        if (oldstate==2):
            newstate=3;
        
        if (oldstate==newstate):
            return;
        #print(row['id']);
            
        row['state']=newstate;
        row['label']=theparameter;
        print("%d---%d"%(row['id'],theparameter))
        row['oldstate']=oldstate;
        
    def performAct4(self,row):
        '''
        执行 Confirm category label
        需要类目标签
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        
        if (oldstate==3):
            newstate=4;
        
        if (oldstate==newstate):
            return;
            
        row['state']=newstate;
        row['oldstate']=oldstate; 
        
    def performAct5(self,row):
        '''
        执行 Remove from selection set
        需要类目标签
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        
        if (oldstate==2):
            newstate=1;
        
        if (oldstate==newstate):
            return;
            
        row['state']=newstate;
        row['oldstate']=oldstate; 
    
    def performAct6(self,row):
        '''
        执行 Remove category label
        
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        
        if (oldstate==7):
            newstate=1;
        if (oldstate==8):
            newstate=1;
        
        if (oldstate==newstate):
            return;
            
        row['state']=newstate;
        row['oldstate']=oldstate; 
    
    def performAct7(self,row):
        '''
        执行 Input split prompts
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        
        if (oldstate==5):
            newstate=6;
        if (oldstate==newstate):
            return;
            
        #sh.splitFelzenszwalb(1584);
        
        row['state']=newstate;
        row['oldstate']=oldstate; 
    
    def performAct8(self,row):
        '''
        执行 Input split prompts
        '''
        oldstate=self.getState(row);
        newstate=oldstate;
        
        if (oldstate==4):
            newstate=1;
        if (oldstate==newstate):
            return;
        print('rrrrrrrrrrrrrrrrr')
        row['state']=newstate;
        row['oldstate']=oldstate;         
            
    def performAct9(self,row):
        '''
        执行 Unselection
        '''
        if (row['currentselect']==1):
            row['state']=row['oldstate'];
            row['currentselect']=0;
    
    def clearCurrentselect(self,row):
        '''
        每次执行完一组操作，执行清空currentselect
        '''
        row['currentselect']=0;
            
        
if __name__ == "__main__":
    pass;
    