plugins = set() 
features = set()

def register_plugin(plugin,is_feature=False):
  if is_feature:
    global features
    features.add(plugin)
  else:
    global plugins
    plugins.add(plugin) 

class plugin(object):
   """Abstract plugin base class."""

   name = 'Plugin name'
   permissions = [True,True] # 0: Match on Private Messages | 1: Match on Group Chat   

   def plugin_init():
       pass

   def match():
       pass   

   def send_message(message,match,nick):
       pass

   def help():
       pass
