# -*- coding: utf-8 -*-

"""sitecustomize for autoinstallation.

This script is to be installed in the Python installation's "sitecustomize.py"
(which may or may not previously exist).

To find the installation directory, enter this into a Python prompt:

>>> import site
>>> print(site.getusersitepackages())

Open (or create) "sitecustomize.py" in this directory insert the code below.
Some parts of the directory path may also need to be created.

"""

##############################################################################
# IMPORTS

import sys


##############################################################################
# FUNCTION

def handle_import_exception(exc_type, exc_value, exc_traceback):
    """handle_import_exception.

    Change how ModuleNotFoundError behaves
    Now ModuleNotFoundError will try to install the missing module.

    """
    if exc_type.__name__ == "ModuleNotFoundError":

        import __main__
        import subprocess
        import importlib

        # --------------------------------------------------------------------
        # Configuration Options

        # whether to ask to install a package
        ASK_TO_INSTALL = True

        # set to 'True' if you need to use 'sudo' to "pip install" packages
        USES_SUDO = False

        # --------------------------------------------------------------------

        debug_mode = False

        # Are we running in the interactive interpreter?
        interactive_mode = not hasattr(__main__, '__file__')

        # get module name; exception string is in the form
        # "No module named 'xxx'"
        module_name = str(exc_value).split("'")[1]

        if ASK_TO_INSTALL:
            print((f"Your script requires the package '{module_name}',"
                   " but you don't have it installed."))

            ans = input("Would you like me to try to install it (y/n)? ")
            if ans.lower() == 'y':
                pass
            else:
                print(("OK! Here's the command "
                       "if you want to do it on your own:\n"))
                install_command = f"pip install {module_name} --user"
                if USES_SUDO:
                    print("sudo " + install_command)
                else:
                    print(install_command, "", sep='\n')
                sys.exit(0)
        else:
            print((f"\nThe package '{module_name}' is not installed..."
                   " attempting installation."))
        # /if

        commands = ["pip", "install", f"{module_name}", "--user"]
        # commands = ["conda", "install", f"{module_name}", '--yes']
        if USES_SUDO:
            commands.insert(0, "/usr/bin/sudo")

        with subprocess.Popen(commands, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              bufsize=1, universal_newlines=True) as p:
            out, err = p.communicate()

        # debugging
        if debug_mode:
            print("--- stdout")
            print(out)
            print("--- stderr")
            print(err)
            print("---")

        if (("ERROR: Could not find a version" in err) or
                ("ERROR: No matching distribution" in err)):
            print(
                f"Sorry, pip could not find a package named {module_name}.\n")
            sys.exit(0)

        elif "Successfully installed" in out:
            # should be installed now; try again
            try:
                importlib.import_module(f'{module_name}')
            except ModuleNotFoundError:
                print("\nSorry, the package installation failed. :(",
                      "Here are the messages to help debug: ",
                      out, err,
                      sep='\n')
                sys.exit(0)

            print((f"The package '{module_name}' was sucessfully installed;"
                   " please rerun your script.\n"))

        else:
            print("\nSorry, the package installation failed. :(",
                  "Here are the messages to help debug: ",
                  out, err,
                  sep='\n')
            sys.exit(0)

sys.excepthook = handle_import_exception
# /def  # needed by setup.py to locate end of code

##############################################################################
# END
