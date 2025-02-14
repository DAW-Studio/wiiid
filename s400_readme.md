# S400 SBRI LaserLockApp

### Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [HotReload Feature](#hotreload-feature)
- [Code Structure](#code-structure)
- [Development Guidelines](#development-guidelines)
- [Colour Palette](#colour-palette)

## Overview  
<!-- Someone else needs to write the description -->
**LaserLockApp** is a GUI-based application built with **PySide6** that...

## Tech Stack  
- **Python** (Version 3.12)  
- **PySide6** (For GUI development)  
- **Pynput** (For [hotreload.py](./utils/hotreload.py#L3), can be removed for release)

## Setup Instructions  
1. **Set up a virtual environment**:  
    ```sh
    python3.12 -m venv LaserLockApp/.venv
    ```
2. **Activate the virtual environment**:
    ```sh
    source LaserLockApp/.venv/bin/activate

    python3 --version
    # Should output Python3.12.x
    ```
3. **Install dependencies**:
    ```sh
    pip install -r LaserLockApp/requirements.txt
    ```
4. **Run the application**:
    ```sh
    cd LaserLockApp
    python3 laserlock.py
    ```

## HotReload Feature
For easier development, I have included a hot reload feature as **PyQt** does not end its process on `KeyboardInterrupt`. The hot reload outputs **stdout** and **stderr** as normal and will not close the current process if the new process starts with an error.
- Press <ctrl+c> to reload the app while running.
- The hotkey is customizable by modifying `hotreload` in [laserlock.py](./laserlock.py#L1000)
    ```python
    hotreload = HotReload(window, hotkey="<ctrl>+s")
    ```

## Code Structure
```
LaserLockApp/
|-- laserlock.py            # Main entry point
|-- assets/                 # Contains style.qss, icons, images
|-- assets/appstyle.qss     # Main style.qss
|-- utils/                  # Utility functions and helpers
|-- components/             # UI components for cards
|-- widgets/                # General widgets (titlebar, tabwidget, graphs, etc.)
|-- requirements.txt        # Dependencies for the project
```

## Development Guidelines
- **Indentation**:
    - Use **4 spaces** per indentation level.
    - **Tabs** (\t) should not be used, only spaces.

- **Blank Lines**:
    - Use **two blank lines** to seperate top-level functions and class definitions.
    - Use **one blank line** to seperate methods inside a class.

- **Imports**:
    - Imports should be on seperate lines.
    - Import should be grouped into three categories in the following order: standard library, third-party, local.
        ```python
        import os
        import sys

        from PySide6.QtWidgets import QApplication

        from utils.hotreload import HotReload
        ```
    - Imports from the same module should be grouped and on separate lines for better readability.
        ```python
        from PySide6.QtWidgets import (
            QApplication,
            QMainWindow,
            QVBoxLayout,
            QLabel,
            QWidget
        )
        ```

- **Naming Conventions**:
    - Use **snake_case** for variables.
    - Use **camelCase** for functions.
    - Use **PascalCase** for classes.
    - Use **UPPER_CASE** for constants.
    ```python
    MY_CONSTANT = 100


    class MyClass:
        def myFunction():
            my_variable = 10
    ```

- **Functions**:
    - Provide docstrings for functions.
    - Arguments should have **type hints**.
    - Functions should have **return types**.
    ```python
    def getFoo(self, foo_name: str) -> Foo:
        """Returns foo from `self.bars`."""
        return self.bars[foo_name]
    ```

- **Styling**:
    - Use **.qss** files to set the style sheet of widgets.
    ### style.qss
    ```css
    background-color: black;
    color: white;
    border: 1px solid grey;
    border-radius: 10px;
    ```
    ### code.py
    ```python
    # Correct:
    with open("style.qss", "r") as file:
        stylesheet = file.read()
        widget.setStyleSheet(stylesheet)

    button.setObjectName("btn")

    # Incorrect:
    button.setStyleSheet("""
        background-color: black;
        color: white;
        border: 1px solid grey;
        border-radius: 10px;
    """)
    ```

## Colour Palette (WIP)

#### Background
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
    <div style="display: flex; align-items: center;">
        <div style="background-color: #171B24; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#171B24</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background-color: #1E232E; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#1E232E</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background-color: #323A4C; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#323A4C</span>
    </div>
</div>

#### Text
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
    <div style="display: flex; align-items: center;">
        <div style="background-color: #848589; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#848589</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background-color: #AFB0B3; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#AFB0B3</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background-color: #FFFFFF; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#FFFFFF</span>
    </div>
</div>

#### Border
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;">
    <div style="display: flex; align-items: center;">
        <div style="background-color: #53596D; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#53596D</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background-color: #53596D; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#53596D</span>
    </div>
    <div style="display: flex; align-items: center;">
        <div style="background-color: #53596D; width: 50px; height: 50px; border-radius: 10px;"></div>
        <span style="margin-left: 10px;">#53596D</span>
    </div>
</div>
