plugins = set() 

def register_plugin(plugin):
  global plugins
  plugins.add(plugin) 

class plugin(object):
   """Abstract plugin base class."""

   name = 'Plugin name'
   permissions = [True,True] # 0: Match on Private Messages | 1: Match on Group Chat   

   def plugin_init():
       pass

   def match(message):
       pass   

   def send_message(nick):
       pass

   def help():
       pass
