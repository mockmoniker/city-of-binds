import copy
from CityOfBinds.src.Triggers.trigger import Trigger

class TriggerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._trigger = None
        self._trigger_class = getattr(self, 'TRIGGER_TYPE', Trigger)
    
    @property
    def trigger(self) -> Trigger:
        return self._trigger
    
    @trigger.setter
    def trigger(self, value):
        if isinstance(value, str):
            self._trigger = self._trigger_class(value)
        elif isinstance(value, Trigger):
            self._trigger = copy.deepcopy(value)
        else:
            self._throw_set_trigger_type_error(value)

    def _throw_set_trigger_type_error(self, value):
        raise TypeError(f"Invalid type '{type(value)}'. Trigger must be set using a string or a Trigger instance.")
