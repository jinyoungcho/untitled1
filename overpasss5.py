from overpass import API
from collections import defaultdict

api = API()
# response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps"](40.751872, -73.994120 ,40.752353, -73.989678);',responseformat="xml")
response2 = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps"](40.751872, -73.994120 ,40.752353, -73.989678);')

# print(response)
# print(response2)

way_dic = defaultdict

for a in response2["features"]:
    print(a["geometry"]["coordinates"])