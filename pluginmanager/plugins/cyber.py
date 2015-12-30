from pluginmanager.pluginmanager import register_plugin, plugin

class Cyber(plugin):
   
    name = 'Cyber'
  
    def plugin_init():
        pass

    def match():
        return '(^|\s+)cyber'

    def send_message(message, match, nick):
        sp = match.span()
        return 'Cyber Cyber Cyber! Cyber%s - https://youtu.be/WY6KkRsS26M' % message[sp[1]:].rstrip()

register_plugin(Cyber, True)
