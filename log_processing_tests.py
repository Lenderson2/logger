import nose.tools as n
from log_processing import AverageProcessor


# unit test cases

# process
def test_process():
	ap = AverageProcessor()
	result = sorted(ap.process('test.log'), key=lambda x: x[0])
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
	# result = ap._calc_averages(user_totals)
	actual = [
		('1', 3160),
		('2', 4924),
		('3', 5486),
		('4', 4777)
	]
	message = "result averages: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# _get_fields_from_line
def test_get_fields_from_line():
	ap = AverageProcessor()
	line = "2,1435457643,open\n"
	result = ap._get_fields_from_line(line)
	actual = ('2', 1435457643, 'open')
	message = "result variables: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# _calc_session_length
# Without max_session
def test_calc_session_length():
	ap = AverageProcessor()
	time = 1435459567
	last_time = 1435456566
	result = ap._calc_session_length(time, last_time)
	actual = time - last_time
	message = "result session length: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)

# With max_session
def test_calc_session_length_max_session():
	ap = AverageProcessor(max_session=30)
	time = 1435459567
	last_time = 1435456566
	result = ap._calc_session_length(time, last_time)
	actual = 30*60
	message = "result session length: {}. should be: {}".format(result, actual)
	n.assert_equal(result, actual, message)