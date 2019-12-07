# -*- coding: utf-8 -*-

"""astroPHD_module_autoinstaller setup.py.

TODO
----
allow setting the configuration options when install

"""

#############################################################################
# IMPORTS

import os
import site
import shutil


#############################################################################
# SETUP

_SITE_PKG = site.getusersitepackages() + '/sitecustomize.py'

# copy over if file does not exist
if not os.path.exists(_SITE_PKG):
    print('installing...', end=' ')

    shutil.copyfile('./sitecustomize.py', _SITE_PKG)

# have to edit sitecustomize.py
else:
    print('sitecustomize.py exists')

    # --------------------------------------
    # setup

    # read in existing sitecustomize
    file = open(_SITE_PKG, mode='r')
    contents = file.readlines()
    file.close()

    # read in the auto-installer code
    with open('./sitecustomize.py', mode='r') as file:
        autocode = file.readlines()

    # --------------------------------------
    # sys import

    # find if already exists
    sysloc = [i for i, line in enumerate(contents)
              if line.startswith('import sys')]

    # find imports that are not in  a blockquote
    importsloc = []
    in_quote = False
    for i, line in enumerate(contents):
        if (line == '```') or (line == '"""'):  # detect blockquote
            in_quote = ~in_quote  # switch state
        if line.startswith('import') and not in_quote:
            importsloc.append(i)
    if not importsloc:  # no imports, just stick in the first line
        importsloc.append(0)

    # adding `import sys` at first viable import
    if not sysloc:  # empty, need to import sys
        with open(_SITE_PKG, mode='r+') as file:
            for i, line in enumerate(contents):
                file.write(line)
                if i == importsloc[0]:
                    file.write(r'import sys')
                    print('\tinserted `import sys`')
    # /if   # /for

    # --------------------------------------

    hasfunc = [i for i, line in enumerate(contents)
               if line.startswith('def handle_import_exception')]

    funcloc = [i for i, line in enumerate(autocode)
               if (line.startswith('def handle_import_exception') or
                   line.startswith('# /def'))]

    # reopen sitecustomize
    with open(_SITE_PKG, mode='a') as file:
        if not hasfunc:  # empty, need to import sys
            file.write(''.join(autocode[funcloc[0]:funcloc[1] + 1]))

            print('\tappended ModuleNotFoundError excepthook')
# /if

#############################################################################
# CLOSE

print('installed!')


#############################################################################
# END
