# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 01:48:02 2020

@author: Administrator
"""

import requests
import pandas as pd
import time 
import numpy as np
import json
pd.set_option('max_rows',500)


# 定义提取数据
def get_data(data,info_list):
    info = pd.DataFrame(data)[info_list] # 主要信息
    
    today_data = pd.DataFrame([i['today'] for i in data ]) # 生成today的数据
    today_data.columns = ['today_'+i for i in today_data.columns] # 修改列名
    
    total_data = pd.DataFrame([i['total'] for i in data ]) # 生成total的数据
    total_data.columns = ['total_'+i for i in total_data.columns] # 修改列名
    
    return pd.concat([info,total_data,today_data],axis=1) # info、today和total横向合并最终得到汇总的数据


# 定义保存数据方法
def save_data(data,name): 
    file_name = name+'_'+time.strftime('%Y_%m_%d',time.localtime(time.time()))+'.csv'
    data.to_csv(file_name,index=None,encoding='utf_8_sig')
    print(file_name+' 保存成功！')


# 描述爬虫时间进度
def min_sec(begin):
    dif = round(time.time()-begin)
    if dif//60 == 0:
        return str(dif)+'s'
    else:    
        return str(dif//60)+'min'+str(dif%60)+'s'
    
# 伪装头
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
    
    
# 当日数据地址
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'   # 定义要访问的地址
r = requests.get(url, headers=headers)  # 使用requests发起请求
    
# 读取为json    
data_json = json.loads(r.text)
data = data_json['data']
    
    
    
    
# 当日数据--------------中国各省
data_province = data['areaTree'][2]['children']  
    
today_province = get_data(data_province,['id','lastUpdateTime','name'])
    
save_data(today_province,'today_province')
    
    
# 当日数据--------------世界各国
areaTree = data['areaTree']  
    
today_world = get_data(areaTree,['id','lastUpdateTime','name'])

save_data(today_world,'today_world')  
    
    
