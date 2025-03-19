from CityOfBinds import Bind

class TestBindFileParameters:

    #({valid file name}, {expected file name})
    test_init_should_set_filename_given_valid_filename_parameters = [
        ("bind.txt", "bind.txt"),
        ("custom_bind.txt", "custom_bind.txt"),
    ]

    #({valid comment banner}, {expected comment banner})
    test_init_should_set_comment_banner_given_valid_comment_banner_parameters = [
        ("binds binds binds", "binds binds binds"),
        ("Custom comment banner", "Custom comment banner"),
        ("Another comment", "Another comment"),
    ]

    # ({valid binds}, {expected binds})
    test_init_should_set_binds_given_valid_binds_parameters = [
        ([Bind(trigger="T", slash_commands=["/command1"])], [Bind(trigger="T", slash_commands=["/command1"])]),
        ([Bind(trigger="W", slash_commands=["/command2", "/command3"])], [Bind(trigger="W", slash_commands=["/command2", "/command3"])]),
        ([Bind(trigger="A", slash_commands=["/command4"]), Bind(trigger="S", slash_commands=["/command5"])], [Bind(trigger="A", slash_commands=["/command4"]), Bind(trigger="S", slash_commands=["/command5"])]),
    ]