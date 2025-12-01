import re


class Power:
    ### Initialization
    def __init__(self, power_string: str):
        formatted_power_string = power_string.lower().strip()
        self._throw_error_if_invalid_power_string_format(
            power_string=formatted_power_string
        )
        self._power = formatted_power_string

    # region Validation and Error Checking
    def _throw_error_if_invalid_power_string_format(self, power_string: str):
        if not re.match(r"^[a-z]+( [a-z]+)*$", power_string):
            raise ValueError(
                f"Invalid power format: '{power_string}'. Power must only contain letters and spaces."
            )

    # endregion

    # region Dunder Methods
    def __str__(self) -> str:
        return self._power

    def __repr__(self) -> str:
        return f"Power('{self._power}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Power):
            return False
        return self._power == other._power

    # endregion
