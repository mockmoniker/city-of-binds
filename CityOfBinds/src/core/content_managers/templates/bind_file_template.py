from enum import Enum
from typing import Self

from .....utils.templates.templates import ListTemplate
from ...game.bind_file.bind_file import BindFile


class RotationPolicy(Enum):
    """
    Enum defining rotation policies for bind templates within rotating bind file sequences.

    Controls which bind templates receive the additional command to load the next bind file
    in a rotating sequence. This allows fine-grained control over bind file advancement.

    Values:
        ON_THIS_TRIGGER: Only binds with this policy will advance to the next bind file.
                        If ANY bind uses this policy, it becomes EXCLUSIVE - only these binds advance.
        NOT_ON_THIS_TRIGGER: This trigger will NEVER advance to the next bind file.
        DEFAULT: By default, the bind will advance to the next bind file, UNLESS there are
                binds with ON_THIS_TRIGGER policy (which makes advancement exclusive).

    Behavior Logic:
        - If NO binds have ON_THIS_TRIGGER: All DEFAULT binds advance to next file
        - If ANY bind has ON_THIS_TRIGGER: Only ON_THIS_TRIGGER binds advance (exclusive mode)
        - NOT_ON_THIS_TRIGGER: This trigger will never advance to the next file

    Example:
        >>> # All binds advance by default
        >>> template.add_bind_template(basic_bind)  # DEFAULT - will advance
        >>> template.add_bind_template(combat_bind) # DEFAULT - will advance

        >>> # Exclusive advancement - only F1 advances
        >>> template.add_bind_template(f1_bind, RotationPolicy.ON_THIS_TRIGGER)  # Only this advances
        >>> template.add_bind_template(f2_bind)  # DEFAULT - will NOT advance (excluded)

        >>> # All except F3 advance
        >>> template.add_bind_template(f3_bind, RotationPolicy.NOT_ON_THIS_TRIGGER)  # F3 won't advance
    """

    ON_THIS_TRIGGER = "inclusive"  # Only this trigger advances (exclusive when present)
    NOT_ON_THIS_TRIGGER = "exclusive"  # Never advances
    DEFAULT = "default"  # Advances unless ON_THIS_TRIGGER is used


class BindFileTemplate(ListTemplate):
    """
    Template for generating rotating bind files with controlled bind file advancement.

    A BindFileTemplate manages collections of bind templates that generate bind files
    capable of rotating to the next bind file in a sequence. It provides sophisticated
    control over which binds receive the "load next bind file" command through rotation policies.

    The template supports advanced rotation patterns:
    - Exclusive advancement (only specific triggers advance)
    - Inclusive advancement (all triggers advance by default)
    - Selective exclusion (all except specific triggers advance)
    - Key up press activation for selected triggers

    Key Concepts:
        - **Rotation**: Process of loading the next bind file in a sequence
        - **Advancement**: Adding the command to load the next bind file
        - **Exclusive Mode**: When ON_THIS_TRIGGER is used, only those binds advance
        - **Inclusive Mode**: Default behavior where all binds advance

    Attributes:
        include_triggers: List of triggers that will exclusively advance to next bind file
        exclude_triggers: List of triggers that will NOT advance to next bind file
        quick_triggers: List of triggers that activate on key up press in addition to key down

    Example:
        >>> template = BindFileTemplate()
        >>> # Normal bind - advances by default
        >>> template.add_bind_template(combat_bind)
        >>> # Only F1 will advance (exclusive mode activated)
        >>> template.add_bind_template(f1_bind, RotationPolicy.ON_THIS_TRIGGER)
        >>> # F2 won't advance due to exclusive mode from F1
        >>> template.add_bind_template(f2_bind)
    """

    def __init__(self):
        """
        Initialize a new BindFileTemplate with empty trigger management lists.

        Creates a new template for rotating bind files with no bind templates and
        initializes all trigger management lists (include, exclude, quick) to empty states.

        The include/exclude lists control which binds get the "load next bind file" command
        when the rotating bind file sequence is generated and linked together.

        Example:
            >>> template = BindFileTemplate()
            >>> len(template.include_triggers)  # 0 - no exclusive advancement triggers
            >>> len(template.exclude_triggers)  # 0 - no excluded triggers
            >>> len(template.quick_triggers)    # 0 - no key up press triggers
        """
        ListTemplate.__init__(self, [])
        self.include_triggers = (
            []
        )  # Triggers that exclusively advance to next bind file
        self.exclude_triggers = []  # Triggers that will NOT advance to next bind file
        self.quick_triggers = []  # Triggers that activate on key up press

    # region Bind Template Management Methods
    def add_bind_template(
        self,
        bind_template,
        rotation_policy: RotationPolicy = RotationPolicy.DEFAULT,
        trigger_on_up_press: bool = False,
    ) -> Self:
        """
        Add a bind template with specified rotation policy and quick trigger settings.

        Incorporates a bind template into the rotating bind file with configurable behavior
        for bind file advancement. The rotation policy determines whether this bind will
        receive the "load next bind file" command when the sequence is linked together.

        Args:
            bind_template: The bind template to add (must have a 'trigger' attribute)
            rotation_policy: Controls bind file advancement behavior:
                           - DEFAULT: Will advance to next file (unless exclusive mode activated)
                           - ON_THIS_TRIGGER: Only this trigger advances (activates exclusive mode)
                           - NOT_ON_THIS_TRIGGER: This trigger will never advance
            trigger_on_up_press: Whether this trigger should also activate on key release

        Returns:
            Self for method chaining

        Rotation Policy Behavior:
            - If any bind uses ON_THIS_TRIGGER, exclusive mode activates
            - In exclusive mode, only ON_THIS_TRIGGER binds get advancement commands
            - Multiple binds can use ON_THIS_TRIGGER to create an inclusive list
            - NOT_ON_THIS_TRIGGER excludes specific triggers from advancement

        Example:
            >>> template = BindFileTemplate()
            >>> # Basic bind - will advance by default
            >>> template.add_bind_template(basic_bind)
            >>> # Exclusive bind - only F1 will advance (activates exclusive mode)
            >>> template.add_bind_template(f1_bind, RotationPolicy.ON_THIS_TRIGGER)
            >>> # F2 won't advance due to exclusive mode
            >>> template.add_bind_template(f2_bind)
            >>> # Multiple exclusive triggers
            >>> template.add_bind_template(f3_bind, RotationPolicy.ON_THIS_TRIGGER)  # F3 also advances
        """
        # Apply rotation policy to trigger management
        if rotation_policy == RotationPolicy.ON_THIS_TRIGGER:
            self.include_triggers.append(bind_template.trigger)
        elif rotation_policy == RotationPolicy.NOT_ON_THIS_TRIGGER:
            self.exclude_triggers.append(bind_template.trigger)

        # Enable key up press activation if requested
        if trigger_on_up_press:
            self.quick_triggers.append(bind_template.trigger)

        return self._add_content(bind_template)

    def _add_content(self, item) -> Self:
        """Add bind template to collection without applying rotation policies."""
        self.template.append(item)
        return self

    # endregion

    # region Template Generation Methods
    def _build_one(self) -> BindFile:
        """Generate single bind file by processing all bind templates."""
        bind_file = BindFile()
        for bind_template in self.template:
            bind_file.add_bind(bind_template._build_one())
        return bind_file

    def _get_unique_count(self) -> int:
        """Calculate LCM of all template lengths for parallel iteration."""
        content_lengths = [content.unique_count for content in self.template]
        return self._calculate_unique_count_from_lengths(content_lengths)

    # endregion
