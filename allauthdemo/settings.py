"""All settings in this demo are written to settings_generated.py

In a real project, you could start by copying the settings_generated.py file
over this file.
"""
try:
    from allauthdemo.settings_generated import *
except ImportError:
    import sys
    sys.stderr.write("ERROR: No settings found. Please run 'make configure' first.\n\n")
    sys.exit(1)
