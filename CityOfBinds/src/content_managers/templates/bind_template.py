from CityOfBinds import Bind, WASDBind
from .utils.commands_template import CommandsTemplate
from ...game.utils.triggers import WASDTrigger, TriggerMixin


class BindTemplate(TriggerMixin, CommandsTemplate):
    BIND_TYPE = Bind

    def __init__(self, trigger: str):
        TriggerMixin.__init__(self, trigger)
        CommandsTemplate.__init__(self)

    def _build_one(self) -> Bind:
        return self.BIND_TYPE(self.trigger, super()._build_one())

    def _get_unique_count(self):
        return super()._get_unique_count()


class WASDBindTemplate(BindTemplate):
    TRIGGER_TYPE = WASDTrigger
    BIND_TYPE = WASDBind
