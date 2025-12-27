import copy

from .trigger import _Trigger


class _TriggerMixin:
    """
    Mixin class providing trigger functionality to game objects.

    This mixin adds trigger property management to classes that need to handle
    game input triggers. It supports both string initialization and Trigger object
    assignment with automatic type conversion and validation.

    The mixin allows subclasses to specify a custom trigger type by defining
    a TRIGGER_TYPE class attribute, enabling specialized trigger behavior.

    Attributes:
        trigger (_Trigger): The trigger instance managing input key combinations

    Example:
        >>> class MyGameObject(_TriggerMixin):
        ...     def __init__(self, trigger_str):
        ...         super().__init__(trigger_str)
        ...
        >>> obj = MyGameObject("shift+f1")
        >>> obj.trigger.key  # "F1"
        >>> obj.trigger.modifier  # "SHIFT"

    Note:
        This is an internal mixin class. Subclasses should handle the trigger
        property through the provided interface rather than accessing _trigger directly.
    """

    def __init__(self, trigger: str):
        """
        Initialize the trigger mixin with a trigger string.

        Sets up the trigger management system, allowing subclasses to customize
        the trigger type through the TRIGGER_TYPE class attribute.

        Args:
            trigger: String representation of the trigger (e.g., "shift+f1", "w", "ctrl+q")
                    Will be parsed and validated according to trigger format rules

        Raises:
            ValueError: If trigger string format is invalid
            AttributeError: If trigger contains unsupported keys or modifiers

        Example:
            >>> mixin = _TriggerMixin("alt+space")
            >>> mixin.trigger.key  # "SPACE"
            >>> mixin.trigger.modifier  # "ALT"
        """
        self._trigger = None
        self._trigger_class = getattr(self, "TRIGGER_TYPE", _Trigger)
        self.trigger = trigger

    @property
    def trigger(self) -> _Trigger:
        """
        Get the current trigger instance.

        Returns:
            _Trigger: The trigger object managing key and modifier combinations
                     Contains parsed and validated key/modifier information

        Example:
            >>> mixin = _TriggerMixin("ctrl+w")
            >>> trigger_obj = mixin.trigger
            >>> trigger_obj.key  # "W"
            >>> trigger_obj.modifier  # "CTRL"
        """
        return self._trigger

    @trigger.setter
    def trigger(self, value):
        """
        Set the trigger using either a string or Trigger instance.

        Accepts multiple input types and automatically handles conversion and validation.
        String values are parsed into Trigger objects, while Trigger instances are
        deep-copied to prevent unwanted shared references.

        Args:
            value: Either a string representation (e.g., "shift+f1") or a Trigger instance
                  String values will be parsed and validated
                  Trigger instances will be deep-copied

        Raises:
            TypeError: If value is neither string nor Trigger instance
            ValueError: If string value has invalid trigger format
            AttributeError: If string contains unsupported keys or modifiers

        Example:
            >>> mixin = _TriggerMixin("f1")
            >>> mixin.trigger = "alt+space"  # String assignment
            >>> other_trigger = _Trigger("ctrl+q")
            >>> mixin.trigger = other_trigger  # Trigger assignment (deep-copied)
        """
        if isinstance(value, str):
            self._trigger = self._trigger_class(value)
        elif isinstance(value, _Trigger):
            self._trigger = copy.deepcopy(value)
        else:
            self._throw_set_trigger_type_error(value)

    def _throw_set_trigger_type_error(self, value):
        raise TypeError(
            f"Invalid type '{type(value)}'. Trigger must be set using a string or a Trigger instance."
        )
