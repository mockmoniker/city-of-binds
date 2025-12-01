from abc import abstractmethod
from CityOfBinds.src.binds.bindtemplate import BindTemplate
from CityOfBinds.src.bind_file.bindfiletemplate import (
    BindFileTemplate,
    AdvanceOnTriggerType,
)
from CityOfBinds.src.bind_graph_publisher.graph import BindFileGraph
from CityOfBinds.src.bind_graph_publisher.publisher import BFGPublisher


class _GenericRotatingBind(BFGPublisher):
    def __init__(self):
        BFGPublisher.__init__(self)
        BindFileTemplate.__init__(self)
        self.bindfile_template = BindFileTemplate()

    def _indexed_bind_files(self):
        return self.bindfile_template.build_all()

    def add_bind_template(
        self,
        bind_template: BindTemplate,
        advance_on_trigger: AdvanceOnTriggerType = AdvanceOnTriggerType.DEFAULT,
    ):
        self.bindfile_template.add_bind_template(bind_template, advance_on_trigger)
        return self


class RotatingBind(_GenericRotatingBind):
    def __init__(self):
        _GenericRotatingBind.__init__(self)

    def _create_bind_file_links(self, bfg: BindFileGraph, bind_file_indexes: list[int]):
        bfg.loop(bind_file_indexes)
