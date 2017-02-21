from overpass import API
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from geopy.distance import vincenty

##
sample_list = [(40.752169, -73.991961), (40.751888, -73.990477), (40.75207, -73.991261), (40.751879, -73.990644), (40.751976, -73.990263), (40.752, -73.9937), (40.752101, -73.993121), (40.751984, -73.991569), (40.752143, -73.992754), (40.751971, -73.990577), (40.751908, -73.991159), (40.752259, -73.992084), (40.752289, -73.990758), (40.751966, -73.991006), (40.752188, -73.993803), (40.752032, -73.993811), (40.751918, -73.992674), (40.752249, -73.991293), (40.752043, -73.993646), (40.75228, -73.991983), (40.752134, -73.992768), (40.752027, -73.991609), (40.751929, -73.991618), (40.751889, -73.991934), (40.752239, -73.989841), (40.752317, -73.991714), (40.751889, -73.992303), (40.752265, -73.991945), (40.75231, -73.993694), (40.751881, -73.99252), (40.752137, -73.994035), (40.751947, -73.989799), (40.751997, -73.990541), (40.752158, -73.989687), (40.751941, -73.99063), (40.751987, -73.990859), (40.752299, -73.993486), (40.752124, -73.992375), (40.752053, -73.991587), (40.752104, -73.994055), (40.752305, -73.992122), (40.752274, -73.992242), (40.751941, -73.991801), (40.752263, -73.992431), (40.752009, -73.990558), (40.752101, -73.989917), (40.752314, -73.992766), (40.751986, -73.991263), (40.75213, -73.990406), (40.752174, -73.993735), (40.752314, -73.991783), (40.751913, -73.991547), (40.752073, -73.991378), (40.752187, -73.991178), (40.751917, -73.992226), (40.752074, -73.993786), (40.75208, -73.992944), (40.75189, -73.990307), (40.75217, -73.992546), (40.752028, -73.989892), (40.751968, -73.99224), (40.752174, -73.992301), (40.752077, -73.992643), (40.751909, -73.992766), (40.752194, -73.990327), (40.751887, -73.991925), (40.752285, -73.991145), (40.752158, -73.991393), (40.751924, -73.992594), (40.751914, -73.990855), (40.752136, -73.99047), (40.751903, -73.992492), (40.752221, -73.991654), (40.752137, -73.990332), (40.752313, -73.9926), (40.752348, -73.992599), (40.751982, -73.993637), (40.752035, -73.989777), (40.752352, -73.991127), (40.752332, -73.992405), (40.751984, -73.992388), (40.752059, -73.990678), (40.751972, -73.993106), (40.752067, -73.993299), (40.75223, -73.994007), (40.752266, -73.989797), (40.752223, -73.991863), (40.75221, -73.990865), (40.752199, -73.991691), (40.752105, -73.99131), (40.751915, -73.991492), (40.752166, -73.991118), (40.752104, -73.992249), (40.752259, -73.991794), (40.75232, -73.994079), (40.752155, -73.990042), (40.752001, -73.992197), (40.751932, -73.993218), (40.752086, -73.99106), (40.751895, -73.990835)]

##

api = API()
# response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps|crossing"](40.751872, -73.994120 ,40.752353, -73.989678);')
response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps|crossing"](40.751872, -73.994120 ,40.762353, -73.979678);')

node_dic={}
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        # print(x, j[1], j[0])
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

cor_dic=defaultdict(list)
for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)


print("node_dic",node_dic)
print(cor_dic)

node_size = len(node_dic)
# print(node_size)
arc_list = np.zeros((node_size,node_size),dtype='int')
distance_list= np.zeros((node_size,node_size),dtype='float')

print(arc_list)

# x =0
# for i in response['features']:
#     for j in range(len(i['geometry']['coordinates'])):
#         if j != len(i['geometry']['coordinates'])-1:
#             arc_list[cor_dic[node_dic[x]][0]][cor_dic[node_dic[x+1]][0]]+=1
#             print(node_dic[x], cor_dic[node_dic[x]], node_dic[x+1], cor_dic[node_dic[x+1]])
#         x += 1
##################################################
cor_dic2=defaultdict(list)
print("-------------")
for a in cor_dic:
    if len(cor_dic[a])>=2:
        print(cor_dic[a])
        cor_dic2[a]=cor_dic[a][0]
print("------------")
print(cor_dic2)
intersection_list = list(cor_dic2.values())
print(intersection_list)
print(node_dic)
##################################################

intersection_dic={}
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        # print(x, j[1], j[0])
        if x in intersection_list:
            intersection_dic[x] = (coordinate[1], coordinate[0])
        x += 1

print("#######intersection_dic",intersection_dic)
print("#######cor_dic",cor_dic)

arc_list2 = np.zeros((node_size,node_size),dtype='int')
distance_list2= np.zeros((node_size,node_size),dtype='float')



