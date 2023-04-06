from flask import Flask, abort
from datetime import datetime, timedelta, timezone
from logger import logger
from utils import get_documentation


app = Flask(__name__)

@app.route('/')
def hello():
    """return: 'Hello, World"""
    return 'Hello, World!'


@app.route('/datetime/')
@app.route('/datetime/<string:tz>')
def get_current_datetime(tz=None):
    """
    If path '/datetime/' - return current date and time in host;
    if path '/datetime/0' - return current UTF date and time;
    if path '/datetime/<num> - return date and time in timezone UTF+<num>.
    """
    tz_input = tz
    if tz:
        try:
            tz = timezone(timedelta(hours=int(tz)))
        except ValueError:
            logger.error(f'Invalid timezone {tz_input}')
            abort(406, "Timezone must be an integer from -23 to 23 ")
    time_str = datetime.now(tz=tz).strftime('Current date %d-%m-%Y and time %H:%M:%S  %z')
    logger.info(f'Successfully, timezone: {tz}')
    return time_str


@app.route('/datetime')
def get_description():
    logger.info(f'Review documentation')
    return get_documentation(get_current_datetime)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

