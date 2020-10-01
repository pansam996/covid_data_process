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
edge_data = pd.read_csv('./Brightkite_edges.txt',header=None,sep='\t')


for i in range(len(edge_data)):
    edge_list.append([edge_data[0][i], edge_data[1][i]])


G = nx.Graph()
# add edge
for i in range(len(edge_list)):
    G.add_edge(edge_list[i][0],edge_list[i][1])

all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()

#### Read the check in data
path = './Brightkite_totalCheckins.txt'

user_data = pd.read_csv(path,header=None,sep='\t')

# Colimn info
user_id = user_data[:][0]
user_x = user_data[:][2]
user_y = user_data[:][3]
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
with open('./3_user_center.txt' ,'w') as f:
    for i in all_node:
        f.write('{},{},{}\n'.format(i,round(user_center[i][0],4),round(user_center[i][1],4)))
f.close()