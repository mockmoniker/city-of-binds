from CityOfBinds.src.Binds.bind import Bind
from CityOfBinds.src.Triggers.trigger import Trigger
from CityOfBinds.src.Triggers.mixin import TriggerMixin
from CityOfBinds.utils.Templates import ListTemplate

class BindTemplate(TriggerMixin, ListTemplate):
    def __init__(self, trigger: Trigger | str, commands_template: ListTemplate):
        super().__init__(commands_template)
        self.trigger = trigger

    def _build_one(self) -> Bind:
        commands = self.template._build_one()
        return Bind(self.trigger, commands)
