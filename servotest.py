from microbit import display
from microbit import pin0
from microbit import button_a, button_b
from microbit import sleep
from servo import Servo
    
def disp(val):
    return display.scroll(str(val), 60, wait=False)

pos = 90
srv = Servo(pin0, 440, 2240)

srv.pos(pos)
srv.start()
disp(pos)

while True:
    # constrain offset to be: 10 >= offset <= -10
    offset = max(-10, min(10, button_b.get_presses() - button_a.get_presses()))
    if offset != 0:
        newpos = max(0, min(pos + offset * 30, 180))
        print("Offset: {}\nNewpos: {}\n".format(offset, newpos))
        if newpos != pos:
            pos = newpos
            srv.pos(pos)
        disp(pos)
    sleep(200)
