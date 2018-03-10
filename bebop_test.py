"""
Demo the Bebop indoors (takes off, turns about 90 degrees, lands)
Note, the bebop will hurt your furniture if it hits it.  Be sure you are doing this in an open area
and are prepared to catch!
"""
import sys
# Import sub-module 'pyparrot'
sys.path.insert(0, sys.path[0]+'/pyparrot')
from Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

if (success):
    #print("turning on the video")
    #bebop.start_video_stream()

    print("sleeping")
    bebop.smart_sleep(2)

    bebop.ask_for_state_update()

    bebop.safe_takeoff(5)

    print("Flying direct: yaw SLOWLY for indoors")
    # Yaw positif droite
    #bebop_direct(roll=0, pitch=0, yaw=40, vertical_movement=0, duration=3)
    # roll positif  droite
    bebop.fly_direct(roll=10, pitch=0, yaw=0, vertical_movement=0, duration=1)
    bebop.fly_direct(roll=-10, pitch=0, yaw=0, vertical_movement=0, duration=1)
    # Pitch positif  avant
    bebop.fly_direct(roll=0, pitch=10, yaw=0, vertical_movement=0, duration=1)
    bebop.fly_direct(roll=0, pitch=-10, yaw=0, vertical_movement=0, duration=1)
    # Vertical positif 
    bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-10, duration=1)
    bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=10, duration=1)

    bebop.smart_sleep(1)
    bebop.safe_land(5)

    print("DONE - disconnecting")
    #bebop.stop_video_stream()
    bebop.smart_sleep(5)
    bebop.disconnect()


