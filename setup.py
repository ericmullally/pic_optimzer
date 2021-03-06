import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],"include_files":["Main_window.ui", "designer_rc.py", "error_logs", "error_pics"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "pic optimizer",
        version = "0.1",
        description = "optimizes pictures for web distribution",
        options = {"build_exe": build_exe_options},
        executables = [Executable("app.py", base=base, icon = "icons/new convert-photo-to-icon-8.ico")])