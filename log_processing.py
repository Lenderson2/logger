from collections import defaultdict
import ipdb



class AverageProcessor(object):
	"""
	Process website log file to produce user average time per session
	
	This implementation ingests records 
	in the form "userid,timestamp,action"

	Parameters
    ----------
    max_session : None or int, default=None
    	If not None, set a maxium session length between
    	'Open' and 'Close' actions to max_session minutes,
    	and set session's length to default_session minutes.
    	If max_session not None, and default_session == None,
    	default_session is set to max_session.

    	In two subsequent sessions '1' and '2', setting max_session 
    	accounts for potential co-occurrence of missing
    	session-1's 'Close' record, and session-2's 'Open'
    	record, which would innacurately inflate the session
    	length. It also allows for discretionary session
    	length limiting.

    default_session : int or None, default=None
    	If not None, session length for two records 
    	that are missing intermediary record(s) will
    	be set to default_session. Otherwise sessions
    	associated with 'close''close' or 'open''open'
    	log sequences are ignored.

    	If max_session not None, and default_session is None,
    	default_session is set to max_session.

    correct_errors: boolean, default = False
    	Non user facing control flow variable to prevent


	Attributes
    ----------
    user_totals : dict
    	Mapping of user ids to a list in the form of
    	[user total time (int), user total sessions (int)]
    user_averages : dict
        A mapping of user ids to average seconds per visit
        created during the 'process' method.
	"""

	def __init__(self, max_session=None,
					default_session=None,
					correct_errors=False):
		self.max_session = max_session
		self.default_session = default_session
		self.correct_errors = False
		if max_session != None and default_session == None:
			self.default_session = max_session
		if max_session == None and default_session != None:
			self.correct_errors = True

	def process(self, logfile):
		"""
		INPUT: logfile: string 
		OUTPUT: list of tuples

		Injests log file and returns list containing
		(userid, average time) tuples.
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
			session_length = time - last_time
			if (self.max_session != None
					and self.max_session*60 < session_length):
				return self.default_session*60
			else:
				return session_length

		elif (self.default_session != None 
				and self.correct_errors
				and action == last_action):
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
	ap = AverageProcessor()
	ap.process('data/big_test.log')
