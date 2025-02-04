from microbit import display
from microbit import pin0
from microbit import button_a, button_b
from microbit import temperature
from microbit import sleep
from servo import Servo
    
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
