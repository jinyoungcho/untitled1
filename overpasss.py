from overpass import API
from time import sleep
from sys import exc_info

api = API()

locations = [(50.406029, 30.619727), (27.988056, 86.925278)]
for loc in locations:
    xx, yy = loc[0], loc[1]
    try:
        response = api.Get('way["highway"](around:50,{0},{1});'.format(loc[0], loc[1]))
        print("For location with coordinates {0}, {1} found way IDs:".format(loc[0], loc[1]))
        if len(response['elements']) > 0:
            for way in response['elements']:
                print(way['id'])
        else:
            print("No ways")
        sleep(1)
    except:
        print("Got error: {0}".format(exc_info())[0])