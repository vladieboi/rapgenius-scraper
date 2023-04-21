import logging
from datetime import datetime

# Define console class used for printing colored timestamped messages
class console:
	def timestamp():
		return datetime.now().strftime('%H:%M:%S.%f')[:-4]

	def print(message, color=''):
		print(f'[{console.timestamp()}] {color}{str(message)}{console.ENDC}')

	HEADER    = '\033[95m'
	OKBLUE    = '\033[94m'
	OKGREEN   = '\033[92m'
	WARNING   = '\033[93m'
	FAIL      = '\033[91m'
	BOLD      = '\033[1m'
	UNDERLINE = '\033[4m'
	ENDC      = '\033[0m'

# Define logger class used for logging events to a log file set on line :67
class logger:
	logging.basicConfig(filename=f'result.log', filemode='w', level=logging.INFO, format='%(asctime)s § %(name)-24s § %(filename)-24s § %(threadName)-24s § %(lineno)-7s § %(levelname)-8s § %(message)s', datefmt='%Y-%m-%d %T%Z')
	
	def start(filename='result.log', level=logging.INFO, loggername='rapgenius.logger'):
		logger = logging.getLogger(loggername); logger.setLevel(level)
		assert logger.parent == logging.root
		return logger

logger = logger.start()