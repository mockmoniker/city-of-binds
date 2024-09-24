### open config json w/ user input

from bindfile import BindFile

def calculate_cycles():
    max_chars = 255
    running_char_count_total = 0

    default_bind_char_count = len("S \"+backwards\"")
    bind_load_file_command_char_count = len(f"bindloadfilesilent {file_path}\a.txt")
    pow_exec_auto_command_char_count = len("powexecauto ")
    pow_exec_toggle_off_command_char_count = len("powexectoggleoff ")
    pow_exec_toggle_on_command_char_count = len("powexectoggleon ")
    slash_command_delim_char_count = len("$$")






file_path = wasd_config.file_settings.file_path
include_space_bar = wasd_config.misc_settings.include_space_bar

w_bind = Bind(trigger = "W", slash_commands = ["+forward"])
a_bind = Bind(trigger = "A", slash_commands = ["+left"])
s_bind = Bind(trigger = "S", slash_commands = ["+backward"])
d_bind = Bind(trigger = "D", slash_commands = ["+right"])

unbind_file = BindFile()
unbind_file.add_bind(w_bind)
unbind_file.add_bind(a_bind)
unbind_file.add_bind(s_bind)
unbind_file.add_bind(d_bind)

if include_space_bar:
    space_bind = Bind(trigger = "SPACE", slash_commands = ["+up"])
    unbind_file.add_bind(space_bind)

unbind_file.write_to_file(f"{file_path}\\unbind_wasd.txt")

for 

for 