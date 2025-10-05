import re

class Power:
    def __init__(self, power_string: str):
        self._power_string = None
        self.power_string = power_string

    ### Properties
    @property
    def power_string(self) -> str:
        return self._power_string

    @power_string.setter
    def power_string(self, power_string: str):
        formatted_power_string = power_string.lower().strip()
        self._throw_error_on_invalid_power_string_format(power_string=formatted_power_string)
        self._power_string = formatted_power_string

    ### Error Checking/Validation
    def _throw_error_on_invalid_power_string_format(self, power_string: str):
        if not re.match(r"^[a-z]+( [a-z]+)*$", power_string):
            raise ValueError(f"Invalid power format: {power_string}")
