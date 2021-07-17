import time
import threading

class RequestCounters:
	# Every window time is broken down to 60 parts
	# 100 req/min translates to requests = 100 and windowTimeInMin = 60
	def __init__(self, requests, windowTimeInMin, bucketSize=12):
		self.counts = {}
		self.totalCounts = 0
		self.requests = requests
		self.windowTimeInMin = windowTimeInMin
		self.bucketSize = bucketSize
		self.lock = threading.Lock()

	# Gets the bucket for the timestamp
	def getBucket(self, timestamp):
		factor = self.windowTimeInMin / self.bucketSize
		return (timestamp // factor) * factor

	# Gets the bucket list corresponding to the current time window
	def _getOldestvalidBucket(self, currentTimestamp):
		return self.getBucket(currentTimestamp - self.windowTimeInMin)

	# Remove all the older buckets that are not relevant anymore
	def evictOlderBuckets(self, currentTimestamp):
		oldestValidBucket = self._getOldestvalidBucket(currentTimestamp)
		bucketsToBeDeleted = filter(
			lambda bucket: bucket < oldestValidBucket, self.counts.keys())
		for bucket in bucketsToBeDeleted:
			bucketCount = self.counts[bucket]
			self.totalCounts -= bucketCount
			del self.counts[bucket]

class SlidingWindowCounterRateLimiter:
	
	def __init__(self, apiList):
		self.lock = threading.Lock()
		self.ratelimiterMap = {}
		self.apiList = apiList
		
	def addUser(self, userId, requests=100, windowTimeInMin=60):
		with self.lock:
			for api in self.apilist:
				if userId in self.ratelimiterMap[api]:
					raise Exception("User already present")
				self.ratelimiterMap[api][userId] = RequestCounters(requests, windowTimeInMin)

	def removeUser(self, userId):
		with self.lock:
			for api in self.apilist:
				if userId in self.ratelimiterMap[api]:
					del self.ratelimiterMap[api][userId]

	@classmethod
	def getCurrentTimestampInSec(cls):
		return int(round(time.time()))

	def shouldAllowServiceCall(self, userId):
		with self.lock:
			for api in self.apiList:
				if userId not in self.ratelimiterMap[api]:
					raise Exception("User is not present")
			userTimestamps = self.ratelimiterMap[api][userId]
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