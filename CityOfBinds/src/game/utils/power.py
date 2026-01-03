class _Power:
    ### Initialization
    def __init__(self, power_string: str):
        formatted_power_string = power_string.lower().strip()
        self._power = formatted_power_string

    # region Dunder Methods
    def __str__(self) -> str:
        return self._power

    def __repr__(self) -> str:
        return f"Power('{self._power}')"

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    # endregion
