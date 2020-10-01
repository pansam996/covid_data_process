import os
import numpy as np
import pandas as pd
import random
import math
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt
def haversine(lon1, lat1, lon2, lat2): # 經度1，緯度1，經度2，緯度2 （十進制）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 將十進制轉為弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半徑，單位為公里
    return c * r * 1000

#### Read the data
nyc_data = pd.read_csv('./dataset_TSMC2014_TKY.txt',header=None,sep='\t',encoding='latin1')

# column info
all_user = nyc_data[:][0]
user_x = nyc_data[:][4]
user_y = nyc_data[:][5]

# process the unique date
all_time = nyc_data[:][7]
all_time = all_time.str[4:10]
unique_date = np.unique(np.array(all_time))
print('total date : ', unique_date.shape[0])
unique_date = sorted(unique_date, key=lambda day: datetime.strptime(day, "%b %d"))
unique_date = unique_date[42:] + unique_date[:42]

# process the unique user
unique_user = np.unique(np.array(all_user))
print('TKY user number : ',unique_user.shape)

#### Calculate the user_user distance
'''
Notice : this task will spend "a day" to finish
'''
with open('./user_user_distance_TKY.txt','w') as f:
    for idx in range(len(unique_date)) :
        print('='*10,idx,'='*10)
        select_date_datas = nyc_data [all_time == unique_date[idx] ]
        index_table = list(select_date_datas[0])
        select_date_id = np.unique(np.array(select_date_datas[0]))
        select_date_id = sorted(select_date_id)
        ## calculate user1 and user2 distance in select date
        for user1 in select_date_id:
            user1_index = index_table.index(user1)
            user1_x = select_date_datas.iloc[user1_index][4]
            user1_y = select_date_datas.iloc[user1_index][5]
            for user2 in select_date_id:
                if user1 >= user2:
                    continue
                # calculate distance
                else:
                    user2_index = index_table.index(user2)
                    user2_x = select_date_datas.iloc[user2_index][4]
                    user2_y = select_date_datas.iloc[user2_index][5]
                    d = int(haversine(user1_x, user1_y, user2_x, user2_y))
                    if d <= 1000:
                        f.write('{},{},{},{}\n'.format(idx, user1, user2, d))
f.close()