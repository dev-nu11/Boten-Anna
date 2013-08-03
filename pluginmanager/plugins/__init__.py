import pluginmanager.pluginmanager
from pluginmanager.plugins.say_hello import fooplugin

pluginmanager.pluginmanager.register_plugin(fooplugin)
print("HELLO")
