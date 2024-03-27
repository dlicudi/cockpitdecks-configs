---
layout: default
title: Encoder Toggle
parent: Experimental
has_children: false
nav_order: 6
---

# Encoder Toggle

New encoder that allows use of the Loupedeck encoders push action to toggle between steps values e.g. coarse/fine.


```
class EncoderToggle(Activation):
    """
    Defines a encoder with stepped value coupled to an on/off button.

    On
    Command 0: Executed when turned clockwise
    Command 1: Executed when turned counter-clockwise
    Off
    Command 2: Executed when turned clockwise
    Command 3: Executed when turned counter-clockwise
    """

    def __init__(self, config: dict, button: "Button"):
        Activation.__init__(self, config=config, button=button)

        # Commands
        self._commands = [Command(path) for path in config.get("commands", [])]
        if len(self._commands) > 0:
            self._command = self._commands[0]
        else:
            logger.error(f"button {self.button_name()}: {type(self).__name__} must have at least one command")

        # Internal status
        self._turns = 0
        self._cw = 0
        self._ccw = 0

        self.longpush = True        
        self._on = True

    def num_commands(self):
        return len(self._commands) if self._commands is not None else 0

    def is_valid(self):
        if self.num_commands() != 4:
            logger.warning(f"button {self.button_name()}: {type(self).__name__} must have 4 commands")
            return False
        return True  # super().is_valid()

    def activate(self, state):
        if state == 1 and self._on:
            self._on = False
        elif state == 1 and not self._on:
            self._on = True

        if state < 2:
            super().activate(state)
        elif state == 2 and not self.is_pressed():  # rotate anti clockwise
            if self._on:
                self.command(self._commands[0])
                print(self._commands[0])
            else:
                self.command(self._commands[2])
                print(self._commands[2])

        elif state == 3 and not self.is_pressed():  # rotate clockwise
            if self._on:
                self.command(self._commands[1])
                print(self._commands[1])
            else:
                self.command(self._commands[3])
                print(self._commands[3])
        else:
            logger.warning(f"button {self.button_name()}: {type(self).__name__} invalid state {state}")

    def get_status(self):
        a = super().get_status()
        if a is None:
            a = {}
        return a | {"cw": self._cw, "ccw": self._ccw, "turns": self._turns}

    def describe(self):
        """
        Describe what the button does in plain English
        """
        if self.longpush:
            return "\n\r".join(
                [
                    f"This encoder has longpush option.",
                    f"This encoder executes command {self._commands[0]} when it is not pressed and turned clockwise.",
                    f"This encoder executes command {self._commands[1]} when it is not pressed and turned counter-clockwise.",
                    f"This encoder executes command {self._commands[2]} when it is pressed and turned clockwise.",
                    f"This encoder executes command {self._commands[3]} when it is pressed and turned counter-clockwise.",
                ]
            )
        else:
            return "\n\r".join(
                [
                    f"This encoder does not have longpush option.",
                    f"This encoder executes command {self._commands[0]} when it is pressed.",
                    f"This encoder does not execute any command when it is released.",
                    f"This encoder executes command {self._commands[1]} when it is turned clockwise.",
                    f"This encoder executes command {self._commands[2]} when it is turned counter-clockwise.",
                ]
            )
```