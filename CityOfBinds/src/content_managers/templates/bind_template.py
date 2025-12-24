from ...game.binds.bind import Bind
from ...game.binds.wasd_binds import WASDBind
from ...game.utils.triggers.trigger_mixin import _TriggerMixin
from ...game.utils.triggers.wasd_trigger import _WASDTrigger
from ..utils.commands_template import _CommandsTemplate


class BindTemplate(_TriggerMixin, _CommandsTemplate):
    BIND_TYPE = Bind

    def __init__(self, trigger: str):
        _TriggerMixin.__init__(self, trigger)
        _CommandsTemplate.__init__(self)

    def _build_one(self) -> Bind:
        return self.BIND_TYPE(self.trigger, super()._build_one())

    def _get_unique_count(self):
        return super()._get_unique_count()


class WASDBindTemplate(BindTemplate):
    TRIGGER_TYPE = _WASDTrigger
    BIND_TYPE = WASDBind
