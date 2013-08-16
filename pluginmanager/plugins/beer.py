from pluginmanager.pluginmanager import register_plugin, plugin

class Beer(plugin):
   
    name = 'Beer'

    # 0: Match on Private Messages | 1: Match on Group Chat
    permissions = [True,True]   
  
    def plugin_init():
        pass

    def match():
        return '(^|\s+)(b([i]+|e)[e]+r)'

    def send_message(message,match,nick):
        return 'Kein Bier vor vier! - http://i.imgur.com/Bg4vMW3.jpg'

register_plugin(Beer)
