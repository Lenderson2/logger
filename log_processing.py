# Author: Lee Henderson <lee.henderson2@gmail.com>
# Processor class to process website log files
# and produce user average time per session.

# When importing to another script, ensure
# that 'process' method is executed before 'to_csv'.

# Averages can also be computed from command line.
# Must provide log file and output csv filename
# as arguments.


from collections import defaultdict
import ipdb
import argparse
from datetime import datetime



class AverageProcessor(object):
	"""
	Process website log file to produce user average time per session
	
	This implementation ingests records 
	in the form "userid,timestamp,action".

	Parameters
    ----------
    default_session : int, 'average' or None, default=None
    	If None, sessions associated with 'close''close' 
    	or 'open''open' log sequences are ignored. 

    	If int, session length for 'close''close' 
    	or 'open''open' log sequences are set to 
    	default_session minutes.

    	If 'average', session length for 'close''close' 
    	or 'open''open' log sequences are set to 
    	the user's average session length for sessions
    	alread processed in the logfile. If no sessions
    	have been processed for a given user, the
    	session is ignored.

	Attributes
    ----------
    user_totals : dict
    	Mapping of user ids to a list in the form of
    	[user total time (int), user total sessions (int)]
    user_averages : dict
    	A list of tuples containing 
    	(user id, average seconds per visit (float))
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
		start = datetime.now()
		user_last_record = dict()
		self.user_totals = defaultdict(lambda: [0,0])

		update = "Processed {} million lines.\n\tElapsed time: {}"

		with open(logfile, 'r') as file:
			for i,line in enumerate(file):
				if i%1000000 == 0:
					print update.format(i/1000000, (datetime.now() - start))

				userid, time, action = self._parse_line(line)
				if userid in user_last_record:
					last_time, last_action = user_last_record[userid]
					session_length = self._calc_session_length(
						time,action, last_time, last_action,
						self.user_totals, userid)

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
		into userid, time, action.
		"""
		record = line.strip().split(',')
		return record[0], int(record[1]), record[2]

	def _calc_session_length(
			self, time, action, last_time, last_action, user_totals, userid):
		"""
		INPUT: time: int,
				action: str,
				last_time: int,
				last-action: str
				user_totals: dict
				userid: str
		OUTPUT: int

		Using current and last record, determines
		session length if applicable. Returns 0 otherwise.

		If self.default_session != None, address log errors
		of 'close' 'close', or 'open' 'open' sequence by
		providing a default session length or the user's
		average session length.
		"""
		if last_action == 'open' and action == 'close':
			return time - last_time

		if self.default_session != None and action == last_action:
			if type(self.default_session) == int:
				return self.default_session*60
			elif self.default_session == 'average':
				total_time, sessions = user_totals[userid]
				if sessions > 0:
					return float(total_time)/sessions

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

	def to_csv(self, output_file):
		"""
		INPUT: output_file: str 
		OUTPUT: None

		Writes user_averages to CSV in form "userid,average\n".
		Should only be called after process function.
		"""
		with open(output_file, 'w') as file:
			for userid, average in self.user_averages:
				file.write("{},{}\n".format(userid, average))



if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("log_file",
						help="path to log file to be processed",
						type=str)
	parser.add_argument("output_file",
						help="path to output csv",
						type=str)
	# optional default_session argument
	parser.add_argument("-d", "--default_session",
						default=None,
                    	help="optional default session length for log errors.")
	
	args = parser.parse_args()

	# if default_session string is a digit, transform to int
	if args.default_session != None and args.default_session.isdigit() == True:
		args.default_session == int(args.default_session)
	
	# process averages in log file
	ap = AverageProcessor(default_session=args.default_session)
	results = ap.process(args.log_file)

	# output to csv
	ap.to_csv(args.output_file)

