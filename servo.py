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
