import os
import numpy as np
import pandas as pd
import random
import math
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt


#############edit threshold ,day ,groups here#####################
threshold = 500
day = 10
groups = 10
##################################################################

#### Read the user_user_distance data
path = './user_user_distance_NYC.txt'

data = pd.read_csv(path,header=None,sep=',')

# column info
time = data[:][0] # timeslot
id_1 = data[:][1] # userid 1
id_2 = data[:][2] # userid 2
distance = data[:][3] # distance


#### add the match node and edge
match_nodes = []
edge_list = []

for i in range(len(data)):
    if distance[i] <= threshold:
        match_nodes.append(id_1[i])
        match_nodes.append(id_2[i])
        edge_list.append([id_1[i],id_2[i]])



G = nx.Graph()
# add node
for i in range(len(match_nodes)):
    G.add_node(match_nodes[i])

# add edge
for i in range(len(edge_list)):
    G.add_edge(edge_list[i][0],edge_list[i][1])

all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()


#### Read the checkin data
path = './dataset_TSMC2014_NYC.txt'

user_data = pd.read_csv(path,header=None,sep='\t',encoding='latin1')

#### column info
user_id = user_data[:][0]
user_x = user_data[:][4]
user_y = user_data[:][5]
check_in_id = np.unique(np.array(user_id))

print('check in id number : ',check_in_id.shape)

#### Calculate the user center
user_center = { u : (0,0) for u in all_node}

for i in check_in_id:
    x = sum(user_x[user_id == i]) / len(user_id[user_id == i])
    y = sum(user_y[user_id == i]) / len(user_id[user_id == i])
    if math.isnan(x) or math.isnan(y):
        user_center[i] = (0,0)
    else:
        user_center[i] = (x, y)

# save the user center
with open('./user_center_NYC.txt' ,'w') as f:
    for i in all_node:
        f.write('{},{},{}\n'.format(i,round(user_center[i][0],4),round(user_center[i][1],4)))
f.close()