from collections import defaultdict
import ipdb
import argparse



class AverageProcessor(object):
	"""
	Process website log file to produce user average time per session
	
	This implementation ingests records 
	in the form "userid,timestamp,action"

	Parameters
    ----------
    default_session : int, 'average' or None, default=None
    	If not None, session length for two records 
    	that are missing intermediary record(s) will
    	be set to default_session. Otherwise sessions
    	associated with 'close''close' or 'open''open'
    	log sequences are ignored.

	Attributes
    ----------
    user_totals : dict
    	Mapping of user ids to a list in the form of
    	[user total time (int), user total sessions (int)]
    user_averages : dict
        A mapping of user ids to average seconds per visit
        created during the 'process' method.
	"""

	def __init__(self, default_session=None):
		self.default_session = default_session

	def process(self, logfile):
		"""
		INPUT: logfile: string 
		OUTPUT: list of tuples

		Injests log file and returns list containing
		(userid, average time in seconds) tuples.
		"""
		file = open(logfile, 'r')
		user_last_record = dict()
		self.user_totals = defaultdict(lambda: [0,0])

		for line in file:
			userid, time, action = self._parse_line(line)

			if userid in user_last_record:
				last_time, last_action = user_last_record[userid]
				session_length = self._calc_session_length(
					time, action, last_time, last_action)
				if session_length > 0:
					self.user_totals[userid][0] += session_length
					self.user_totals[userid][1] += 1

			user_last_record[userid] = [time, action]

		self.user_averages = self._calc_averages(self.user_totals)
		return self.user_averages

	def _parse_line(self, line):
		"""
		INPUT: line: string 
		OUTPUT: userid: string,
				time: int,
				action: string

		Seperates and assgins a line "userid,timestamp,action\n"
		into userid, time, action
		"""
		record = line.strip().split(',')
		return record[0], int(record[1]), record[2]

	def _calc_session_length(self, time, action, last_time, last_action):
		"""
		INPUT: time: int,
				action: str,
				last_time: int,
				last-action: str
		OUTPUT: int

		Using current and last record, determines
		session length if applicable. Returns 0 otherwise.
		"""
		if last_action == 'open' and action == 'close':
			return time - last_time
		elif (self.default_session != None and action == last_action):
			return self.default_session*60	
		else:		
			return 0

	def _calc_averages(self, user_totals):
		"""
		INPUT: user_totals: dict of lists 
		OUTPUT: list of tuples

		Transforms user_totals into list of
		(userid, average time) tuples.
		"""
		averages = list()
		for userid, totals in user_totals.iteritems():
			total_time, sessions = totals
			averages.append((userid, float(total_time)/sessions))
		return averages


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("filename",
						help="path to log file to be processed",
						type=str)
	parser.add_argument("-d", "--default_session",
						default=None,
						type=int,
                    	help="optional default session length for log errors.")
	args = parser.parse_args()

	# print args
	ap = AverageProcessor(default_session=args.default_session)
	results = ap.process(args.filename)
	print results
