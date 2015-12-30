commands = set() 
noises = set()

def register_plugin(plugin, is_noise_plugin = False):
    """
    Registers a new plugin oder feature
    :param plugin plugin: plugin class to register / store
    :param bool is_feature: plugin or feature based?
    """
    if is_noise_plugin:
        global noises 
        noises.add(plugin)
    else:
        global commands
        commands.add(plugin) 

class plugin(object):
    """
    Abstract plugin base class.
    """
    name = 'Plugin name'

    def plugin_init():
        print("This one")

    def match():
        pass   

    def send_message(message, match, nick):
        pass

    def help():
        return "No help ..." 
