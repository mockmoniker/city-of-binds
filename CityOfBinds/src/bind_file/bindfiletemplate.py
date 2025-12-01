from typing import Self
from enum import Enum
from CityOfBinds.src.bind_file.bindfile import BindFile
from CityOfBinds.utils.Templates import ListTemplate


class AdvanceOnTriggerType(Enum):
    INCLUDE = 1
    EXCLUDE = 2
    DEFAULT = 3


class BindFileTemplate(ListTemplate):
    def __init__(self):
        ListTemplate.__init__(self, [])
        self.include_triggers = []
        self.exclude_triggers = []

    def add_bind_template(
        self,
        bind_template,
        advance_on_trigger: AdvanceOnTriggerType = AdvanceOnTriggerType.DEFAULT,
    ) -> Self:
        if advance_on_trigger == AdvanceOnTriggerType.INCLUDE:
            self.include_triggers.append(bind_template.trigger)
        elif advance_on_trigger == AdvanceOnTriggerType.EXCLUDE:
            self.exclude_triggers.append(bind_template.trigger)
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
