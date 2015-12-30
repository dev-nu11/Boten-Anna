from pluginmanager.pluginmanager import register_plugin, plugin

class Next(plugin):
   
  name = 'Next'

  def plugin_init():
    pass

  def match():
    return '^!next' 

  def send_message(message, match, nick):
    return 'Another satisfied customer! NEXT!'

register_plugin(Next)
