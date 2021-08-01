from time import sleep
from sliding_window_counter import SlidingWindowCounterRateLimiter
from client import clientGenerator

apiEndpoints = ["api1", "api2","api3"]


client1 = clientGenerator(apiEndpoints, [ [ -1, -1 ], [ 60, 90 ], [ -1, -1 ] ], "Riya")
client2 = clientGenerator(apiEndpoints, [ [ -1, -1 ], [ 60, 5 ], [ -1, -1 ] ], "Pratham")

myRateLimiter = SlidingWindowCounterRateLimiter(apiEndpoints)

# if client request to avail api service for first time. -- default configuration
myRateLimiter.addUser(client1)
myRateLimiter.addUser(client2)

# Before calling API for the user
while(1):
    if myRateLimiter.shouldAllowServiceCall(client2, "api2"):
        print("Allowed ...")
    else:
        print("NOT ALLOWED")
    # Comment to strike the bottleneck
    sleep(2)
    # To just req. at maximum limit -- aprox.
    # sleep(13)
    print(myRateLimiter.ratelimiterMap[client2.id]["api2"].counts)


# if client de subscribe for the service.
myRateLimiter.removeUser(client1)
myRateLimiter.removeUser(client2)