from overpass import API

api = API()
api.timeout=900

# response = api.Get('way["name"="6th Avenue"];')
# response = api.Get('way["highway"]["tiger:county"= "New York, NY"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps"];')


response = api.Get('way["highway"]["highway"!~"footway|cycleway|path|service|track|pedestrian|steps"](40.752197, -73.993588 ,40.762937, -73.973621);')

# response = api.Get('way[highway][name="6th Avenue"];node(w)->.n1;way[highway][name="West 23rd Street"];node(w)->.n2;node.n1.n2;')

print(response)
# print(response.keys())
for a in response['features']:
    print(a['geometry']['coordinates'])
    print(a['properties'])

    try:
        print(a['properties']['oneway'])
    except:
        print('no')
    print("------")