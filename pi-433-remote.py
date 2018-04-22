from flask import Flask, render_template
from subprocess import call

app = Flask(__name__)

SENDER_CONFIG = '10101'
SEND_CONFIG = ['-u', '-s']
RECEIVER = {
    'A': '1',
    'B': '2',
    'C': '3',
    'D': '4',
}
STATES = {
    'on':'1',
    'off':'0'
}

def send_signal(receiver, state):
    call(['./send', SENDER_CONFIG, *SEND_CONFIG, receiver, state])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/on/', methods=['POST'])
def on_all():
    for _, value in RECEIVER.items():
        send_signal(value, STATES['on'])
    return 'all on'

@app.route('/off/', methods=['POST'])
def off_all():
    for _, value in RECEIVER.items():
        send_signal(value, STATES['off'])
    return 'all off'

@app.route('/receiver/<receiver_id>/<state_id>/', methods=['POST'])
def switch(receiver_id, state_id):
    if receiver_id not in RECEIVER.keys():
        return '{} not in {}'.format(receiver_id, RECEIVER.keys()), 400
    elif state_id not in STATES.keys():
        return '{} not in {}'.format(state_id, STATES.keys()), 400
    else:
        send_signal(RECEIVER[receiver_id], STATES[state_id])
        return '{} {}'.format(receiver_id, state_id)


