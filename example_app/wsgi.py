import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/root/customer-account-automation/")

from app import app as application
app = application
application.run()