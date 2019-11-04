# Automatically Install Missing Python Modules

This is a hack developed at dotAstronomy 2019 that will attempt to install Python modules that are imported from a script you run, but are missing from your installation. Instead of getting the usual

```
ModuleNotFoundError: No module named 'x'
```

the function will attempt to install the missing package.

This patch works for Python scripts run on the command line as well as the interactive interpreter. When running a script with a missing module the script will need to be rerun after the installation; this is not needed for the interactive interpreter.

## Installation Instructions

1. In your terminal, start Python.
2. Enter the following:

    ```
    import site
    print(site.getusersitepackages())
    ```
3. Open (or `cd` into) the directory returned. It's possible that you may need to create parts of the path.
4. Open the file `sitecustomize.py`. If it's not there, you will need to create it.
5. Paste the contents of the file in this repository called `python_package_autoinstall.py`.
6. Important! Make sure to set the configuration options (see below) specific to your installation.

## Configuration Options

Some variables should be set to reflect your Python environment and preferences. These are at the top of the function `handle_import_exception`:

* `ask_to_install` : Set to `True` if you want to be prompted whether to install package that wasn't found; `False` to try to immediately try to install it.
* `uses_sudo` : Set to `True` if your Python installation requires `sudo` to install packages via pip; set to `False` if your Python is installed in a user-readable location. In other words, if you normally install packages with `sudo pip install xxx`, set this to `True`.

## How It Works

Python has a mechanism to let you set what code is called when certain events occur. This code attaches its own function to the exception hook; in other words, every time an exception is raised, our code will be called.

Our function checks the name of the exception and only does anything if the exception is named `ModuleNotFoundError`. It then gets the name of the package that the script tried to import and run `pip install <package>` on the command line for you.

## Caveats

The function attempts to install missing packages using `pip`. If you have a different package manager, e.g. Anaconda's `conda`, this is will not be used. In general, this is not a problem. Supporting `conda` would be a great update to the code!

