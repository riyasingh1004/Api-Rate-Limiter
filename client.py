import uuid

class clientGenerator:	
	def __init__(self, apiList, reqList, name, namespace="global"):
		#can be set to partition the api according to namespace
		self.id = uuid.uuid4()
		self.name = name
		self.namespace = namespace
		self.apiRequest = {}
		for api_idx in range(len(apiList)):
			self.apiRequest[apiList[api_idx]] = {}
			# sets the window time as default(60) for -1
			self.apiRequest[apiList[api_idx]]['windowTime'] = (60 if reqList[api_idx][0] == -1 else reqList[api_idx][0])
			# sets the num of requests as default(100) for -1 
			self.apiRequest[apiList[api_idx]]['numOfReq'] = (100 if reqList[api_idx][1] == -1 else reqList[api_idx][1])

