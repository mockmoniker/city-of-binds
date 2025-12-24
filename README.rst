================
City of Binds
================

A Python library for creating advanced key binds for City of Heroes. Whether you want simple macros or complex rotating power sequences, this library helps you generate the bind files automatically.

**Perfect for City of Heroes players who want:**

- Automated toggle management (keep your shields/travel powers on automatically)
- Complex power rotations through simple movement keys
- Multiple auto-cast powers cycling as you play
- Custom bind file generation without manual editing

🎮 **New to Programming?**
~~~~~~~~~~~~~~~~~~~~~~~~

Don't worry! You don't need to be a programmer to use this. If you're new to Python, check out these beginner-friendly resources:

- `Python.org Beginner's Guide <https://www.python.org/about/gettingstarted/>`_
- `Installing Python <https://realpython.com/installing-python/>`_
- `Python for Beginners <https://docs.python.org/3/tutorial/>`_

📦 Installation
~~~~~~~~~~~~~~~

Install from PyPI using pip:

.. code-block:: bash

    pip install CityOfBinds

🚀 Quick Start
~~~~~~~~~~~~~~

Here's how to create a basic WASD bind that automatically keeps your travel powers on:

.. code-block:: python

    from CityOfBinds import WASDRotatingBind

    # Create a rotating bind system
    wasd_bind = WASDRotatingBind()

    # Add powers you want automatically turned on
    wasd_bind.wasd_bind_template.add_toggle_on_power("sprint")
    wasd_bind.wasd_bind_template.add_toggle_on_power("super speed")

    # Generate the bind files
    wasd_bind.publish_bind_files(
        parent_folder_name="travel_powers", 
        directory="my_binds"
    )

    # Load in game with: /bindloadfile my_binds/travel_powers/0.txt

This creates bind files that automatically turn on your travel powers whenever you move with WASD keys!

💡 Real Examples
~~~~~~~~~~~~~~~~

**Automated Toggle Management** (Great for Warshades, Peacebringers, etc.)

.. code-block:: python

    from CityOfBinds import WASDRotatingBind

    wasd_bind = WASDRotatingBind()
    
    # Keep human form (turn off transformations)
    wasd_bind.wasd_bind_template.add_toggle_off_power("dark nova")
    wasd_bind.wasd_bind_template.add_toggle_off_power("black dwarf")
    
    # Always keep these on
    wasd_bind.wasd_bind_template.add_toggle_on_power("sprint")
    wasd_bind.wasd_bind_template.add_toggle_on_power("super speed")
    
    # Rotate through different shields
    wasd_bind.wasd_bind_template.add_toggle_on_power_pool([
        "gravity shield", "penumbral shield", "twilight shield"
    ])
    
    wasd_bind.publish_bind_files("warshade_binds", "binds")

**Multiple Auto-Cast Powers** (Perfect for Dominators)

.. code-block:: python

    from CityOfBinds import WASDRotatingBind

    wasd_bind = WASDRotatingBind()
    
    # Rotate through multiple auto powers
    wasd_bind.wasd_bind_template.add_auto_power_pool([
        "hasten", "domination", "inner inspiration"
    ])
    
    wasd_bind.publish_bind_files("dominator_autos", "binds")

📋 Dependencies
~~~~~~~~~~~~~~~

- Python 3.9 or higher
- networkx (automatically installed)

🔧 Development Setup
~~~~~~~~~~~~~~~~~~~~

If you want to contribute or modify the library:

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/yourusername/city-of-binds.git
    cd city-of-binds

    # Install in development mode with dev dependencies
    pip install -e ".[dev]"

    # Run tests
    pytest

    # Format code
    black .
    isort .

🎯 Core Features
~~~~~~~~~~~~~~~~

**Bind Types**
- ``Bind``: Single key binds with commands
- ``WASDBind``: Movement key binds with power management
- ``WASDRotatingBind``: Advanced rotating power sequences
- ``RotatingBind``: Custom rotation sequences
- ``RandomBinds``: Randomized power selection

**Power Management**
- Toggle powers on/off automatically
- Auto-cast power rotation
- Power pools for cycling through options
- Persistent power states through movement

**File Generation**
- Automatic bind file creation
- Proper file linking for rotations
- Customizable folder organization
- Ready-to-use in City of Heroes

🎮 How It Works in Game
~~~~~~~~~~~~~~~~~~~~~~~

1. **Generate bind files** using this library
2. **Copy files** to your City of Heroes directory
3. **Load in-game** with ``/bindloadfile path/to/your/0.txt``
4. **Play normally** - powers activate automatically as you move!

The library creates multiple bind files that link to each other, creating smooth rotations and automations that work seamlessly in City of Heroes.

📖 Advanced Usage
~~~~~~~~~~~~~~~~~

**Custom Triggers and Conditions**

.. code-block:: python

    from CityOfBinds import Bind, BindFile

    # Create custom binds
    bind = Bind(
        key="F1",
        slash_commands=["team Hello team!", "powexec_auto hasten"]
    )

    # Add to bind file
    bind_file = BindFile()
    bind_file.add_bind(bind)

**File Organization**

.. code-block:: python

    # Organize binds in folders
    wasd_bind.publish_bind_files(
        parent_folder_name="my_character_name",
        directory="C:/Games/City of Heroes/binds"
    )

📄 License
~~~~~~~~~~

This project is licensed under the MIT License - see the LICENSE file for details.

🤝 Contributing
~~~~~~~~~~~~~~~

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

🐛 Issues and Support
~~~~~~~~~~~~~~~~~~~~

If you encounter any issues or have questions:

1. Check the examples in the ``tests/examples/`` directory
2. Open an issue on GitHub with your bind configuration
3. Include the error message and your Python version

🎊 Acknowledgments
~~~~~~~~~~~~~~~~~

Created for the City of Heroes community. Special thanks to all the players who helped test and provide feedback on complex bind scenarios.

---

*City of Heroes is a trademark of NC Interactive, LLC. This project is not affiliated with or endorsed by NC Interactive, LLC.*
