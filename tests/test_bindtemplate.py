from CityOfBinds import CommandsTemplate, BindTemplate

class TestBindTemplate:
    def test_bindtemplate(self):
        powers = ["dark nova blast", "dark nova bolt", "dark nova emmanation"]
        command_template = (CommandsTemplate()
            .add_toggle_off_power("super speed")
            .add_toggle_off_power("sprint")
            .add_toggle_on_power("dark nova")
            .add_power_pool(powers)
            .add_toggle_off_power("dark nova")
        )
        bind_template = BindTemplate('1', command_template)

        assert str(bind_template.build()[0]) == '1 "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova blast$$powexectoggleoff dark nova"'
        assert str(bind_template.build()[0]) == '1 "powexectoggleoff super speed$$powexectoggleoff sprint$$powexectoggleon dark nova$$powexecname dark nova bolt$$powexectoggleoff dark nova"'