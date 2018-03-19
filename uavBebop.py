#from pyparrot.Bebop import Bebop
import sys
sys.path.insert(0, sys.path[0]+'/pyparrot')

from Bebop import Bebop

class uavBebop:
    """A simple example class"""
    with_drone = False
    bebop = Bebop()
    timeout = 5
    speed_factor = 1
    print_trace = True

    def connect(self):
        if self.with_drone:
            return self.bebop.connect(10)
        else:
            print("No connection because you are in 'no drone' mode. Call allow_flight()")

    def disconnect(self):
        if self.with_drone:
            return self.bebop.disconnect()

    def arm(self):
        print("TODO : arming")

    def disarm(self):
        print("TODO : disarming")

    def takeoff(self):
        self.debug("Going to takeoff")
        if self.with_drone: self.bebop.safe_takeoff(self.timeout)

    def land(self):
        self.debug("Going to land")
        if self.with_drone: self.bebop.safe_land(self.timeout)

    def roll(self, speed, distance):
        self.debug("Going to roll {} for {}".format(speed, distance))
        if self.with_drone: self.bebop.fly_direct(roll=speed*self.speed_factor, pitch=0, yaw=0, vertical_movement=0, duration=distance)

    def pitch(self, speed, distance):
        if self.with_drone: self.bebop.fly_direct(roll=0, pitch=speed*self.speed_factor, yaw=0, vertical_movement=0, duration=distance)

    def yaw(self, speed, distance):
        if self.with_drone: self.bebop.fly_direct(roll=0, pitch=0, yaw=speed*self.speed_factor, vertical_movement=0, duration=distance)

    def throttle(self, speed, distance):
        if self.with_drone: self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=speed*self.speed_factor, duration=distance)

    def stop(self):
        if self.with_drone: self.bebop.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=0, duration=distance)

    def return_to_launch(self):
        print("ERROR : RTL Not implemented.")

    def test_move(self):
        if self.with_drone:
            distance = 1
            self.roll(-10, distance)
            self.throttle(10, distance)
            self.pitch(10, distance)
            self.roll(10, distance)
            self.throttle(-10, distance)
            self.pitch(-10, distance)

    def allow_flight(self):
        self.with_drone = True

    def set_speed_factor(self, speed_factor):
        self.speed_factor = speed_factor

    def debug(self, msg):
        if self.print_trace:
            print(msg)

if __name__ == '__main__':
    uav = uavBebop()
    #uav.allow_flight()
    uav.connect()
    uav.arm()
    uav.takeoff()
    uav.test_move()
    uav.land()
    uav.disarm()
    uav.disconnect()
