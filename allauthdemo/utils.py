import os
"""Handy utils for config"""

def contents(*names):
    """Return string contents from first matching named environment variable
    or file.

    Each name in names is checked first against an environment variable then
    a file. An Exception is raised if nothing matches.
    """
    for name in names:
        if name in os.environ:
            return os.environ[name]

        else:
            name = os.path.expanduser(name)
            if os.path.isfile(name):
                with open(name) as src:
                    return src.read().strip()

    raise Exception("Unresolved content: "+', '.join(names))

