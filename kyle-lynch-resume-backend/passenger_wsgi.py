import sys
import os
from pathlib import Path

# Add the application directory to Python path
INTERP = os.path.join(os.environ['HOME'], '.pyenv', 'versions', '3.11.0', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Get the directory containing this file
application_dir = Path(__file__).parent
sys.path.insert(0, str(application_dir))

# Import FastAPI app
from server import app as application

# This is required for Passenger
def application(environ, start_response):
    return application(environ, start_response)
