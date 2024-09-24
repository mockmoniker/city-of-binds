from CityOfBinds.binds import Bind
from CityOfBinds.binds import WASDBind

def main():

    single_bind = Bind(trigger="X", slash_commands=["first_command"])
    print(single_bind.get_bind_string())  # Output: X "single_command"

    multi_bind = Bind(trigger="Y", slash_commands=["first_command", "second_command"])
    print(multi_bind.get_bind_string())  # Output: Y "first_command$$second_command

    single_bind.add_slash_command("second_command")
    print(single_bind.get_bind_string())  # Output: X "first_command$$second_command"

    multi_bind.add_slash_commands(["third_command", "fourth_commanddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"])
    print(multi_bind.get_bind_string())  # Output: Y "first_command$$second_command$$third_command$$fourth_command"

    w_bind = WASDBind(trigger="w")
    w_bind.set_auto_power("hasten")
    w_bind.add_toggle_on_power("dark nova")
    w_bind.add_toggle_off_powers("black dwarf")
    print(w_bind.get_bind_string())  # Output: W "+forward"
    w_bind.set_trigger("SPACE")
    print(w_bind.get_bind_string())  # Output: SPACE "+up$$powexectoggleoff dark nova$$powexectoggleon black dwarf$$powexecauto hasten"

    a_bind = WASDBind(trigger="a", slash_commands="new_command")
    a_bind.set_toggle_on_powers("dark nova")
    a_bind.set_auto_power("domination")
    print(a_bind.get_bind_string())  # Output: A "+left$$new_command$$powexectoggleon dark nova$$powexecauto domination"

if __name__ == "__main__":
    main()