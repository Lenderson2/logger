import nose.tools as n
from logProcessor import logProcessor


# unit test cases

# proper initialization
def test_init_time_sessions():
	lp = logProcessor()
	actual = None
	message = "lp.time_sessions: {}. Should be {}.".format(
		lp.time_sessions, actual)
	n.assert_equal(lp.time_sessions, actual, message)

def test_init_averages():
	lp = logProcessor()
	actual = None
	message = "lp.averages: {}. Should be {}.".format(lp.averages, actual)
	n.assert_equal(lp.averages, actual, message)

# process
def test_process():
	lp = logProcessor()
	lp.process('test.log')
	actual = {
		'1': 3160,
		'2': 4924,
		'3': 5486,
		'4': 4777
	}
	message = "result averages: {}. should be: {}".format(lp.averages, actual)
	n.assert_equal(lp.averages, actual, message)

# collect total time and sessions
def test_collect_time_sessions():
	lp = logProcessor()
	c = dict()
	with open('test.log', 'r') as f:
		for record in f:
			c = lp.collect_time_sessions(c, record)
	
	actual = {
		'1': [6320, 2, 1435466775, 'close'],
		'2': [4924, 1, 1435462567, 'close'], 
		'3': [5486, 1, 1435464398, 'close'], 
		'4': [4777, 1, 1435465122, 'close']
	}
	message = "result time_sessions: {}. Should be: {}".format(c, actual)
	n.assert_equal(c, actual, message)



# collect averages
# def test_collect_averages():
# 	lp = logProcessor()
# 	c = {
# 		'1': [6320, 2, 1435466775, 'close'],
# 		'3': [5486, 1, 1435464398, 'close'],
# 		'2': [4924, 1, 1435462567, 'close'],
# 		'4': [4777, 1, 1435465122, 'close']
# 	}
# 	averages = dict()
# 	lp.test_collect_averages
# 	actual = {
# 		'1': 3160,
# 		'2': 5486,
# 		'3': 4924,
# 		'4': 4777
# 	}
# 	message = "result averages: {}. should be: {}".format(averages, actual)
# 	n.assert_equal(averages, actual, message)

# read file too great for memory

# to_csv

# to list

# read file in memory

