plugins = set() 
features = set()

def register_plugin(plugin,is_feature=False):
    """
    Registers a new plugin oder feature
    :param plugin plugin: plugin class to register / store
    :param bool is_feature: plugin or feature based?
    """
    if is_feature:
        global features
        features.add(plugin)
    else:
        global plugins
        plugins.add(plugin) 

class plugin(object):
    """
    Abstract plugin base class.
    """
    name = 'Plugin name'

    # 0: Match on private messages | 1: Match on groupchat
    permissions = [True,True]  

    def plugin_init():
        pass

    def match():
        pass   

    def send_message(message,match,nick):
        pass

    def help():
        pass
