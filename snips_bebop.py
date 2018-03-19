import json
# https://github.com/snipsco/snips-platform-documentation/tree/master/python
import paho.mqtt.client as mqtt
import sys
from uavBebop import uavBebop

# Boolean to debug things, set to True in production
with_drone = True
with_mqtt = True


# MQTT client to connect to the bus
if with_mqtt: mqtt_client = mqtt.Client()

uav = uavBebop()

def on_connect(client, userdata, flags, rc):
   '''
   Listning to the MQTT bus
   '''
   mqtt_client.subscribe('hermes/intent/trancept:BebopFly')


def on_message(client, userdata, msg):
    '''
    # Process a message as it arrives
    '''
    # Read Snips Payload
    print(msg.payload)
    json_data = msg.payload.decode('utf-8')
    slots = parse_slots(json.loads(json_data))
    session_id = parse_session_id(json_data)
    if 'Action' not in slots:
        say("I don't know where I should go.", session_id)
    else:
        action = slots['Action']
        say('OK, I will {} my lord.'.format(action), session_id)
        make_move(action, session_id = session_id)
        say("MakeMove Done")


def parse_session_id(msg):
    '''
    Extract the session id from the message
    '''
    data = json.loads(msg)
    return data['sessionId']


def say(text, session_id = 0):
    '''
    Print the output to the console and to the TTS engine and keep dialog session open
    '''
    print(text)
    if with_mqtt: mqtt_client.publish('hermes/dialogueManager/continueSession', json.dumps({'text': text, "sessionId" : session_id}))

def say_and_end_session(session_id, text):
    '''
    Print the output to the console and to the TTS engine and end the dialogue session
    '''
    print(text)
    if with_mqtt: mqtt_client.publish('hermes/dialogueManager/endSession', json.dumps({'text': text, "sessionId" : session_id}))

def make_move(action, distance=1, session_id = 0):
    global uav
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
    stop
    come back, return to launch
    dance, show me
    '''
    if action == 'takeoff':
        say("Taking off")
        uav.takeoff()
        #uav.land()
    elif action == 'land':
        say("Landing")
        uav.land()
        uav.disconnect()
        sys.exit(0)
    elif action == 'left':
        #say('Going {} for {} meters.'.format(action, distance))
        uav.roll(-10, distance)
    elif action == 'right':
        print("Going ", action, " for ", distance, " meters.")
        uav.roll(10, distance)
    elif action == 'up':
        print("Going ", action, " for ", distance, " meters.")
        uav.throttle(10, distance)
    elif action == 'down':
        print("Going ", action, " for ", distance, " meters.")
        uav.throttle(-10, distance)
    elif action == 'backward':
        print("Going ", action, " for ", distance, " meters.")
        uav.pitch(-10, distance)
    elif action == 'forward':
        print("forward")
        uav.pitch(10, distance)
    elif action == 'left turn':
        print("Going ", action, " for ", distance, " meters.")
        uav.yaw(-10, distance)
    elif action == 'right turn':
        print("Going ", action, " for ", distance, " meters.")
        uav.yaw(10, distance)
    elif action == 'stop':
        print("Stop move")
        uav.stop()
    elif action == 'come back':
        say("RTL Not implemented.")
    elif action == 'dance':
        print("Going ", action, " for you baby.")
        uav.test_move()
    else:
        if with_drone: bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=1)
        print('ERROR : action ', action, ' unknown !')

def parse_slots(msg):
    '''
    We extract the slots as a dict
    '''
    #data = json.loads(msg) # .payload
    data = msg
    return dict((slot['slotName'], slot['rawValue']) for slot in data['slots'])

def unit_test():
    with open('./snips_config/takeoff.json') as json_data:
        msg = json.load(json_data)
        #print(msg)
        slots = parse_slots(msg)
        #print(slots)
        #print(slots['Action'])
        make_move(slots['Action'])

    with open('./snips_config/move.json') as json_data:
        msg = json.load(json_data)
        #print(msg)
        slots = parse_slots(msg)
        #print(slots)
        #print(slots['Action'])
        make_move(slots['Action'], slots['distance'])

if __name__ == '__main__':
  if with_mqtt:
    if with_drone:
      uav.allow_flight()
      print("Connecting to Bebop")
      success = uav.connect()
      print(success)
    else:
      print("INFO : Debug mode : no Bebop connection !")
    print("Connecting to MQTT Snips queue...")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect('localhost', 1883)
    print("Waiting for mqtt message")
    mqtt_client.publish('hermes/tts/say', json.dumps({'text': 'Ready to fly !'}))
    mqtt_client.loop_forever()
  else:
    print("INFO Unit test : no drone and no MQTT")
    unit_test()
