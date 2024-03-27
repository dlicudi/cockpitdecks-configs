---
layout: default
title: Encoder Value
parent: Experimental
has_children: false
nav_order: 6
---

# Encoder Value Extended

Based on existing EncoderValue class

```
class EncoderValueExtended(OnOff):
    """
    Activation that maintains an internal value and optionally write that value to a dataref
    """

    def __init__(self, config: dict, button: "Button"):
        self.step = float(config.get("step", 1))
        self.stepxl = float(config.get("stepxl", 10))
        self.value_min = float(config.get("value-min", 0))
        self.value_max = float(config.get("value-max", 100))
        self.options = config.get("options", None)

        # Internal status
        self._turns = 0
        self._cw = 0
        self._ccw = 0
        self.encoder_current_value = float(config.get("initial-value", 1))
        self._step_mode = self.step
        self._local_dataref = "data:" + config.get("dataref", None)  # local dataref to write to

        OnOff.__init__(self, config=config, button=button)

    def init(self):
        if self._inited:
            return
        value = self.button.get_current_value()
        if value is not None:
            self.encoder_current_value = value
            logger.debug(f"button {self.button_name()} initialized on/off at {self.encoder_current_value}")
        elif self.initial_value is not None:
            self.encoder_current_value = self.initial_value
            logger.debug(f"button {self.button_name()} initialized on/off at {self.onoff_current_value} from initial-value")
        if self.encoder_current_value is not None:
            self._inited = True

    def decrease(self, x):
        if self.options == "modulo":
            new_x = (x - self._step_mode - self.value_min) % (self.value_max - self.value_min + 1) + self.value_min
            return new_x
        else:
            x = x - self._step_mode
            if x < self.value_min:
                return self.value_min
            return x

    def increase(self, x):
        if self.options == "modulo":
            new_x = (x + self._step_mode - self.value_min) % (self.value_max - self.value_min + 1) + self.value_min
            return new_x
        else:
            x = x + self._step_mode
            if x > self.value_max:
                return self.value_max
            return x

    def is_valid(self):
        if self.writable_dataref is None:
            logger.error(f"button {self.button_name()}: {type(self).__name__} must have a dataref to write to")
            return False
        return super().is_valid()

    def activate(self, state):
        if state == 1:
            if self._step_mode == self.step:
                self._step_mode = self.stepxl
            else:
                self._step_mode = self.step
            self.view()
            return

        ok = False
        x = self.encoder_current_value
        if x is None:
            x = 0
        if state == 2:  # anti-clockwise
            # x = x - self._step_mode
            x = self.decrease(x)
            ok = True
            self._turns = self._turns - 1
            self._ccw = self._ccw + 1
        elif state == 3:  # clockwise
            # x = x + self._step_mode
            x = self.increase(x)
            ok = True
            self._turns = self._turns + 1
            self._cw = self._cw + 1
        elif self.has_long_press() and self.long_pressed():
            self.long_press(state)
            print('why hello again!')
            logger.debug(f"button {self.button_name()}: {type(self).__name__}: long pressed")
            return

        if ok:
            self.encoder_current_value = x
            self.write_dataref(x)

            # write to local dataref if configured
            if self._local_dataref:
                self._write_dataref(self._local_dataref, x)
                print(f'self._local_dataref: {self._local_dataref}')

            print(f'x: {x}')

    def get_status(self):
        a = super().get_status()
        if a is None:
            a = {}
        return a | {
            "step": self.step,
            "stepxl": self.stepxl,
            "value_min": self.value_min,
            "value_max": self.value_max,
            "cw": self._cw,
            "ccw": self._ccw,
            "turns": self._turns,
        }

    def describe(self):
        """
        Describe what the button does in plain English
        """
        a = [
            f"This encoder increases a value by {self.step} when it is turned clockwise.",
            f"This encoder decreases a value by {self.step} when it is turned counter-clockwise.",
            f"The value remains in the range [{self.value_min}-{self.value_max}].",
        ]
        if self.writable_dataref is not None:
            a.append(f"The value is written in dataref {self.writable_dataref}.")
        return "\n\r".join(a)

```