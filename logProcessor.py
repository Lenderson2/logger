from collections import defaultdict
import ipdb



class logProcessor(object):
	"""
	Class to process website user logs
	"""

	def __init__(self):
		"""
		initialize empty logProcessor
		"""
		self.time_sessions = None
		self.averages = None

	def process(self, filename):
		"""
		top level function to process log file
		"""
		file = open(filename, 'r')
		self.time_sessions = reduce(self.collect_time_sessions, file, {})
		self.averages = {key: float(value[0])/value[1] \
			for key, value in self.time_sessions.iteritems()}
		file.close()

	def collect_time_sessions(self, collection, record):
		"""
		reduce function for use in self.process

		returns dict "collection" for continued reduction
		"""
		r = record.strip().split(',')
		userid, time, action = r[0], int(r[1]), r[2]
		if userid not in collection:
			collection[userid] = [0, 0, time, action]
			return collection
		last_record = collection[userid]
		if last_record[3] == 'open' and action == 'close':
			tot_time = last_record[0] + time - last_record[2]
			sessions = collection[userid][1] + 1
			update = [tot_time, sessions, time, action]
			collection[userid] = update
			return collection
		else:
			collection[userid][2] = time
			collection[userid][3] = action
			return collection

	def to_csv(self):
		"""
		"""
		pass

if __name__ == '__main__':
	lp = logProcessor()
	lp.process('test.log')
	print lp.averages
