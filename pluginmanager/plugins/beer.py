from pluginmanager.pluginmanager import register_plugin, plugin

class Beer(plugin):
   
  name = 'Beer'
  permissions = [True,True] # 0: Match on Private Messages | 1: Match on Group Chat   
  
  def plugin_init():
    pass

  def match():
    return '(^|\s+)(be[e]+r|bier)'

  def send_message(message,match,nick):
    return 'Kein Bier vor vier! - http://i.imgur.com/Bg4vMW3.jpg'

  def help():
    pass

register_plugin(Beer)
