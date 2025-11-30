import re
from .pool import Pool
from .constants import TemplateConstants

class StringTemplate:
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

    def _build_one(self) -> str:
        placeholder_pattern = self._build_placeholder_regex()

        def replace_placeholder(match):
            placeholder_name = match.group(1)
            pool = self.pool_dict[placeholder_name]
            item = pool.pop()
            return str(item) if item is not None else ""
        
        result_string = placeholder_pattern.sub(replace_placeholder, self.template)
        return result_string
    
    def build(self, count: int) -> list[str]:
        return [self._build_one() for _ in range(count)]

    def _build_placeholder_regex(self):
        pool_names = [re.escape(pool_name) for pool_name in self.pool_dict.keys()]
        pool_alternation = "|".join(pool_names)
        left_encap = re.escape(TemplateConstants.ENCAPSULATION_LEFT)
        right_encap = re.escape(TemplateConstants.ENCAPSULATION_RIGHT)
        pattern = f"{left_encap}({pool_alternation}){right_encap}"
        return re.compile(pattern)

class ListTemplate():
    def __init__(self, template: list):
        self.template = template

    def _build_one(self) -> list:
        new_list = []
        for item in self.template:
            if isinstance(item, Pool):
                pool_value = item.pop()
                if pool_value is not None:
                    new_list.append(pool_value)
            else:
                new_list.append(item)
        return new_list

    def build(self, count: int = 1) -> list[list] | list:
        if count == 1:
            return self._build_one()
        return [self._build_one() for _ in range(count)]
