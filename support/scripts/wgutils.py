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


	def save_excel(self, df, filename):
		# force using openpyxl
		filepath = os.path.join(self.dir, filename + '.xlsx')
		df.to_excel(filepath)
		tracelog("Excel file written at " + filepath)

def get_secrets():
	return os.path.join(os.environ['PROJECT_ROOT'], 'config', 'secrets.json')

def tracelog (msg, kind='P'):
	prefix = '['+kind+'] '
	timelog = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
	print (prefix + timelog + ': ' + msg)
