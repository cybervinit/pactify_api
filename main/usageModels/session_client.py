import os
import redis

class SessionClient:
	def __init__(self, host, port):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

	def add(self, username, data):
		self.r.set(username, data)

	def pop(self, username):
		self.r.delete(username)

	def get(self, username):
		return self.r.get(username)


sess = SessionClient('localhost', 6379) # TODO: change to dynamic set of urls


