import copy

from .trigger import _Trigger


class _TriggerMixin:
    def __init__(self, trigger: str):
        self._trigger = None
        self._trigger_class = getattr(self, "TRIGGER_TYPE", _Trigger)
        self.trigger = trigger

    @property
    def trigger(self) -> _Trigger:
        return self._trigger

    @trigger.setter
    def trigger(self, value):
        if isinstance(value, str):
            self._trigger = self._trigger_class(value)
        elif isinstance(value, _Trigger):
            self._trigger = copy.deepcopy(value)
        else:
            self._throw_set_trigger_type_error(value)

    def _throw_set_trigger_type_error(self, value):
        raise TypeError(
            f"Invalid type '{type(value)}'. Trigger must be set using a string or a Trigger instance."
        )
