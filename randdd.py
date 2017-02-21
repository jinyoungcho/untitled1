import random

a = random.randrange(40751872,40752353)
b = random.randrange(-73994120,-73989678)

def a(a,b,c,d):
    n1 = random.randrange(a,c)
    n2 = random.randrange(b,d)
    return (n1,n2)

list_a=[]

# print(a(40751872,-73994120,40752353,-73989678))
for i in range(100):
    asdf = a(40751872,-73994120 ,40752353 , -73989678)
    list_a.append((float(asdf[0])/1000000,float(asdf[1])/1000000))

print(list_a)