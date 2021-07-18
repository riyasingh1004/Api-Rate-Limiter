from time import sleep
from sliding_window_counter import SlidingWindowCounterRateLimiter
from client import clientGenerator
import threading

def addSingleUser(lock, client):
    with lock:
        myRateLimiter.addUser(client)

apiEndpoints = ["api1", "api2","api3"]

# client1 = clientGenerator(apiEndpoints, [ [ -1, -1 ], [ 60, 90 ], [ -1, -1 ] ], "Riya")
# client2 = clientGenerator(apiEndpoints, [ [ -1, -1 ], [ 60, 5 ], [ -1, -1 ] ], "Pratham")

clients = []

for cid in range(1000):
    clients.append(clientGenerator(apiEndpoints, [ [ -1, -1 ], [ -1, -1 ], [ -1, -1 ] ], "user"+str(cid)))

myRateLimiter = SlidingWindowCounterRateLimiter(apiEndpoints)

lock = threading.Lock()
w = []
for cid in range(1000):
    w.append(threading.Thread(target=addSingleUser, args=(lock, clients[cid], )))
# w1 = threading.Thread(target=addSingleUser, args=(lock, client1, ))
# w2 = threading.Thread(target=addSingleUser, args=(lock, client2, ))

# if client request to avail api service for first time. -- default configuration
# myRateLimiter.addUser(client1)
# myRateLimiter.addUser(client2)
# w1.start()
# w2.start()
for cid in range(1000):
    w[cid].start()

# if client de subscribe for the service.
# myRateLimiter.removeUser(client1)
# myRateLimiter.removeUser(client2)
for cid in range(100):
    myRateLimiter.removeUser(clients[cid])