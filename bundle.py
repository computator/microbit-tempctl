class Servo:
    def _calc_duty(self, val):
        return float(val) / (self._cycle_ms * 1000) * 1023

    def __init__(self, pin, min_us=1000, max_us=2000, cycle_ms=20):
        self.pin = pin

        self._cycle_ms = max(5, min(cycle_ms, 300))
        self._d_min = self._calc_duty(max(300, min_us))
        self._d_max = self._calc_duty(min(max_us, 3000))

        self._on = False
        self._pos = 90

        # turn off the pin so we aren't sending an initial position
        self.stop()

    def stop(self):
        self.pin.write_digital(0)
        self._on = False

    def start(self):
        self.pin.set_analog_period(self._cycle_ms)
        self._on = True
        self._update()

    def pos(self, angle):
        self._pos = max(0, min(angle, 180))
        if self._on:
            self._update()

    def _update(self):
        duty = self._d_min + (self._d_max - self._d_min) * ((180 - self._pos) / 180)
        self.pin.write_analog(duty)

    def calibration(self, min_us, max_us, cycle_ms=20):
        self._cycle_ms = max(5, min(cycle_ms, 300))
        self._d_min = self._calc_duty(max(300, min_us))
        self._d_max = self._calc_duty(min(max_us, 3000))
        if self._on:
            self._update()
from microbit import display
from microbit import pin0
from microbit import button_a, button_b
from microbit import temperature
from microbit import sleep
    
def disp(val):
    return display.scroll(str(val), 100, wait=False)

# farenheight temperature
temperature_f = lambda: temperature() * (9 / 5) + 32


A_HEAT = 140
A_COOL = 20
T_RNG = 2
T_OFFSET = -10

tmp = 70
last_tmp = tmp
last_pos = 90

srv = Servo(pin0, 440, 2240)
srv.pos(last_pos)
srv.start()
sleep(1000)
srv.stop()

def update_pos(curr_tmp):
    global last_pos
    min_tmp = tmp - T_RNG
    # calclate offet into the temp range
    tmp_offset = max(0, min(curr_tmp - min_tmp, T_RNG * 2))
    pos = (A_HEAT - A_COOL) * (tmp_offset / (T_RNG * 2)) + A_COOL
    print("T Offset: {}\nPos: {}\n".format(tmp_offset, pos))
    if pos != last_pos:
        srv.pos(pos)
        srv.start()
        sleep(1000)
        srv.stop()
        last_pos = pos

disp(temperature_f() + T_OFFSET)

loops = 0
while True:
    offset = button_b.get_presses() - button_a.get_presses()
    if offset != 0:
        tmp = max(50, min(tmp + offset, 100))
        print("Chg: {}\nNew T: {}\n".format(offset, tmp))
        disp(tmp)
        update_pos(temperature_f() + T_OFFSET)
        loops = 0
        continue

    loops = (loops + 1) % 50 # 0.200s * 50 = 10s
    if loops == 0:
        curr_tmp = temperature_f() + T_OFFSET
        if curr_tmp != last_tmp:
            update_pos(curr_tmp)
            last_tmp = curr_tmp
        print("Tmp: {}".format(curr_tmp))
        disp(curr_tmp)

    sleep(200)
