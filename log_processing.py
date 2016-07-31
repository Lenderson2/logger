from collections import defaultdict
import ipdb



class AverageProcessor(object):
	"""
	Process website log file to produce user average time per session
	
	This implementation ingests records 
	in the form "userid,timestamp,action"

	Parameters
    ----------
    log_errors: string {'ignore', 'average'} or int, default='ignore'
    	If 'ignore'

    max_session: None or int, default=None
    	If not None, set a maxium session length between
    	'Open' and 'Close' actions to max_session minutes.

    	In two subsequent sessions, setting max_session 
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

	def __init__(self, max_session=None):
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
		user_totals = dict()

		for line in file:
			userid, time, action = self._get_fields_from_line(line)

			if userid not in user_last_record:
				user_last_record[userid] = [time, action]
				user_totals[userid] = [0, 0]
				continue

			last_time, last_action = user_last_record[userid]

			if last_action == 'open' and action == 'close':
				session_length = self._calc_session_length(time, last_time)
				user_totals[userid][0] += session_length
				user_totals[userid][1] += 1
			user_last_record[userid] = [time, action]

		averages = self._calc_averages(user_totals)
		return averages

	def _get_fields_from_line(self, line):
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

	def _calc_session_length(self, time, last_time):
		"""
		INPUT: time: int, last_time: int 
		OUTPUT: int

		Returns session lenght by subtracting time stamps.
		if self.max_session is not None, limits session length
		to self.max_session minutes.
		"""
		session_length = time - last_time
		if self.max_session != None:
			max_seconds = self.max_session*60
			if max_seconds < session_length:
				session_length = max_seconds
		return session_length

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
