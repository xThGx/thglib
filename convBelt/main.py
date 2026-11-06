import time
import keyboard as kb
import random

class Motor:
    def __init__(self, name):
        self.name: str = name
        self.status: bool = False

    def on(self):
        if not self.status:
            print("Motor turned on")
        self.status = True
        
    def off(self):
        if self.status:
            print("Motor turned off")
        self.status = False
class Cylinder:
    def __init__(self, name):
        self.name: str = name
        self.status: bool = False
        self.tON = TON(0.5)

    def home(self):
        if self.status:
            print("Cylinder moved to home pos")
            print("-" * 50)
        self.status = False

    def work(self):
        if not self.status:
            print("Cylinder moved to work pos")
        self.status = True
class Sensor:
    def __init__(self, name):
        self.name: str = name
        self.status: bool = False

    def partDetected(self):
        if not self.status:
            print("part detected")
        self.status = True

    def partGone(self):
        if self.status:
            print("part gone")
        self.status = False
class TON():
    def __init__(self, preset: float):
        self.preset: float = preset
        self._start = None

    def update(self, IN: bool) -> bool:
        if not IN:
            self._start = None
            return False
        if self._start is None:
            self._start = time.monotonic()
        return self.elapsed() >= self.preset

    def elapsed(self) -> float:
        if self._start is None:
            return 0.0
        return time.monotonic() - self._start


def readStatus(sensor: Sensor, motor: Motor, cylinder: Cylinder):
    '''returns the sensor status'''
    if bool(random.getrandbits(1)) and motor.status:
        print("=" * 50)
        sensor.partDetected() 
    return sensor.status, motor.status, cylinder.status


def writeOutputs(sensor: Sensor, motor: Motor, cylinder: Cylinder):
    '''returns the status after executing steps'''
    if not sensor.status and not cylinder.status:
        motor.on()
    else:
        motor.off()
        cylinder.work()
        sensor.partGone()
        
    return sensor.status, motor.status, cylinder.status


def main():
    sensor = Sensor("PartAtCylinder")
    motor = Motor("ConveyorMotor")
    cylinder = Cylinder("PusherCylinder")
    machineRuns: bool = False
    runTime = TON(0)
    cycleTime = TON(0)
    cycleTimeOn = False
    lastCycleTime = .0
    refreshTimer = TON(2)
    refresh = False
    
    print("To start the machine, press 'r'. To stop the machine, press 's'.\n")

    while True:
        if kb.is_pressed('r'):
            machineRuns:bool = True
            print("Machine started.")
            while kb.is_pressed('r'):
                pass  # warten bis losgelassen
        if kb.is_pressed('s'):
            machineRuns: bool = False
            motor.off()
            print("Machine stopped.")
            while kb.is_pressed('s'):
                pass  # warten bis losgelassen
        if kb.is_pressed('i'):
            print(f"Sensor: {sensor.status}, Motor: {motor.status}, Cylinder: {cylinder.status}")
            print(f"Run time: {float(runTime.elapsed()):.2f}")
            print(f"Cycle time: {float(cycleTime.elapsed()):.2f}, Last Cycle: {lastCycleTime:.2f}")
            while kb.is_pressed('i'):
                pass  # warten bis losgelassen
        if kb.is_pressed('esc'):
            print("shutting down")
            time.sleep(.5)
            break

        refresh = refreshTimer.update(not refresh)

        runTime.update(machineRuns)
        if machineRuns and refresh:
            readStatus(sensor, motor, cylinder)
            writeOutputs(sensor, motor, cylinder)
        
        if machineRuns:
            if cylinder.tON.update(cylinder.status):
                cylinder.home()
        if motor.status:
            cycleTimeOn = True
        if not sensor.status and not cylinder.status and not motor.status:
            cycleTimeOn = False
        
        if cycleTime.elapsed() != lastCycleTime and cycleTime.elapsed() > 0 and not cycleTimeOn:
            lastCycleTime = cycleTime.elapsed()
            print("*" *50)
            print()
            print(f"Last Cycle took {lastCycleTime:.2f}sec")
            print()
            print("*" *50)
        cycleTime.update(cycleTimeOn)

        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
