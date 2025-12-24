from enum import Enum
from typing import Self

from ....utils.templates.templates import ListTemplate
from ...game.bind_file.bind_file import BindFile


class RotationPolicy(Enum):
    ON_THIS_TRIGGER = "inclusive"
    NOT_ON_THIS_TRIGGER = "exclusive"
    DEFAULT = "default"


class BindFileTemplate(ListTemplate):
    def __init__(self):
        ListTemplate.__init__(self, [])
        self.include_triggers = []
        self.exclude_triggers = []
        self.quick_triggers = []

    def add_bind_template(
        self,
        bind_template,
        rotation_policy: RotationPolicy = RotationPolicy.DEFAULT,
        quick_trigger: bool = False,
    ) -> Self:
        if rotation_policy == RotationPolicy.ON_THIS_TRIGGER:
            self.include_triggers.append(bind_template.trigger)
        elif rotation_policy == RotationPolicy.NOT_ON_THIS_TRIGGER:
            self.exclude_triggers.append(bind_template.trigger)
        if quick_trigger:
            self.quick_triggers.append(bind_template.trigger)
        return self._add_content(bind_template)

    def _add_content(self, item) -> Self:
        self.template.append(item)
        return self

    def _build_one(self) -> BindFile:
        bind_file = BindFile()
        for bind_template in self.template:
            bind_file.add_bind(bind_template._build_one())
        return bind_file

    def _get_unique_count(self) -> int:
        content_lengths = [content.unique_count for content in self.template]
        return self._calculate_unique_count_from_lengths(content_lengths)
