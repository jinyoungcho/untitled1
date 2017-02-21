from collections import defaultdict
from geopy.distance import vincenty
import pandas as pd
import json, io

with open('data.json', encoding='utf-8') as data_file:
    response = json.loads(data_file.read())

node_dic={}
cor_dic=defaultdict(list)
x = 0
for features in response['features']:
    for coordinate in features['geometry']['coordinates']:
        node_dic[x] = (coordinate[1], coordinate[0])
        x += 1

for node_num in node_dic:
    cor_dic[node_dic[node_num]].append(node_num)

#####################################################################################################################

intersection_cor_dic={}
cor_intersection_dic={}

for key in cor_dic:
    if len(cor_dic[key]) > 1:
        cor_intersection_dic[key] = cor_dic[key][0]
        intersection_cor_dic[cor_dic[key][0]] = key

intersection_size = len(intersection_cor_dic)
distance_dic={}
street_dic={}

for feature in response['features']:
    sample_coordinates = []
    coordinates = feature['geometry']['coordinates']
    for cor in coordinates:
        if (cor[1],cor[0]) in cor_intersection_dic.keys():
            sample_coordinates.append((cor[1],cor[0]))
    for i in range(len(sample_coordinates)-1):
        cor_i = sample_coordinates[i]
        cor_j = sample_coordinates[i+1]
        distance_dic[cor_intersection_dic[cor_i], cor_intersection_dic[cor_j]] = vincenty(cor_i,cor_j).km*100
        if "name" in feature["properties"]:
            street_dic[cor_intersection_dic[cor_i], cor_intersection_dic[cor_j]] = feature["properties"]["name"]
        else:
            street_dic[cor_intersection_dic[cor_i], cor_intersection_dic[cor_j]] = "unknown"
            print(feature["properties"])
            print(feature['geometry']['coordinates'])
            print("-----")
        if "oneway" not in feature["properties"].keys():
            distance_dic[cor_intersection_dic[cor_j], cor_intersection_dic[cor_i]] = vincenty(cor_j, cor_i).km * 100
            if "name" in feature["properties"]:
                street_dic[cor_intersection_dic[cor_j], cor_intersection_dic[cor_i]] = feature["properties"]["name"]
            else:
                street_dic[cor_intersection_dic[cor_j], cor_intersection_dic[cor_i]] = "unknown"

Arc_tuple_List = []
for key in distance_dic.keys():
    Arc_tuple_List.append((key[0],key[1]))

df = pd.DataFrame()
arc_i_list = [arc[0]for arc in Arc_tuple_List]
arc_j_list = [arc[1]for arc in Arc_tuple_List]
arc_distace_list = [distance_dic[arc[0],arc[1]]for arc in Arc_tuple_List]
street_name_list = [street for street in street_dic.values()]
df["i"] = arc_i_list
df["j"] = arc_j_list
df["distance"] = arc_distace_list
df["street"] = street_name_list
df.to_csv("Arc.csv")

df2 = pd.DataFrame()
intersection_list = [intersection for intersection in intersection_cor_dic]
Lat_list = [coordinate[0] for coordinate in intersection_cor_dic.values()]
Lon_list = [coordinate[1] for coordinate in intersection_cor_dic.values()]
df2["node"] = intersection_list
df2["Lat"] = Lat_list
df2["Lon"] = Lon_list
df2.to_csv("Node.csv")