for feature in response['features']:
    # print(feature['geometry']['coordinates'])
    # print(feature['properties'].keys())
    # if 'oneway' in feature['properties'].keys():
    ilen = len(feature['geometry']['coordinates'])
    for i,coordinate in enumerate(feature['geometry']['coordinates']):
        if i != ilen-1:
            cor_key1 = (feature['geometry']['coordinates'][i][1],feature['geometry']['coordinates'][i][0])
            cor_key2 = (feature['geometry']['coordinates'][i+1][1], feature['geometry']['coordinates'][i+1][0])
            # print(cor_dic[cor_key1][0], cor_dic[cor_key2][0])
            arc_list[cor_dic[cor_key1][0]][cor_dic[cor_key2][0]]+=1

            if (cor_key1 in intersection_dic.values()) and (cor_key2 in intersection_dic.values()):
                print(cor_key1, cor_key2)
                arc_list2[cor_dic[cor_key1][0]][cor_dic[cor_key2][0]] += 1

            if 'oneway' not in feature['properties'].keys():
                # print(cor_dic[cor_key2][0], cor_dic[cor_key1][0])
                arc_list[cor_dic[cor_key2][0]][cor_dic[cor_key1][0]] += 1






# print((feature['geometry']['coordinates'][i+1][1],feature['geometry']['coordinates'][i+1][0]))



    # for j in range(len(i['geometry']['coordinates'])):
    #     if j != len(i['geometry']['coordinates'])-1:
    #         arc_list[cor_dic[node_dic[x]][0]][cor_dic[node_dic[x+1]][0]]+=1
    #         print(node_dic[x], cor_dic[node_dic[x]], node_dic[x+1], cor_dic[node_dic[x+1]])
    #     x += 1
#
#
#
# x =0
# for feature in response['features']:
#     print(feature['properties'])
#     print(feature['geometry'])
#     print("----------------")
#     try:
#         if feature['properties']['oneway'] =='yes':
#             for i, coordinate in enumerate(feature['geometry']['coordinates']):
#                 if i != len(feature['geometry']['coordinates']) - 1:
#                     arc_list[cor_dic[node_dic[x]][0]][cor_dic[node_dic[x + 1]][0]] += 1
#
#                     distance = vincenty(node_dic[x],node_dic[x + 1]).km*100 #미터단위
#                     distance_list[cor_dic[node_dic[x]][0]][[cor_dic[node_dic[x + 1]][0]]] = distance
#                     # print("단방향" ,node_dic[x], cor_dic[node_dic[x]], node_dic[x + 1], cor_dic[node_dic[x + 1]])
#                 x += 1
#     except:
#         # print(feature['properties'])
#         for i, coordinate in enumerate(feature['geometry']['coordinates']):
#             if i != len(feature['geometry']['coordinates']) - 1:
#                 arc_list[cor_dic[node_dic[x]][0]][cor_dic[node_dic[x + 1]][0]] += 1
#                 arc_list[cor_dic[node_dic[x + 1]][0]][cor_dic[node_dic[x]][0]] += 1
#
#                 distance = vincenty(node_dic[x], node_dic[x + 1]).km * 100  # 미터단위
#                 distance_list[cor_dic[node_dic[x]][0]][[cor_dic[node_dic[x + 1]][0]]] = distance
#                 distance_list[cor_dic[node_dic[x+1]][0]][[cor_dic[node_dic[x]][0]]] = distance
#
#                 # print("양방향",
#                 #       node_dic[x], cor_dic[node_dic[x]], node_dic[x + 1], cor_dic[node_dic[x + 1]],"<->" ,node_dic[x + 1], cor_dic[node_dic[x + 1]],node_dic[x], cor_dic[node_dic[x]]
#                 #       )
#                 x += 1





#####################################################
Arc_tuple_List = []
for x,y in enumerate(arc_list2):
    for i,j in enumerate(y):
        if arc_list2[x,i] != False:
            Arc_tuple_List.append((x,i))
print(Arc_tuple_List)

# def closest_node(node, nodes):
#     nodes = np.asarray(nodes)
#     deltas = nodes - node
#     dist_2 = np.einsum('ij,ij->i', deltas, deltas)
#     return np.argmin(dist_2)
#
# print(closest_node(2,node_dic),"####")


new_node_dic = {}
for nodes in cor_dic.values():
    new_node_dic[nodes[0]] = node_dic[nodes[0]]

print(node_dic)
print(new_node_dic)

G = nx.DiGraph()
G.add_nodes_from(intersection_dic)
G.add_edges_from(Arc_tuple_List)


# for i,row in enumerate(distance_list.tolist()):
#     for j,value in enumerate(row):
#         if distance_list[i][j] != False:
#             G.add_edge(i,j,weight=distance_list[i][j])

# edge_labels=dict([((u,v,),d['weight'])for u,v,d in G.edges(data=True)])
nx.draw(G, pos=new_node_dic,with_labels=True, node_size = 300, width=0.3)
# nx.draw_networkx_edge_labels(G,pos=node_dic,edge_labels=labels)

# nx.draw_networkx_nodes(G, pos = node_dic)
plt.show()

