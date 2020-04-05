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
    
    

#-----------------------历史数据--------------------------------
    


# 1.历史数据--------------中国整体

# 数据地址
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'   # 定义要访问的地址
r = requests.get(url, headers=headers)  # 使用requests发起请求
    
# 读取为json    
data_json = json.loads(r.text)
data = data_json['data']

# 获取数据
timeseries_China = get_data(data['chinaDayList'],['date','lastUpdateTime'])
save_data(timeseries_China,'timeseries_China')
    

    
# 2.历史数据--------------中国各省
province_dict = {num:name for num,name in zip(today_province['id'],today_province['name'])}
    
for province_id in province_dict: # 遍历各省编号
    province_num1 = province_id
    break

count = 1
start = time.time()

for province_id in province_dict: # 遍历各省编号
    
    try:
        now = time.time()
        # 按照省编号访问每个省的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='+province_id
        r = requests.get(url, headers=headers)
        data_json = json.loads(r.text)
        
        # 提取各省数据，然后写入各省名称
        province_data = get_data(data_json['data']['list'],['date'])
        province_data['name'] = province_dict[province_id]
        
        # 合并数据
        if province_id == province_num1:
            timeseries_province = province_data
        else:
            timeseries_province = pd.concat([timeseries_province,province_data])
            
        print('---当前第'+str(count)+'个省---',
              province_dict[province_id],'成功',
            '---剩余'+str(len(province_dict)-count)+'个省---',
              province_data.shape,timeseries_province.shape,
             '---耗时:'+min_sec(now),
             ',累计：'+min_sec(start)+'---')
        count += 1
        
        # 设置延迟等待
        time.sleep(np.random.randint(5,20))
        
    except:
        print('-'*20,count,province_dict[province_id],'wrong','-'*20)
        count += 1
 
    
    
    
    
# 3.历史数据--------------世界各国
country_dict = {key:value for key,value in zip(today_world['id'], today_world['name'])}    
    
for country_id in country_dict: # 遍历各省编号
    country_num1 = country_id
    print(type(country_num1),country_num1,country_dict[country_num1])
    break


count = 1
start = time.time()
wrong_list = []

for country_id in country_dict: # 遍历每个国家的编号
    
    try:
        now = time.time()

        # 按照编号访问每个国家的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='+country_id
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)
        
        # 生成每个国家的数据
        country_data = get_data(json_data['data']['list'],['date'])
        country_data['name'] = country_dict[country_id]

        # 数据叠加
        if country_id == country_num1:
            timeseries_world = country_data
        else:
            timeseries_world = pd.concat([timeseries_world,country_data])
            
        print('---当前第'+str(count)+'个国家---',
              country_dict[country_id],'成功',
              '---剩余'+str(len(country_dict)-count)+'个国家---',
              country_data.shape,timeseries_world.shape,
              '---耗时:'+min_sec(now),          
              ',累计:'+min_sec(start)+'---')
        
        count += 1
        time.sleep(np.random.randint(1,20))

    except:
        print('-'*20,count,country_dict[country_id],'wrong','-'*20)
        count += 1
        wrong_list.append(country_id)  
        
        
if len(wrong_list) != 0:
    for country_id in wrong_list: # 遍历每个国家的编号
    
        # 按照编号访问每个国家的数据地址，并获取json数据
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='+country_id
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)

        # 生成每个国家的数据
        country_data = get_data(json_data['data']['list'],['date'])
        country_data['name'] = country_dict[country_id]
        timeseries_world = pd.concat([timeseries_world,country_data])
        print(country_dict[country_id])
