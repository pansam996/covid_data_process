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

##########edit group size and day here##########
groups = 10
day = 10
################################################


#### read the edge data
edge_list = []
edge_data = pd.read_csv('./Brightkite_edges.txt',header=None,sep='\t')


for i in range(len(edge_data)):
    edge_list.append([edge_data[0][i], edge_data[1][i]])


G = nx.Graph()
# add edge
for i in range(len(edge_list)):
    G.add_edge(edge_list[i][0],edge_list[i][1])


print('edge number :',G.number_of_edges(),'\nnode number :',G.number_of_nodes())

all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()


##### graph.txt
with open('./graph_3.txt','w') as f:
    f.write('{} {},{},{}\n'.format('g',G.number_of_nodes(),G.number_of_edges(),day * groups))
f.close()

#### Node
with open('./graph_3.txt','a') as f:
    for i in all_node:
        node_type = random.randint(0,3)
        R = round(random.uniform(0,1),3)
        Ct = round(random.uniform(0,1),3)
        S = round(random.uniform(0,1),3)
        Cr = round(random.uniform(0,1),3)
        HI = round(random.uniform(0,1),3)
        HA = round(random.uniform(0,1),3)
        HT = round(random.uniform(0,1),3)
        D = round(random.uniform(0,1),3)
        f.write('{} {},{},{},{},{},{},{},{},{},{}\n'.format('n',i , node_type, R, Ct, S, Cr, HI, HA, HT, D))
f.close()

#### Edge
with open('./graph_3.txt','a') as f:
    for i in range(len(all_edge)):
        prob = random.uniform(0,1)
        node1 = all_edge[i][0]
        node2 = all_edge[i][1]
        f.write('{} {},{},{}\n'.format('e', node1,node2,round(prob,3)))
f.close()

#### Calculate the max radius
user_center_data = pd.read_csv('./user_center_3.txt',header=None,sep=',')
user_x = np.array(user_center_data[:][1])
user_y = np.array(user_center_data[:][2])
#### find the farest x_value on +x axis and -x axis
x_max = np.amax(user_x)
x_min = np.amin(user_x)
#### find the farest y_value on +y axis and -y axis
y_max = np.amax(user_y)
y_min = np.amin(user_y)

length = round(haversine(x_max,y_max,x_min,y_min),2)
max_radius = round(length/2,2)
print('diagonal length : ',length)
print('max radius : ',max_radius)

#### Select the group
#### Group
with open('./graph_3.txt','a') as f:
    for d in range(day):
        ## random radius by "normal distrubtion"
        radius = np.random.normal(max_radius,scale=1000000,size = groups)
        ## random user be the center
        centers = np.random.randint(0,G.number_of_nodes() - 1,size = groups)

        for idx in range(groups):
            # empty set
            sd = set()
            cost = random.randint(1,10)
            lv = random.randint(1,3)
            eta = -1
            # find the user that in the center range
            for i in range(len(all_node)):
                center_x = user_center_data[1][centers[idx]]
                center_y = user_center_data[2][centers[idx]]
                compare_x = user_center_data[1][i]
                compare_y = user_center_data[2][i]
                l = haversine(center_x, center_y ,compare_x,compare_y )
                if l <= radius[idx]:
                    sd.add(i)
            f.write('{} {}_{}_{}_{}_{}\n'.format('X', d, cost, lv, eta, ",".join(str(i) for i in sd)))
f.close()

#### user on the graph
plt.figure(figsize=(8,8))
plt.scatter(user_x,user_y)
plt.show()