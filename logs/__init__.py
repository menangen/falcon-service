import sys
from logbook import Logger, StreamHandler, FileHandler

# Enable logging to File
# log_to_file = FileHandler('logs/service.log')
# log_to_file.push_application()

# Enable logbook logger Stream to output
StreamHandler(sys.stdout).push_application()

log_request = Logger('FormResource:request.stream.read')
log_response = Logger('FormResource:response.body')