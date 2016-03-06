from flask import Flask
app = Flask(__name__)

import os
import sys
import rollbar
import rollbar.contrib.flask
from flask import request, got_request_exception


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        'c6393fb20bf5493bbd0cc0d667ccc863',
        'local',
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False)

    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

@app.route('/')
def index():
    print "in hello"
    x = None
    x[5]
    return "Hello World!"

@app.route('/greeting')
def greeting():
    name = request.args.get('name')
    if not name:
        rollbar.report_message('No name passed for greeting', 'warning')
        return "Hello World!"

    return "Hello {}!".format(name)

@app.route('/insult')
def insult():
    name = request.args.get('name')

    try:
        severity = int(request.args.get('severity'))
        if severity < 10:
            return "You smell, {}.".format(name)
        else:
            return "Everyone who loved you was wrong, {}.".format(name)            
    except:
        rollbar.report_exc_info(sys.exc_info(), request)
        rollbar.report_message('Severity level not an integer', 'warning', request)
        return "Unable to formulate insult; you smell poorly."


if __name__ == '__main__':
    app.run()