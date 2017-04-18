import os
import datetime

class Session(object):
	def __init__(self, label=''):
		if not label:
			# get a default label
			label='unnamed_session'
		dir_name = datetime.datetime.now().strftime('%Y%m%dT%H%M%S') + '_' + label.lower().replace(' ', '_')
		self.dir = os.path.join(os.environ['PROJECT_ROOT'], 'output', dir_name)
		os.makedirs(self.dir)

def tracelog (msg, kind='P'):
	prefix = '['+kind+'] '
	timelog = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
	return prefix + timelog + ': ' + msg
