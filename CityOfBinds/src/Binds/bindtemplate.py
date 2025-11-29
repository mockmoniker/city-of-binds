from CityOfBinds.src.Binds.bind import Bind
from CityOfBinds.src.Triggers.trigger import Trigger
from CityOfBinds.src.Triggers.mixin import TriggerMixin
from CityOfBinds.utils.Templates import ListTemplate

class BindTemplate(TriggerMixin):
    def __init__(self, trigger: Trigger | str, commands_template: ListTemplate):
        super().__init__()
        self.trigger = trigger
        self.commands_template: ListTemplate = commands_template

    def build_bind(self) -> Bind:
        return Bind(self.trigger, self.commands_template.build_list())

    def build_binds(self, count: int) -> list[Bind]:
        return [self.build_bind() for _ in range(count)]