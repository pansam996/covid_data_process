import os
import numpy as np
import pandas as pd
import random
import math
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt

# read friendship
friendship_1 = np.array(pd.read_csv('./dataset_WWW2019/dataset_WWW_friendship_new.txt',header=None,sep='\t'))
friendship_2 = np.array(pd.read_csv('./dataset_WWW2019/dataset_WWW_friendship_old.txt',header=None,sep='\t'))
friendship_all = np.concatenate((friendship_1,friendship_2),axis = 0)

edge_list = []
for i in range(len(friendship_all)):
    edge_list.append([friendship_all[i][0], friendship_all[i][1]])

G = nx.Graph()
# add edge
for i in range(len(edge_list)):
    G.add_edge(edge_list[i][0],edge_list[i][1])


print('edge number :',G.number_of_edges(),'\nnode number :',G.number_of_nodes())


all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()

# Read the checkin data
path = './dataset_WWW2019/dataset_WWW_Checkins_anonymized.txt'

check_in_data = pd.read_csv(path,header=None,sep='\t')
all_id = check_in_data.iloc[:,0]
check_in_id = np.unique(np.array(all_id))
print('check in id number : ',check_in_id.shape)
np.amax(check_in_id)

# Read the position data
place_table = pd.read_csv('./dataset_WWW2019/raw_POIs.txt',header=None,sep='\t')
pid_table = place_table.iloc[:,0]

# Calculate user center
# init the dict
user_center = { i : (0,0) for i in all_node }

all_placeID = check_in_data.iloc[:,1]

for _id in check_in_id:
    if _id % 1000 == 0:
        print(_id)
    _data = all_placeID[all_id == _id]
    place = _data.iloc[0]
    _place_data = place_table[pid_table == place]
    x = round(_place_data.iloc[0,1], 3)
    y = round(_place_data.iloc[0,2], 3)
    user_center[_id] = (x,y)

# save the user center
with open('./user_center_2.txt' ,'w') as f:
    for i in all_node:
        f.write('{},{},{}\n'.format(i,user_center[i][0],user_center[i][1]))
f.close()