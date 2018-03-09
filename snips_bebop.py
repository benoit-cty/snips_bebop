import json
# https://github.com/snipsco/snips-platform-documentation/tree/master/python
import paho.mqtt.client as mqtt
# Import sub-module 'pyparrot'
import sys
sys.path.insert(0, sys.path[0]+'/pyparrot')
from Bebop import Bebop
bebop = Bebop()

# Boolean to debug things, set to True in production
with_drone = False
with_mqtt = True

# MQTT client to connect to the bus
if with_mqtt: mqtt_client = mqtt.Client()



# Subscribe to the important messages
def on_connect(client, userdata, flags, rc):
   '''
   hermes/intent/trancept:BebopFly: b'{"sessionId":"96f371a0-64f0-47d5-8ea7-3075e0bc375f","customData":null,"siteId":"default","input":"up","intent":{"intentName":"trancept:BebopFly","probability":1.0},"slots":[{"rawValue":"up","value":{"kind":"Custom","value":"up"},"range":{"start":0,"end":2},"entity":"FlyAction","slotName":"Action"}]}'
   '''
   mqtt_client.subscribe('hermes/intent/trancept:BebopFly')

# Process a message as it arrives
def on_message(client, userdata, msg):
    # Read Snips Payload
    print(msg.payload)
    json_data = msg.payload.decode('utf-8')
    slots = parse_slots(json.loads(json_data))
    session_id = parse_session_id(json_data)
    if 'Action' not in slots:
        say(session_id, "I don't know where I should go.")
    else:
        action = slots['Action']
        say(session_id, 'OK, I will {} my lord.'.format(action))
        make_move(action)


def parse_session_id(msg):
    '''
    Extract the session id from the message
    '''
    data = json.loads(msg)
    return data['sessionId']

def say(session_id, text):
    '''
    Print the output to the console and to the TTS engine
    '''
    print(text)
    mqtt_client.publish('hermes/dialogueManager/endSession', json.dumps({'text': text, "sessionId" : session_id}))

def make_move(action, distance=None):
    timeout = 5
    '''
    land,
    take off, takeoff
    left,
    right,
    up, climb
    down
    right turn, yaw right
    left turn, yaw left
    forward, front
    backward, back
    stop, no, oh my god, fuck, abort
    come back, return to launch
    dance, show me
    '''
    if action == 'takeoff':
        print("Taking off")
        if with_drone: bebop.safe_takeoff(timeout)
    elif action == 'land':
        print("Landing")
        if with_drone: bebop.safe_land(timeout)
    elif action == 'left':
        print("Going ", action, " for ", distance, " meters.")
        if with_drone: bebop.fly_direct(roll=1, pitch=0, yaw=0, vertical_movement=0, duration=1)
    elif action == 'right':
        print("Going ", action, " for ", distance, " meters.")
    elif action == 'up':
        print("Going ", action, " for ", distance, " meters.")
    elif action == 'down':
        print("Going ", action, " for ", distance, " meters.")
    elif action == 'backward':
        print("Going ", action, " for ", distance, " meters.")
    elif action == 'forward':
        print("forward")
    elif action == 'left turn':
        print("Going ", action, " for ", distance, " meters.")
    elif action == 'right turn':
        print("Going ", action, " for ", distance, " meters.")
    elif action == 'stop':
        print("Stop move")
        if with_drone: bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=5)
    elif action == 'come back':
        print("RETURN TO LAUNCH")
    elif action == 'dance':
        print("Going ", action, " for you baby.")
    else:
        if with_drone: bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=5)
        print('ERROR : action ', action, ' unknown !')


def parse_slots(msg):
    '''
    We extract the slots as a dict
    '''
    #data = json.loads(msg) # .payload
    data = msg
    return dict((slot['slotName'], slot['rawValue']) for slot in data['slots'])

def unit_test():
    with open('takeoff.json') as json_data:
        msg = json.load(json_data)
        #print(msg)
        slots = parse_slots(msg)
        #print(slots)
        #print(slots['Action'])
        make_move(slots['Action'])

    with open('move.json') as json_data:
        msg = json.load(json_data)
        #print(msg)
        slots = parse_slots(msg)
        #print(slots)
        #print(slots['Action'])
        make_move(slots['Action'], slots['distance'])

unit_test
if __name__ == '__main__' and with_mqtt:
    if with_drone:
      print("Connecting to Bebop")
      success = bebop.connect(10)
      print(success)
    else:
      print("Debug mode : no Bebop connection !")
    print("Connecting to MQTT Snips queue...")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('localhost', 1883)
    print("Waiting for mqtt message")
    mqtt_client.loop_forever()
