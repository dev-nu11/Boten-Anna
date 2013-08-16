from pluginmanager.pluginmanager import register_plugin, plugin

class Next(plugin):
   
  name = 'Next'
 
  # 0: Match on Private Messages | 1: Match on Group Chat   
  permissions = [True,True]  

  def plugin_init():
    pass

  def match():
    return '^!next' 

  def send_message(message,match,nick):
    return 'Another satisfied customer! NEXT!'

register_plugin(Next)
