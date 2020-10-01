import os
import numpy as np
import pandas as pd
import random
import math
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import networkx as nx
import matplotlib.pyplot as plt


#############edit threshlod ,day , groups here#####################
threshold = 50
day = 10
groups = 10
###################################################################

#### read the data
path = './Kissler_DataS1.csv'

data = pd.read_csv(path,header=None,sep=',')

# column info
time = data[:][0] # timeslot
id_1 = data[:][1] # userid 1
id_2 = data[:][2] # userid 2
distance = data[:][3] # distance

#### add the mathc nodes and edges
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

print('edge number :',G.number_of_edges(),'\nnode number :',G.number_of_nodes())

all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()

#### Graph.txt
with open('./graph_4.txt','w') as f:
    f.write('{} {},{},{}\n'.format('g', G.number_of_nodes(), G.number_of_edges(), day*groups))
f.close()

#### Node
with open('./graph_4.txt','a') as f:
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
        f.write('{} {},{},{},{},{},{},{},{},{},{}\n'.format('n',i - 1, node_type, R, Ct, S, Cr, HI, HA, HT, D))
f.close()


#### Edge
with open('./graph_4.txt','a') as f:
    for i in range(len(all_edge)):
        prob = random.uniform(0,1)
        node1 = all_edge[i][0] - 1
        node2 = all_edge[i][1] - 1
        f.write('{} {},{},{}\n'.format('e',node1,node2,round(prob,3)))
f.close()


#### Group
# random select
with open('./graph_4.txt','a') as f:
    for d in range(day):
        for group_num in range(groups):
            user_num = random.randint(60,120)
            users = np.random.randint(0,G.number_of_nodes()-1,size = user_num)
            cost = random.randint(1,10)
            lv = random.randint(1,3)
            eta = -1
            f.write('{} {}_{}_{}_{}_{}\n'.format('X', d, cost, lv, eta, ",".join(str(i) for i in users)))
f.close()

#### user on the graph
plt.figure(1,figsize=(8,8))
nx.draw_networkx_nodes(G,pos=nx.random_layout(G),node_size=20)
plt.show()