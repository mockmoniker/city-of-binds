from enum import Enum
from typing import Self

from ....utils.templates.templates import ListTemplate
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
        """
        Internal method to add a bind template to the collection.

        Appends the bind template to the internal template list for later processing
        during bind file generation. This method handles the core template storage
        without applying rotation policies or trigger management.

        Args:
            item: The bind template to add to the collection

        Returns:
            Self for method chaining

        Note:
            This is an internal method used by add_bind_template. Direct usage
            bypasses rotation policy and quick trigger management, which may result
            in incorrect bind file advancement behavior in rotating sequences.
        """
        self.template.append(item)
        return self

    # endregion

    # region Template Generation Methods
    def _build_one(self) -> BindFile:
        """
        Generate a single bind file from all collected bind templates.

        Processes all bind templates in the collection and combines them into a
        complete BindFile. Each bind template's _build_one() method is called to
        generate individual binds, which are then assembled into the final file.

        Returns:
            Complete BindFile containing all generated binds

        Example:
            >>> template = BindFileTemplate()
            >>> template.add_bind_template(combat_bind)
            >>> template.add_bind_template(travel_bind)
            >>> bind_file = template._build_one()
            >>> len(bind_file.binds)  # 2

        Note:
            This method implements the core generation logic. For multiple variations,
            use the inherited build() method which calls this method iteratively.
        """
        bind_file = BindFile()
        for bind_template in self.template:
            bind_file.add_bind(bind_template._build_one())
        return bind_file

    def _get_unique_count(self) -> int:
        """
        Calculate the total number of unique bind file variations possible.

        Determines how many different bind files can be generated from the current
        collection of bind templates by analyzing each template's unique count and
        calculating the Least Common Multiple (LCM) of all template lengths.

        Since bind templates iterate in parallel rather than cross-product style,
        the unique count is the LCM - the point where all templates sync back to
        their starting positions after cycling through their variations.

        Returns:
            Integer representing total unique variations (LCM of all template lengths)

        Example:
            >>> # Template with bind templates having 4, 2, and 6 unique counts each
            >>> template._get_unique_count()  # Returns LCM(4, 2, 6) = 12
            >>> # The 2-count template cycles 6 times, 4-count cycles 3 times,
            >>> # 6-count cycles 2 times before all sync up at iteration 12

        Note:
            This calculation is used by the ListTemplate generation system to
            determine iteration bounds for comprehensive bind file generation.
            Uses inherited _calculate_unique_count_from_lengths() method.
        """
        content_lengths = [content.unique_count for content in self.template]
        return self._calculate_unique_count_from_lengths(content_lengths)

    # endregion
