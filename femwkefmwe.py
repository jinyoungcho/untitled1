import geocoder

g = geocoder.reverse([40.729417, -74.000460])

print(g.address)
print(g.neighborhood)
print(g.locality)

