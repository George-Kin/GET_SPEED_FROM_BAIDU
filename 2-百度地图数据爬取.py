# -*- coding: utf-8 -*-
"""
Created on Thu May 18 17:57:04 2023

@author: jzh78
"""
import requests
import time
def pa(start_point,end_point):# 设置起点和终点的经纬度坐标,str

    # 服务地址
    host = "https://api.map.baidu.com"

    # 接口地址
    uri = "/directionlite/v1/driving"

    # 此处填写你在控制台-应用管理-创建应用后获取的AK
    ak = "ktsquUVb9OXCazn3QRyzhWWEh7Y6OzCK"

    params = {
        "origin":    "40.01116,116.339303",
        "destination":    "39.936404,116.452562",
        "ak":       ak,
        "coord_type": "wgs84"
            }

    response = requests.get(url = host + uri, params = params)

    # 解析API响应
    result = response.json()
    if result["status"] == 0:
        # 获取路段通行时间和通行距离
        route = result["result"]["routes"][0]
        duration = route["duration"]  # 路段总通行时间，单位：秒
        distance = route["distance"]  # 路段总通行距离，单位：米
        return duration,distance
    else:
        return "N/A" ,"N/A" 

#读取节点和边文件
import pandas as pd

node = pd.read_csv("CQ_map/node.csv",encoding='gbk') 
link = pd.read_csv("CQ_map/link.csv",encoding='gbk')
speed=pd.DataFrame()
speed['link_id']=link['link_id']
speed['speed']=''
for i in link['link_id']:
    s_n=link['from_node_id'][i]
    e_n=link['to_node_id'][i]
    s_n_x=node['x_coord'][s_n]
    s_n_y=node['y_coord'][s_n]
    e_n_x=node['x_coord'][e_n]
    e_n_y=node['y_coord'][e_n]
    start_point="{:.6f}".format(s_n_y)+','+"{:.6f}".format(s_n_x)
    end_point="{:.6f}".format(e_n_y)+','+"{:.6f}".format(e_n_x)
    dur,dis=pa(start_point,end_point)
    speed['speed'][i]=dis/dur
    if i%150==0:
        print(i)
        time.sleep(60)
        

speed.to_csv("CQ_map/speed_20.00.csv", index=False) 
    