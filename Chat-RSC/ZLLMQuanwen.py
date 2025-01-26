# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:24:12 2024

@author: panxinpower
"""

import requests
import json
from ZCategoryLables import *;
from ZSamHelper import *;

def run_llm_content(mystring="",act=None):
    # 填入你的API Key
    api_key = 'XXXXXXXXXXXXXXXXXXXXXXX'
    # 填入正确的API Endpoint
    endpoint = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
    
    if mystring=="" :
        user_message = "This is not good enough, perform automatic selection;The Segment ID entered is [472, 513, 500, 100] mode is 1 "
    else:
        user_message=mystring;
    result = call_qwen_function(api_key, endpoint, user_message, functions)
    
    if result:
        # 检查是否有函数调用
        if 'function_call' in result['choices'][0]['message']:
            function_call = result['choices'][0]['message']['function_call']
            function_name = function_call['name']
            arguments = json.loads(function_call['arguments'])
            
            arguments['act']=act;
            
            print(arguments);
            thesh=None;
            
            if (act==None):
                resultstr="You haven't loaded or initialized the corresponding image.";
                if (function_name == 'action10'):
                    [resultstr,thesh]=action10(**arguments)
                
                if (function_name == 'action12'):
                    resultstr=action12(**arguments)
            else:
                pass;
                         
                if function_name == 'action1':
                    resultstr=action1(**arguments)
                elif function_name == 'action2':
                    resultstr=action2(**arguments)
                elif function_name == 'action3':
                    resultstr=action3(**arguments)
                elif function_name == 'action4':
                    resultstr=action4(**arguments)
                elif function_name == 'action5':
                    resultstr=action5(**arguments)
                elif function_name == 'action6':
                    resultstr=action6(**arguments)
                elif function_name == 'action7':
                    resultstr=action7(**arguments)
                elif function_name == 'action8':
                    resultstr=action8(**arguments)
                elif function_name == 'action9':
                    resultstr=action9(**arguments)
                elif function_name == 'action10':
                    [resultstr,thesh]=action10(**arguments)
                elif function_name == 'action11':
                    resultstr=action11(**arguments)
                elif function_name == 'action12':
                    resultstr=action12(**arguments)
                else:
                    resultstr="Your instruction is not clear. Please describe it more specifically."
            
        else:
            resultstr="Chat-RSC only accepts instructions related to remote sensing image classification. Please reorganize the relevant content."
            thesh=None;
    else:
        print("API调用失败")
    
    return [resultstr, thesh];
    

def call_qwen_function(api_key, endpoint, message, functions):
    """
    调用通义千问API并执行特定的功能。
    
    :param api_key: 你的API密钥
    :param endpoint: API的端点地址
    :param message: 用户输入的消息
    :param functions: 可供调用的函数列表
    :return: API响应的数据
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        'model': 'qwen-plus',
        "messages": [
            {"role": "user", "content": message}
        ],
        "functions": functions
    }
    
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    


# 定义10个函数
def action1(segments,act):
    # Manual selection
    print(f"Action1: Select the corresponding si in Sstate based on the point prompts, and add it to the selected set Select. Segments: {segments}")
    
    
    result=[];
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        act.Action1(result,0);
        
    except :
        print("Error");
    
    nums=len(result);
    rstr=f"{nums} objects are selected";
    
    print(rstr);
    
    return rstr;
    
    

def action2(segments,mode,act):
    # Automatic selection
    print(f"Action2: Automatically select items using the similar feature based on the point prompts, and add them to the selected set Select. Segments: {segments} {mode}")
    
    #act.Action2([471, 513, 500, 100],0);
    
    result=[];
    nums=0;
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        nums=act.Action2(result,selectmode=mode);
    except :
        print("Error");
    
    #nums=len(result);
    rstr=f"{nums} objects are selected";
    
    print(rstr);
    
    return rstr;
    

def action3(category,act):
    # Assigned category label
    print(f"Action3: Assign category labels to the selected set Select. Category: {category}");
    
    try:
        pass;
        categorylabel=CategoryLabels();
        label=categorylabel.getCategory(category);
        print(f"the lable is {label}")
       
        act.Action3(label);
    except :
        print("Error");
    return "Action performed";

def action4(segments,act):
    # Confirm category label
    print(f"Action4: Confirm all objects that have been assigned category labels. Segments: {segments}")
    
    try:
        pass;
        act.Action4();
    except :
        print("Error");
    return "Action performed";


def action5(segments,act):
    # Remove from selection set
    print(f"Action5: Removed from Select and set state to 1. Segments: {segments}")
 
    
    result=[];
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        
        act.Action5(result);
    except :
        print("Error");
    
    nums=len(result);
    rstr=f"{nums} objects are removed";
    
    print(rstr);
    
    return rstr;

