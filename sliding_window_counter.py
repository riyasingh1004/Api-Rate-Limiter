import time
import threading

class RequestCounters:
	# Every window time is broken down to 60 parts
	# 100 req/min translates to requests = 100 and windowTimeInSec = 60
	def __init__(self, requests, windowTimeInSec, bucketSize=10):
		self.counts = {}
		self.totalCounts = 0
		self.requests = requests
		self.windowTimeInSec = windowTimeInSec
		self.bucketSize = bucketSize
		self.lock = threading.Lock()

	# Gets the bucket for the timestamp
	def getBucket(self, timestamp):
		factor = self.windowTimeInSec / self.bucketSize
		return (timestamp // factor) * factor

	# Gets the bucket list corresponding to the current time window
	def _getOldestvalidBucket(self, currentTimestamp):
		return self.getBucket(currentTimestamp - self.windowTimeInSec)

	# Remove all the older buckets that are not relevant anymore
	def evictOlderBuckets(self, currentTimestamp):
		oldestValidBucket = self._getOldestvalidBucket(currentTimestamp)
		bucketsToBeDeleted = filter(
			lambda bucket: bucket < oldestValidBucket, self.counts.keys())
		for bucket in list(bucketsToBeDeleted):
			bucketCount = self.counts[bucket]
			self.totalCounts -= bucketCount
			del self.counts[bucket]

class SlidingWindowCounterRateLimiter:
	def __init__(self, apiList):
		self.lock = threading.Lock()
		self.ratelimiterMap = {}
		self.apiList = apiList
		
	def addUser(self, user):
		with self.lock:
			if user.id in self.ratelimiterMap:
					raise Exception("User already present")
			self.ratelimiterMap[user.id] = {}
			for api in self.apiList:
				self.ratelimiterMap[user.id][api] = RequestCounters(user.apiRequest[api]['numOfReq'], user.apiRequest[api]['windowTime'])
			print(" -- Added -- " + str(user.name) + " to the database ...")

	def removeUser(self, user):
		with self.lock:
			if user.id in self.ratelimiterMap:
					del self.ratelimiterMap[user.id]
			print("-- Removed -- " + str(user.name) + " from the database ...")

	@classmethod
	def getCurrentTimestampInSec(cls):
		return int(round(time.time()))

	def shouldAllowServiceCall(self, user, api):
		with self.lock:
			if user.id not in self.ratelimiterMap:
					raise Exception("User is not present")
			userTimestamps = self.ratelimiterMap[user.id][api]
			with userTimestamps.lock:
				currentTimestamp = self.getCurrentTimestampInSec()
				# remove all the existing older timestamps
				userTimestamps.evictOlderBuckets(currentTimestamp)
				currentBucket = userTimestamps.getBucket(currentTimestamp)
				userTimestamps.counts[currentBucket] = userTimestamps.counts.get(currentBucket, 0) + 1
				userTimestamps.totalCounts += 1
				if userTimestamps.totalCounts > userTimestamps.requests:
					return False
				return True
