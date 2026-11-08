import time
import keyboard as kb
import random
import os

class Machine():
    def __init__(self):
        self.runs = False
        self.shutdown = False
        self.eStopOk = False
        self.safetyOk = False
        self.ems_quit = False
        self.ack = False
        self.door_quit = False
        self.tim = TON(preset = 0)
        self.lastCT = TON(preset = 0)
        self.ref = TON(preset = 2)
        self.runtime = TON(preset = 0)
        self.motor = Motor("ConveyorMotor")
        self.sensor = Sensor("PartAtCylinder")
        self.cylinder = Cylinder("PusherCylinder")


class Drives():
    def __init__(self, name: str, status: bool = False, dir: str = "cw", acc: float = 100, dcc: float = 100, speed: float = 200):
        super().__init__()
        self.name = name
        self.status = status
        self.dir = dir
        self.acc = acc
        self.dcc = dcc
        self.speed = speed
class Motor(Drives):
    def __init__(self, name: str, status = False, dir = "cw", acc = 100, dcc = 100, speed: float = 200):
        super().__init__(name, status, dir, acc, dcc, speed)


    def setOn(self, release):
        if not release:
            print(f"{self.name}: no release to turn on")
            self.setOff()
            return
        if not self.status:
            print("Motor turned on")
        self.status = True
    def setOff(self):
        if self.status:
            print("Motor turned off")
        self.status = False
class Cylinder():
    def __init__(self, name):
        self.name: str = name
        self.status: bool = False
        self.tON = TON(0.5)

    def setHome(self, release):
        if not release:
            print(f"{self.name}: release is missing")
            return
        if self.status:
            print("Cylinder: HP")
            print("-" * 50)
        self.status = False
    def setWork(self, release):
        if not release:
            print(f"{self.name}: release is missing")
            return
        if not self.status:
            print("Cylinder WP")
        self.status = True
class Sensor:
    def __init__(self, name):
        self.name: str = name
        self.status: bool = False

    def setPartDetected(self):
        if not self.status:
            print("part detected")
        self.status = True

    def setPartGone(self):
        if self.status:
            print("part gone")
        self.status = False
class Timer():
    def __init__(self):
        self.preset: float = 0
        self._start = None
class TON(Timer):
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


def readStatus(m: Machine):
    '''returns the sensor status'''
    if m.sensor.status and not m.cylinder.status:
        m.sensor.setPartGone()
    if bool(random.getrandbits(1)) and m.motor.status:
        print("=" * 50)
        m.sensor.setPartDetected()
    return m.sensor.status, m.motor.status, m.cylinder.status


def writeOutputs(m: Machine):
    '''returns the status after executing steps'''
    if not m.sensor.status and not m.cylinder.status:
        m.motor.setOn(m.safetyOk and m.eStopOk)
    else:
        m.motor.setOff()
        m.cylinder.setWork(m.eStopOk and m.safetyOk)
        m.sensor.setPartGone()
    return m.sensor.status, m.motor.status, m.cylinder.status


def header(sign, msg:str) -> str:
    prefix = sign * 50
    suffix = sign * 50
    print(f"{prefix}\n{msg}\n{suffix}")
    return f"{prefix}\n{msg}\n{suffix}"


def setEMS(m: Machine):
    m.runs = False
    m.eStopOk = False
    print("E-Stop pressed!")
    m.motor.setOff()

def setEMS_Quit(m: Machine):
    if not m.safetyOk:
        print("Quit the doors first")
        return
    if not m.eStopOk and m.safetyOk and m.ems_quit:
        m.eStopOk = True
        print("EMS quit impulse")
def setDoors_Quit(m: Machine):
    if not m.safetyOk and m.door_quit:
        m.safetyOk = True
        print("Door Quit impulse")

def handleSafety(m: Machine):
    if kb.is_pressed("q"):
        m.ems_quit = True
        setEMS_Quit(m)
        while kb.is_pressed("q"):
            pass
        if m.ems_quit:
            m.ems_quit = False
    if kb.is_pressed("d"):
        m.door_quit = True
        setDoors_Quit(m)
        while kb.is_pressed("d"):
            pass
        if m.safetyOk:
            m.door_quit = False
    if kb.is_pressed("o"):
        setEMS(m)
        while kb.is_pressed("o"):
            pass
    
def getCT(m: Machine, cycleTimeOn, lastCycleTime):
    if m.tim.elapsed() != lastCycleTime and m.tim.elapsed() > 0 and not cycleTimeOn:
        lastCycleTime = m.tim.elapsed()
        header("*", f"Last Cycle took {lastCycleTime:.2f}sec")
    m.tim.update(cycleTimeOn)
    #return lastCycleTime
def handleKeys(m: Machine):
    if kb.is_pressed('r'):
        while kb.is_pressed("r"):
            pass
        if not m.eStopOk or not m.safetyOk:
            print("Start not allowed check safety first")
            print(f"EMS status: {"OK" if m.eStopOk else "NOK"}")
            print(f"Door status: {"OK" if m.safetyOk else "NOK"}")
            return
        if not m.runs:
            header("=", "Machine runs")
        m.runs = True
    if kb.is_pressed('s'):
        while kb.is_pressed('s'):
            pass  # warten bis losgelassen
        if m.runs:
            header("=", "Machine stopped")
        m.runs = False
        m.motor.setOff()

    if kb.is_pressed('i'):
        print(f"Sensor: {m.sensor.status}, Motor: {m.motor.status}, Cylinder: {m.cylinder.status}")
        print(f"Run time: {float(m.tim.elapsed()):.2f}")
        print(f"Safety status: EMS = {"OK" if m.eStopOk else "NOK"}, Door status = {"OK" if m.safetyOk else "NOK"}")
        #print(f"Cycle time: {float(m.tim.elapsed()):.2f}, Last Cycle: {lastCycleTime:.2f}")
        while kb.is_pressed('i'):
            pass  # warten bis losgelassen
    if kb.is_pressed("c"):
        while kb.is_pressed("c"):
            pass
        os.system("cls")
    if kb.is_pressed('esc'):
        print("shutting down")
        m.shutdown = True
        time.sleep(.5)


def main():
    # put all the global variables before the main loop 
    m = Machine()
    # sensor = Sensor("PartAtCylinder")
    # motor = Motor("ConveyorMotor")
    # cylinder = Cylinder("PusherCylinder")
    #machineRuns: bool = m.runs
    refresh: bool = False
    cycleTimeOn: bool = False
    lastCycleTime: float = .0
    print("Check Safety before you start ('d' - door quit / 'q' - EMS quit)")
    print("To start the machine, press 'r'. To stop the machine, press 's'.\n")

    while True:
        handleSafety(m)
        handleKeys(m)
        if m.shutdown:
            break
        machineRuns = m.runs

        refresh = m.ref.update(not refresh)

        m.runtime.update(machineRuns)
        if machineRuns and refresh:
            readStatus(m)
            writeOutputs(m)
        
        if machineRuns:
            if m.cylinder.tON.update(m.cylinder.status):
                m.cylinder.setHome(m.eStopOk and m.safetyOk)
        if m.motor.status:
            cycleTimeOn = True
        if not m.sensor.status and not m.cylinder.status and not m.motor.status:
            cycleTimeOn = False
        getCT(m, cycleTimeOn, lastCycleTime)


        time.sleep(0.01)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
