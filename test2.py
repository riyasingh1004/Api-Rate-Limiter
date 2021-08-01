from sliding_window_counter import SlidingWindowCounterRateLimiter
from client import clientGenerator
import concurrent.futures

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

# Creating 10 clinets
for cid in range(10):
    clients.append(clientGenerator(apiEndpoints, [ [ -1, -1 ], [ -1, -1 ], [ -1, -1 ] ], "user"+str(cid)))

myRateLimiter = SlidingWindowCounterRateLimiter(apiEndpoints)

# Creating users asynchronously for concurrent calls
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executer:
    for res in executer.map(addSingleUser, clients, timeout=30):
        print("[] Ended " + res.name + " thread... starting new thread...")

# if client unsubscribes from the service.
for cid in range(10):
    myRateLimiter.removeUser(clients[cid])