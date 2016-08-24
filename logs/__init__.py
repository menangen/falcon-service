import sys
from logbook import Logger, StreamHandler, RotatingFileHandler, TimedRotatingFileHandler

# Enable logging to File
# Based on File Size:

# log_to_file = RotatingFileHandler('logs/service.log', max_size=1048576, backup_count=3)

# Based on Date:
# log_to_file = TimedRotatingFileHandler('logs/service.log', date_format='%d-%m-%Y', backup_count=15)

# log_to_file.push_application()

# Enable logbook logger Stream to output
StreamHandler(sys.stdout).push_application()

request = Logger('FormResource [Request.stream.read]')
response = Logger('FormResource [Response.body]')

data_validator = Logger('Data processing [Validate]')
data_transaction = Logger('Data processing [Transaction]')