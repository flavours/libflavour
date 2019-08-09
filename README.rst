libflavour
===========

Python library to validate and load flavour YAML files for projects and addons.



Usage for a projects::

   from libflavor import load_project
   from pathlib import Path
   
   with Path('/path/to/file.yaml').open() as f:
       load_project(f.read())

Usage for a addon::

   from libflavor import load_addon
   from pathlib import Path
   
   with Path('/path/to/file.yaml').open() as f:
       load_addon(f.read())
