from typing import Self

from ..._configs.constants import ChangelingConstants
from ...core.content_managers.templates.bind_template import BindTemplate
from ...core.game_content.utils.triggers.trigger_mixin import _TriggerEnjoyer
from .rotating_bind import RotatingBind


class _ChangelingRotatingBind(_TriggerEnjoyer, RotatingBind):
    NOVA_FORM: str
    DWARF_FORM: str

    def __init__(
        self, trigger: str, is_silent: bool = True, absolute_path_links: bool = False
    ):
        _TriggerEnjoyer.__init__(self, trigger)
        RotatingBind.__init__(
            self,
            is_silent=is_silent,
            absolute_path_links=absolute_path_links,
            loop_delay=1,
        )
        self._form_changes: list[str] = []
        self._form_powers: list[str] = []
        self.changeling_bind_template: BindTemplate = BindTemplate(self.trigger)

    def add_bolt(self, count: int = 1) -> Self:
        return self._add_nova_power(ChangelingConstants.BOLT, count)

    def add_blast(self, count: int = 1) -> Self:
        return self._add_nova_power(ChangelingConstants.BLAST, count)

    def add_detonation(self, count: int = 1) -> Self:
        return self._add_nova_power(ChangelingConstants.DETONATION, count)

    def add_strike(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.STRIKE, count)

    def add_smite(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.SMITE, count)

    def add_antagonize(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.ANTAGONIZE, count)

    def _build_bind_files(self):
        self._build_changeling_bind_template(self.changeling_bind_template)
        self._bind_file_template.add_bind_template(
            self.changeling_bind_template, execute_on_up_press=True
        )
        return super()._build_bind_files()

    def _add_nova_power(self, power: str, count: int = 1) -> Self:
        return self._add_form_power(self.NOVA_FORM, power, count)

    def _add_dwarf_power(self, power: str, count: int = 1) -> Self:
        return self._add_form_power(self.DWARF_FORM, power, count)

    def _add_form_power(self, form: str, power: str, count: int = 1) -> Self:
        for _ in range(count):
            self._form_changes.append(form)
            self._form_powers.append(f"{form} {power}")
        return self

    def _build_changeling_bind_template(self, template: BindTemplate):
        template.add_toggle_on_power_pool(self._form_changes)
        template.add_power_pool(self._form_powers)
        template.add_toggle_off_power_pool(self._form_changes)


class ChangelingRotatingBindWS(_ChangelingRotatingBind):
    NOVA_FORM = ChangelingConstants.DARK_NOVA
    DWARF_FORM = ChangelingConstants.BLACK_DWARF

    def __init__(
        self, trigger: str, is_silent: bool = True, absolute_path_links: bool = False
    ):
        super().__init__(
            trigger, is_silent=is_silent, absolute_path_links=absolute_path_links
        )

    def add_emmanation(self, count: int = 1) -> Self:
        return self._add_nova_power(ChangelingConstants.EMMANATION, count)

    def add_drain(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.DRAIN, count)

    def add_mire(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.MIRE, count)


class ChangelingRotatingPB(_ChangelingRotatingBind):
    NOVA_FORM = ChangelingConstants.BRIGHT_NOVA
    DWARF_FORM = ChangelingConstants.WHITE_DWARF

    def __init__(
        self, trigger: str, is_silent: bool = True, absolute_path_links: bool = False
    ):
        super().__init__(
            trigger, is_silent=is_silent, absolute_path_links=absolute_path_links
        )

    def add_scatter(self, count: int = 1) -> Self:
        return self._add_nova_power(ChangelingConstants.SCATTER, count)

    def add_flare(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.FLARE, count)

    def add_sublimation(self, count: int = 1) -> Self:
        return self._add_dwarf_power(ChangelingConstants.SUBLIMATION, count)
