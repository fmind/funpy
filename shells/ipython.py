# Configuration file for ipython.

from traitlets.config import get_config

c = get_config()

c.InteractiveShellApp.extensions = ["autoreload"]

c.InteractiveShellApp.exec_lines = [
    "from IPython.lib import deepreload as rl",
    "%autoreload 2",
]

c.TerminalIPythonApp.force_interact = True

c.TerminalInteractiveShell.confirm_exit = False
c.TerminalInteractiveShell.extra_open_editor_shortcuts = True
