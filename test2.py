from concurrent import futures
from time import sleep
from sliding_window_counter import SlidingWindowCounterRateLimiter
from client import clientGenerator
import concurrent.futures, requests

def addSingleUser(client):
    try:
        print(" *- Starting new thread for " + client.name + " ...")
        myRateLimiter.addUser(client)
        print(" *- Exiting thread for " + client.name + " ...")
        return client
    except Exception:
        raise Exception("User already present -- Exception returned")

apiEndpoints = ["api1", "api2","api3"]

clients = []

for cid in range(10):
    clients.append(clientGenerator(apiEndpoints, [ [ -1, -1 ], [ -1, -1 ], [ -1, -1 ] ], "user"+str(cid)))

myRateLimiter = SlidingWindowCounterRateLimiter(apiEndpoints)

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executer:
    for res in executer.map(addSingleUser, clients, timeout=30):
        print("[] Added " + res.name + " to the database starting new thread...")

# if client de subscribe for the service.
for cid in range(10):
    myRateLimiter.removeUser(clients[cid])