def action6(segments,act):
    # Remove category label
    print(f"Action6: Remove the category labels and set state to 1. Segments: {segments}")
    
    result=[];
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        
        act.Action6(result);
    except :
        print("Error");
    
    nums=len(result);
    rstr=f"{nums} objects are removed category labels";
    
    print(rstr);
    
    return rstr;

def action7(segments,act):
    # Input split prompts
    print(f"Action7: The segment corresponding to si is under-segmented, input further split point prompts. Segments: {segments}")
    
    result=[];
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        
        act.Action7(result);
    except :
        print("Error");
    
    nums=len(result);
    rstr=f"{nums} segments are splited";
    
    print(rstr);
    
    return rstr;

def action8(segments,act):
    # Reinitialize child segments
    print(f"Action8: Further segment si, delete si from Sstate, and add the newly segmented items to Sstate. Segments: {segments}")
    
    result=[];
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        
        act.Action8(result);
    except :
        print("Error");
    
    nums=len(result);
    rstr=f"{nums} objects are inited";
    
    print(rstr);
    return rstr;

def action9(segments,act):
    # Unselecting
    print(f"Action9: Go back or roll back to the previous state. Segments: {segments}")
    
    result=[];
    try:
        pass;
        lst = eval(segments)
        result = [int(item) for item in lst]
        
        act.Action9(result);
    except :
        print("Error");
    
    nums=len(result);
    rstr=f"{nums} objects are go back to the previous state";
    
    print(rstr);
    return rstr;

def action10(filename,act):
    # Initializing the image's state machine
    print(f"Action10: Based on the Image initialize Sstate, the number of categories, and initial parameters (such as the color rendered for specific categories). filename: {filename}")

    sh=None;
    try:
        image_filename="K:\\sam\img\\"+filename;
        #image_filename=r"K:\sam\img\img30.bmp";
        print("-------------");
        print(image_filename);
        
        #image_filename=r"K:\sam\img\aa.jpg";
        sh=SamHelper();
        sh.loadImg(image_filename);
        sh.SegmentAll();
        sh.ClusterAll();
        
        
        #act.Action10(filename);
    except :
        print("Error");
    return ["Loading complete. You can try to control the classification results through conversation.",sh];
    
def action11(segments,act):
    # Input split prompts
    print(f"Action11: By using the input prompt, modify the state of S with Aclassify, and then output the state of S to the UI with Arender")
    
    #result=[];
    try:
        pass;
        #lst = eval(segments)
        #result = [int(item) for item in lst]
        
        #act.Action7(result);
    except :
        print("Error");
    
    #nums=len(result);
    #rstr=f"{nums} segments are splited";
    
    #print(rstr);
    
    return "AgentRender performed";    

def action12(segments,act):
    print(f"Action12:Reload previous data")
    return "RELOAD";
    
# 函数列表
functions = [
    {
        "name": "action1",
        "description": "Manual selection, Select the corresponding si in Sstate based on the point prompts, and add it to the selected set Select",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": []
        }
    },
    {
        "name": "action2",
        "description": "Automatic selection, Automatically select items using the similar feature based on the point prompts, and add them to the selected set Select;",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                },
                "mode": {
                   "type": "string",
                   "description": "If the user requests automatic selection by object, the value of mode is '1', and in all other cases, its value is '0'.",
                   "default": "0"
               }
            },
            "required": ["segments","mode"]
        }
    },
    {
        "name": "action3",
        "description": "Assigned category label, Assign category labels to the selected set Select",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "category label, lable, class label",
                    "default": "[]"
                }
            },
            "required": ["category"]
        }
    },
    {
        "name": "action4",
        "description": "Confirm category label, Change all si in Sstate from state 3 to state 4",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action5",
        "description": "Remove from selection set",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action6",
        "description": "Remove category label, Remove the class labels and set state to 1",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action7",
        "description": "Input split prompts, The segment corresponding to si is under-segmented, input further split point prompts",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action8",
        "description": "Reinitialize child segments, Further segment si, delete si from Sstate, and add the newly segmented items to Sstate",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action9",
        "description": "Unselecting, Go back to the previous state",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action10",
        "description": "Initializing the image's state machine, Load the image; Need input  image filename",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "filename string",
                    "default": "[]"
                }
            },
            "required": ["filename"]
        }
    },
    {
        "name": "action11",
        "description": "By using the input prompt, modify the state of S with Aclassify, and then output the state of S to the UI with Arender",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    },
    {
        "name": "action12",
        "description": "Reload previous data",
        "parameters": {
            "type": "object",
            "properties": {
                "segments": {
                    "type": "string",
                    "description": "Segments string",
                    "default": "[]"
                }
            },
            "required": ["segments"]
        }
    }
]

# 使用示例
if __name__ == "__main__":
    run_llm_content("");
   