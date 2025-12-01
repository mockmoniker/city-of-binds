from CityOfBinds.src.Binds.bind import Bind, WASDBind
from CityOfBinds.src.Triggers.trigger import Trigger, WASDTrigger
from CityOfBinds.src.Triggers.mixin import TriggerMixin
from CityOfBinds.src.SlashCommands.commandstemplate import CommandsTemplate

class BindTemplate(TriggerMixin, CommandsTemplate):
    BIND_TYPE = Bind

    def __init__(self, trigger: Trigger | str):
        TriggerMixin.__init__(self)
        CommandsTemplate.__init__(self)
        self.trigger = trigger

    def _build_one(self) -> Bind:
        return self.BIND_TYPE(self.trigger, super()._build_one())

    def _get_unique_count(self):
        return super()._get_unique_count()

class WASDBindTemplate(BindTemplate):
    TRIGGER_TYPE = WASDTrigger
    BIND_TYPE = WASDBind
