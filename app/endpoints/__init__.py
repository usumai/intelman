import os
import pkgutil
import importlib
from flask import Blueprint

blueprints = []

# Directory of the current package (endpoints)
package_dir = os.path.dirname(__file__)

# Dynamically import all modules in the endpoints package.
for finder, module_name, is_pkg in pkgutil.iter_modules([package_dir]):
    module = importlib.import_module(f"endpoints.{module_name}")
    # Look for instances of Flask Blueprint in the module.
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isinstance(attribute, Blueprint):
            blueprints.append(attribute)
