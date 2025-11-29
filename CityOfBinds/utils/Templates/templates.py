import re
from .pool import Pool

class StringTemplate:
    ENCAPSULATION_PATTERN = "<>"
    ENCAPSULATION_LEFT = ENCAPSULATION_PATTERN[:len(ENCAPSULATION_PATTERN)//2]
    ENCAPSULATION_RIGHT = ENCAPSULATION_PATTERN[len(ENCAPSULATION_PATTERN)//2:]

    def __init__(self, template: str, pools: list[Pool] = None):
        self.template = template
        self.pool_dict: dict[str, Pool] = {}

        if pools is not None:
            self.add_pools(pools)

    def add_pool(self, pool: Pool) -> 'StringTemplate':
        self.pool_dict[pool.name] = pool
        return self

    def add_pools(self, pools: list[Pool]) -> 'StringTemplate':
        for pool in pools:
            self.add_pool(pool)
        return self

    def build_string(self) -> str:
        placeholder_pattern = self._build_placeholder_regex()

        def replace_placeholder(match):
            placeholder_name = match.group(1)
            pool = self.pool_dict[placeholder_name]
            item = pool.pop()
            return str(item) if item is not None else ""
        
        result_string = placeholder_pattern.sub(replace_placeholder, self.template)
        return result_string
    
    def build_strings(self, count: int) -> list[str]:
        new_strings = []
        for _ in range(count):
            new_strings.append(self.build_string())
        return new_strings

    def _build_placeholder_regex(self):
        pool_names = [re.escape(pool_name) for pool_name in self.pool_dict.keys()]
        pool_alternation = "|".join(pool_names)
        left_encap = re.escape(self.ENCAPSULATION_LEFT)
        right_encap = re.escape(self.ENCAPSULATION_RIGHT)
        pattern = f"{left_encap}({pool_alternation}){right_encap}"
        return re.compile(pattern)

class CommandFactory:
    def __init__(self, command: str, argument_options: list[str], *args, **kwargs):
        self._command = command

        self._arg_pool = Pool("args", argument_options, *args, **kwargs)
        self._command_template = StringTemplate(f"{self._command} {self._arg_pool}", [self._arg_pool])

    def build_command(self) -> str:
        return self._command_template.build_string()
    
    def build_commands(self, count: int) -> list[str]:
        return self._command_template.build_strings(count)
    
class PowExecFactory(CommandFactory):
    def __init__(self, powers: list[str], *args, **kwargs):
        super().__init__("powexectoggleon", powers, *args, **kwargs)

class ListTemplate():
    def __init__(self, template: list):
        self.template = template

    def build_list(self) -> list:
        new_list = []
        for item in self.template:
            if isinstance(item, Pool):
                pool_value = item.pop()
                if pool_value is not None:
                    new_list.append(pool_value)
            else:
                new_list.append(item)
        return new_list

    def build_lists(self, count: int) -> list[list]:
        new_lists = []
        for _ in range(count):
            new_lists.append(self.build_list())
        return new_lists
