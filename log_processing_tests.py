import nose.tools as n
from log_processing import AverageProcessor


# unit test cases

# process
def test_process():
	ap = AverageProcessor()
	result = sorted(ap.process('data/test.log'), key=lambda x: x[0])
	actual = [
		('1', 3160),
		('2', 4924),
		('3', 5486),
		('4', 4777)
	]
	message = "result averages: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# _calc_averages
def test_calc_averages():
	ap = AverageProcessor()
	user_totals = {
		'1': [6320, 2],
		'3': [5486, 1],
		'2': [4924, 1],
		'4': [4777, 1]
	}
	result = sorted(ap._calc_averages(user_totals), key=lambda x: x[0])
	actual = [
		('1', 3160),
		('2', 4924),
		('3', 5486),
		('4', 4777)
	]
	message = "result averages: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# _parse_line
def test_parse_line():
	ap = AverageProcessor()
	line = "2,1435457643,open\n"
	result = ap._parse_line(line)
	actual = ('2', 1435457643, 'open')
	message = "result variables: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# _calc_session_length
# with close, open sequence
def test_calc_session_length_open_close():
	ap = AverageProcessor()
	time = 1435459567
	action = 'close'
	last_time = 1435456566
	last_action = 'open'
	user_totals = None
	userid = None
	result = ap._calc_session_length(
		time, action, last_time, last_action, user_totals, userid)
	actual = 1435459567 - 1435456566
	message = "result session length: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# with non applicable sequence
def test_calc_session_length_close_close():
	ap = AverageProcessor()
	time = 1435459567
	action = 'close'
	last_time = 1435456566
	last_action = 'close'
	user_totals = None
	userid = None
	result = ap._calc_session_length(
		time, action, last_time, last_action, user_totals, userid)
	actual = 0
	message = "result session length: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# with default_session int
def test_calc_session_length_default_session_int():
	ap = AverageProcessor(default_session=24)
	time = 1435459567
	action = 'close'
	last_time = 1435456566
	last_action = 'close'
	user_totals = None
	userid = None
	result = ap._calc_session_length(
		time, action, last_time, last_action, user_totals, userid)
	actual = 24*60
	message = "result session length: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# with default_session average
def test_calc_session_length_default_session_average():
	ap = AverageProcessor(default_session='average')
	time = 1435459567
	action = 'close'
	last_time = 1435456566
	last_action = 'close'
	user_totals = {'123': [1000, 2]}
	userid = '123'
	result = ap._calc_session_length(
		time, action, last_time, last_action, user_totals, userid)
	actual = float(user_totals[userid][0])/user_totals[userid][1]
	message = "result session length: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)