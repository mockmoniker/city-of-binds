from ...game_content.binds.bind import Bind
from ...game_content.binds.wasd_binds import WASDBind
from ...game_content.utils.triggers.trigger_mixin import _TriggerMixin
from ...game_content.utils.triggers.wasd_trigger import _WASDTrigger
from ..utils.commands_template import _CommandsTemplate


class BindTemplate(_TriggerMixin, _CommandsTemplate):
    """
    Template for generating individual bind objects with configurable commands.

    BindTemplate combines trigger management with command template functionality to
    create individual bind objects. It serves as a factory for generating bind
    instances with specific triggers and collections of slash commands.

    The template inherits from both _TriggerMixin (for trigger validation and management)
    and _CommandsTemplate (for command collection and generation), providing a complete
    solution for bind creation with dynamic command sequences.

    Key Features:
        - Trigger validation and storage via _TriggerMixin
        - Command collection and templating via _CommandsTemplate
        - Dynamic bind generation with _build_one()
        - Support for multiple bind variations through unique count calculation
        - Extensible architecture for specialized bind types

    Class Attributes:
        BIND_TYPE: The type of bind object to create (default: Bind)

    Inheritance Chain:
        BindTemplate -> _TriggerMixin (trigger management)
                    -> _CommandsTemplate (command collection)

    Example:
        >>> template = BindTemplate("F1")
        >>> template.add_power("Hasten")
        >>> template.add_emote("wave")
        >>> bind = template._build_one()
        >>> print(bind.trigger)  # "F1"
        >>> print(len(bind.commands))  # 2
    """

    BIND_TYPE = Bind

    def __init__(self, trigger: str):
        """
        Initialize a new BindTemplate with the specified trigger.

        Creates a bind template that can generate bind objects with the given trigger
        and any commands added through the inherited command template methods.

        Args:
            trigger: The key or key combination that will activate the bind
                    (e.g., "F1", "CTRL+ALT+Q", "LBUTTON")

        Example:
            >>> template = BindTemplate("SHIFT+F5")
            >>> template.add_command("say Hello World!")
            >>> bind = template._build_one()
            >>> bind.trigger  # "SHIFT+F5"

        Note:
            Trigger validation is handled by the _TriggerMixin parent class.
            Invalid triggers will raise appropriate exceptions during initialization.
        """
        _TriggerMixin.__init__(self, trigger)
        _CommandsTemplate.__init__(self)

    # region Template Generation Methods
    def _build_one(self) -> Bind:
        """Generate bind object with current trigger and commands."""
        return self.BIND_TYPE(self.trigger, super()._build_one())

    # endregion


class WASDBindTemplate(BindTemplate):
    """
    Specialized bind template for WASD movement key binds with enhanced trigger validation.

    WASDBindTemplate extends BindTemplate with specific support for movement key binds
    that use WASD keys (W, A, S, D) and related directional controls. It provides
    enhanced trigger validation through _WASDTrigger and generates WASDBind objects
    optimized for movement-related commands.

    This template is particularly useful for creating movement macros, travel power
    binds, and directional command sequences that need to integrate seamlessly with
    the game's movement system.

    Key Differences from BindTemplate:
        - Uses _WASDTrigger for enhanced movement key validation
        - Generates WASDBind objects instead of standard Bind objects
        - Optimized for movement-related command sequences
        - Supports directional movement patterns and travel powers

    Class Attributes:
        TRIGGER_TYPE: Specifies _WASDTrigger for movement key validation
        BIND_TYPE: Specifies WASDBind for movement-optimized bind generation

    Example:
        >>> template = WASDBindTemplate("W")
        >>> template.add_power("Super Speed")
        >>> template.add_command("++forward")
        >>> wasd_bind = template._build_one()
        >>> isinstance(wasd_bind, WASDBind)  # True
        >>> wasd_bind.trigger  # "W"

    Note:
        All command template methods (add_power, add_emote, etc.) are inherited
        from the parent classes and work identically to BindTemplate.
    """

    TRIGGER_TYPE = _WASDTrigger
    BIND_TYPE = WASDBind
