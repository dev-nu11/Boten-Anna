import pkgutil
import imp
import os

plugin_path = [os.path.join(__path__[0], "plugins/")]
for loader, name, ispkg in pkgutil.iter_modules(plugin_path):
    file, pathname, desc = imp.find_module(name, plugin_path)
    imp.load_module(name, file, pathname, desc)
