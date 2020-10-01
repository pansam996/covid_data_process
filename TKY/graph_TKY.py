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

#############edit threshold ,day ,groups here#####################
threshold = 500
day = 10
groups = 10
##################################################################

#### Read the data
tky_data = pd.read_csv('./dataset_TSMC2014_TKY.txt',header=None,sep='\t',encoding='latin1')

# column info
all_user = tky_data[:][0]
user_x = tky_data[:][4]
user_y = tky_data[:][5]

# process the unique date
all_time = tky_data[:][7]
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
# with open('./user_user_distance_TKY.txt','w') as f:
#     for idx in range(len(unique_date)) :
#         print('='*10,idx,'='*10)
#         select_date_datas = tky_data [all_time == unique_date[idx] ]
#         index_table = list(select_date_datas[0])
#         select_date_id = np.unique(np.array(select_date_datas[0]))
#         select_date_id = sorted(select_date_id)
#         ## calculate user1 and user2 distance in select date
#         for user1 in select_date_id:
#             user1_index = index_table.index(user1)
#             user1_x = select_date_datas.iloc[user1_index][4]
#             user1_y = select_date_datas.iloc[user1_index][5]
#             for user2 in select_date_id:
#                 if user1 >= user2:
#                     continue
#                 # calculate distance
#                 else:
#                     user2_index = index_table.index(user2)
#                     user2_x = select_date_datas.iloc[user2_index][4]
#                     user2_y = select_date_datas.iloc[user2_index][5]
#                     d = int(haversine(user1_x, user1_y, user2_x, user2_y))
#                     if d <= 1000:
#                         f.write('{},{},{},{}\n'.format(idx, user1, user2, d))
# f.close()

#### Read the user_user_distance data
path = './user_user_distance_TKY.txt'

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

print('edge number :',G.number_of_edges(),'\nnode number :',G.number_of_nodes())

all_edge = list(G.edges)
all_edge.sort()

all_node = list(G.nodes)
all_node.sort()

#### Graph.txt
with open('./graph_TKY.txt','w') as f:
    f.write('{} {},{},{}\n'.format('g', G.number_of_nodes(), G.number_of_edges(), day*groups))
f.close()

#### Node
with open('./graph_TKY.txt','a') as f:
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
with open('./graph_TKY.txt','a') as f:
    for i in range(len(all_edge)):
        prob = random.uniform(0,1)
        node1 = all_edge[i][0] - 1
        node2 = all_edge[i][1] - 1
        f.write('{} {},{},{}\n'.format('e',node1,node2,round(prob,3)))
f.close()

#### Read the checkin data
path = './dataset_TSMC2014_TKY.txt'

user_data = pd.read_csv(path,header=None,sep='\t',encoding='latin1')

#### column info
user_id = user_data[:][0]
user_x = user_data[:][4]
user_y = user_data[:][5]
check_in_id = np.unique(np.array(user_id))

print('check in id number : ',check_in_id.shape)

#### Calculate the user center
# user_center = { u : (0,0) for u in all_node}

# for i in check_in_id:
#     x = sum(user_x[user_id == i]) / len(user_id[user_id == i])
#     y = sum(user_y[user_id == i]) / len(user_id[user_id == i])
#     if math.isnan(x) or math.isnan(y):
#         user_center[i] = (0,0)
#     else:
#         user_center[i] = (x, y)

# # save the user center
# with open('./user_center_TKY.txt' ,'w') as f:
#     for i in all_node:
#         f.write('{},{},{}\n'.format(i,round(user_center[i][0],4),round(user_center[i][1],4)))
# f.close()

#### Calculate the max radius
user_center_data = pd.read_csv('./user_center_TKY.txt',header=None,sep=',')
user_x = np.array(user_center_data[:][1])
user_y = np.array(user_center_data[:][2])
## find the farest x_value on +x axis and -x axis
x_max = np.amax(user_x)
x_min = np.amin(user_x)
## find the farest y_value on +y axis and -y axis
y_max = np.amax(user_y)
y_min = np.amin(user_y)

length = round(haversine(x_max,y_max,x_min,y_min),2)
max_radius = round(length/2,2)
print('diagonal length : ',length)
print('max radius : ',max_radius)

#### Select the group
## group
with open('./graph_TKY.txt','a') as f:
    for d in range(day):
        ## random radius by "normal distrubtion"
        radius = np.random.normal(max_radius,scale=10000,size = groups)
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