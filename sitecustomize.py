import sys

# This script is to be installed in the Python installation's "sitecustomize.py" file
# (which may or may not previously exist).
#
# To find the directory where this file belongs, enter this into a Python prompt:
#
# import site
# print(site.getusersitepackages())
# 
# Open (or create) "sitecustomize.py" in this directory and place the code below. Some
# parts of the directory path may also need to be created.
#

def handle_import_exception(exc_type, exc_value, exc_traceback):

	if exc_type.__name__ == "ModuleNotFoundError":
		import __main__
		import subprocess

		# ---------------------
		# Configuration Options
		# ----------------------------------------------------------------------------------
		# change this to set whether to ask to install a package or just attempt it directly
		ask_to_install = False
		
		# set this to 'True' if you need to use 'sudo' to "pip install" packages
		uses_sudo = True
		# ----------------------------------------------------------------------------------

		debug_mode = False

		# Are we running in the interactive interpreter?
		interactive_mode = not hasattr(__main__, '__file__')
		
		# get module name; exception string is in the form
		# "No module named 'xxx'"
		module_name = str(exc_value).split("'")[1]

		if ask_to_install:
			print(f"Your script requires the package '{module_name}', but you don't have it installed.")
			ans = input("Would you like me to try to install it (y/n)? ")
			if ans.lower() == 'y':
				pass
			else:
				print("OK! Here's the command if you want to do it on your own:")
				print("")
				install_command = f"pip install {module_name}"
				if uses_sudo:
					print("sudo " + install_command)
				else:
					print(install_command)
				print("")
				sys.exit(0)
		else:
			print(f"\nThe package '{module_name}' is not installed... attempting installation.")
		
		commands = ["pip", "install", f"{module_name}"] # "--user" after 'install'
		if uses_sudo:
			commands.insert(0, "/usr/bin/sudo")

		with subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
							  bufsize=1, universal_newlines=True) as p:
			out, err = p.communicate()

		# debugging
		if debug_mode:
			print("--- stdout")
			print(out)
			print("--- stderr")
			print(err)
			print("---")

		import importlib

		if "ERROR: Could not find a version" in err or "ERROR: No matching distribution" in err:
			print(f"Sorry, pip could not find a package named {module_name}.\n")
			sys.exit(0)
		
		elif "Successfully installed" in out:
			# should be installed now; try again
			try:
				module = importlib.import_module(f'{module_name}')
			except ModuleNotFoundError:
				print("\nSorry, the package installation failed. :(\n")
				print("Here are the messages to help debug: ")
				print(out)
				print(err)
				sys.exit(0)
			
			print(f"The package '{module_name}' was sucessfully installed; please rerun your script.\n")
				
		else:
			print("\nSorry, the package installation failed. :(\n")
			print("Here are the messages to help debug: ")
			print(out)
			print(err)
			sys.exit(0)
		
sys.excepthook = handle_import_exception

