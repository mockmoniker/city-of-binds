import random
import re
from enum import Enum

class SelectionType(Enum):
    SEQUENTIAL = 0
    RANDOM = 1
    RANDOM_ORDER = 2

class Pool:
    DEFAULT_SELECT_BEHAVIOR = SelectionType.SEQUENTIAL
    DEFAULT_IS_FINITE = False
    DEFAULT_RANDOM_SEED = 0xDEADBEEF

    def __init__(
        self, 
        name: str, 
        items: list, 
        select_behavior: SelectionType = DEFAULT_SELECT_BEHAVIOR, 
        is_finite: bool = DEFAULT_IS_FINITE,
        random_seed: int = DEFAULT_RANDOM_SEED,
    ):
        self.name: str = name
        self.items: list = items # TODO: verify list input, decide if it should be mutable (2025/11/27) 
        self.is_finite: bool = is_finite
        self._select_type: SelectionType = select_behavior
        self.random_seed: int = random_seed

        self._access_count = 0
        self._random_gen = random.Random(self.random_seed)
        self._random_items = self._new_random_order(self.items)

    @property
    def access_count(self) -> int:
        return self._access_count

    def pop(self):
        item = self.peek()
        if item is not None:
            self._pop_update()
        return item
    
    def peek(self):
        if self._select_type == SelectionType.RANDOM:
            self._random_gen.seed(self._access_count + self.random_seed)
            return self._random_gen.choice(self.items)

        if self.is_finite and self._access_count == len(self.items):
            return None

        if self._select_type == SelectionType.SEQUENTIAL:
            return self.items[self._access_count % len(self.items)]
        
        if self._select_type == SelectionType.RANDOM_ORDER:
            """ creates a new random list whenever random list is exhausted """
            return self._random_items[self._access_count % len(self.items)]

    def set_select_behavior(self, behavior: SelectionType): # TODO: do I really want this value to be updated? Does it cause weird behavior as is? (2025/11/27) 
        self._select_type = behavior

    def _pop_update(self):
        self._access_count += 1
        if self._select_type == SelectionType.RANDOM_ORDER:
            if self._access_count % len(self.items) == 0:
                self._random_items = self._new_random_order(self.items)

    def _new_random_order(self, items: list) -> list:
        random_items = items.copy()
        self._random_gen.shuffle(random_items)
        return random_items

    def __str__(self):
        return f"{StringTemplate.ENCAPSULATION_LEFT}{self.name}{StringTemplate.ENCAPSULATION_RIGHT}"

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
    
# example usage:

costumes = Pool("costumes", ["wizard", "warrior", "rogue"], SelectionType.RANDOM_ORDER)
toggle_commands = ToggleOnTemplate(costumes).build_commands(5)

command_template = CommandGroupTemplate()
command_template.add_movement_command("forward").add_pool(toggle_commands)

bind_commands = command_template.build_commands(3)

binds = [Bind("W", bind_commands)]

for bind in binds:
    print(bind.bind_string)
# Output might be:
# W "+forward$$powexectoggleon wizard"
# W "+forward$$powexectoggleon warrior"
# W "+forward$$powexectoggleon rogue"