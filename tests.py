import time
import random

base = set(range(1,100000))



start = time.time()

for i in range(100):
    r = random.randint(0,1000000)
    if(r in base):
        print "is in !!!!"
print time.time() - start