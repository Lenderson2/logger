from collections import defaultdict
import ipdb



class AverageProcessor(object):
	"""
	Process website log file to produce user average time per session
	
	This implementation ingests records 
	in the form "userid,timestamp,action"

	Parameters
    ----------
    default_session: int or None, default=None
    	If not None, session length for two records 
    	that are missing intermediary record(s) will
    	be set to default_session. Otherwise sessions
    	associated with subsequent 'close' or 'open' 
    	records are ignored.

    	If max_session not None, and default_session is None,
    	default_session is set to max_session.

    max_session: None or int, default=None
    	If not None, set a maxium session length between
    	'Open' and 'Close' actions to max_session minutes,
    	and set session's length to default_session minutes.
    	If max_session not None, and default_session == None,
    	default_session is set to max_session.

    	In two subsequent sessions '1' and '2', setting max_session 
    	accounts for potential co-occurrence of missing
    	session-1's 'Close' record, and session-2's 'Open'
    	record, which would innacurately inflate the session
    	length.

    input : string {'filename', 'file', 'content'}
        If 'filename', the sequence passed as an argument to fit is
        expected to be a list of filenames that need reading to fetch
        the raw content to analyze.

	Attributes
    ----------
    vocabulary_ : dict
        A mapping of terms to feature indices.
	"""

	def __init__(self, default_session=None, max_session=None):
		self.default_session = default_session
		if default_session == None and max_session != None:
			self.default_session = max_session
		self.max_session = max_session

	def process(self, logfile):
		"""
		INPUT: logfile: string 
		OUTPUT: list of tuples

		Injests log file and returns list containing
		(userid, average time) tuples.
		"""
		file = open(logfile, 'r')
		user_last_record = dict()
		user_totals = defaultdict(lambda: [0,0])

		for line in file:
			userid, time, action = self._parse_line(line)

			if userid in user_last_record:
				last_time, last_action = user_last_record[userid]
				session_length = self._calc_session_length(
					time, action, last_time, last_action)
				if session_length > 0:
					user_totals[userid][0] += session_length
					user_totals[userid][1] += 1

			user_last_record[userid] = [time, action]

		averages = self._calc_averages(user_totals)
		return averages

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
