import machine

class Button:
    """Debounced Button
    Uses internal state to debounce button in software.
    """
    def __init__(self, pin, checks=3, check_period=20):
        self.pin = pin
        self.pin.irq(handler=self._switch_change,
                     trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)

        self.debounce_timer = machine.Timer(-1)
        self.value = None
        self.prev_value = None
        self.debounce_checks = 0
        self.checks = checks
        self.check_period = check_period
        self.on_pressed_cb = set()
        self.on_released_cb = set()

    def register_for_pressed(self, cb):
        self.on_pressed_cb.add(cb)

    def register_for_released(self, cb):
        self.on_released_cb.add(cb)

    def _switch_change(self, pin):
        self.value = pin.value()
        self.debounce_checks = 0
        self._start_debounce_timer()
        # Disable IRQs
        self.pin.irq(trigger=0)

    def _start_debounce_timer(self):
        self.debounce_timer.init(period=self.check_period, mode=machine.Timer.ONE_SHOT,
                                 callback=self._check_debounce)

    def _check_debounce(self, _):
        new_value = self.pin.value()

        if new_value == self.value:
            self.debounce_checks = self.debounce_checks + 1

            if self.debounce_checks == self.checks:
                # Values are the same, debouncing done
                if self.prev_value != new_value:
                    self.prev_value = new_value
                    if new_value:
                        for cb in self.on_released_cb:
                            cb()
                    else:
                        for cb in self.on_pressed_cb:
                            cb()
                # Reenable the Switch IRQ
                self.pin.irq(handler=self._switch_change,
                             trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
            else:
                self._start_debounce_timer()
        else:
            self.debounce_checks = 0
            self.value = new_value
            self._start_debounce_timer()
