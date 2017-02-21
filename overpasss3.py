from overpass import API

api = API()

locations=(40.748164, -73.949755)

x = locations[0]
y = locations[1]

response = api.Get(('way["highway"](around:10,{0},{1});').format(x, y))

print(response.keys())
for a in response['features']:
    print(a)

print("-----------------------")

print(response['features'][0])
for a in response['features'][0]:
    print(a)

print("-----------------------")

print(response['features'][0]['properties'])

for a in response['features'][0]['properties']:
    print(a, ':' ,response['features'][0]['properties'][a])