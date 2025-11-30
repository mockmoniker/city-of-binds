from typing import Self
from CityOfBinds.src.BindFile.bindfile import BindFile
from CityOfBinds.utils.Templates import ListTemplate

class BindFileTemplate(ListTemplate):
    def __init__(self):
        ListTemplate.__init__(self, [])

    def add_bind_template(self, bind_template) -> Self:
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