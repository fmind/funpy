# Configuration file for ipython.

from traitlets.config import get_config

c = get_config()

c.TerminalIPythonApp.force_interact = True

c.TerminalInteractiveShell.colors = "Linux"
c.TerminalInteractiveShell.editing_mode = "vi"
c.TerminalInteractiveShell.confirm_exit = False

c.InteractiveShellApp.extensions = ["autoreload"]
c.InteractiveShellApp.exec_lines = ["%autoreload 2"]

c.TerminalInteractiveShell.extra_open_editor_shortcuts = True
