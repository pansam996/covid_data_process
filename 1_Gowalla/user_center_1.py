import os
import numpy as np
import pandas as pd
import random
import math
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt


#### read the edge data
edge_list = []
edge_data = pd.read_csv('./gowalla/gowalla_friendship.csv',sep=',')


for i in range(len(edge_data)):
    edge_list.append([edge_data.iloc[i,0], edge_data.iloc[i,1]])


G = nx.Graph()
# add edge
for i in range(len(edge_list)):
    G.add_edge(edge_list[i][0],edge_list[i][1])

all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()


#### Read the check in data
path = './original/gowalla_checkins_chron.csv'

check_in_data = pd.read_csv(path,sep=',')
all_id = check_in_data.iloc[:,0]
check_in_id = np.unique(np.array(all_id))
print('check in id number : ',check_in_id.shape)

#### Read the spot
place_table = pd.read_csv('./gowalla/gowalla_spots_subset1.csv',sep=',')
pid_table = place_table.iloc[:,0]

#### Calculate the user center
'''
Notice : this task will spend "a day" to finish
'''
## init the dict
user_center = { i : (0,0) for i in all_node }

all_placeID = check_in_data.iloc[:,1]

for _id in check_in_id:
    if _id % 100 == 0:
        print(_id)
    data_len = len(all_placeID[all_id == _id])
    if data_len >= 3:
        x = 0
        y = 0
        for idx in [1,int(data_len/2),-1]:
            place = all_placeID[all_id == _id].iloc[idx]
            x += place_table[pid_table == place].iloc[0,3]
            y += place_table[pid_table == place].iloc[0,2]
        x = round(x / 3, 3)
        y = round(y / 3, 3)
        user_center[_id] = (x,y)
    else:
        place = all_placeID[all_id == _id].iloc[0]
        x = round(place_table[pid_table == place].iloc[0,3], 3)
        y = round(place_table[pid_table == place].iloc[0,2], 3)
        user_center[_id] = (x,y)

# save the user center
with open('./user_center_1.txt' ,'w') as f:
    for i in all_node:
        f.write('{},{},{}\n'.format(i,round(user_center[i][0],4),round(user_center[i][1],4)))
f.close()