from pluginmanager.pluginmanager import register_plugin, plugin 

class JanKenoJannsen(plugin):
  
  name = 'Jan Keno Jannsen'
  permissions = [True,True] # 0: Match on Private Message | 1: Match on Group Chat
  
  words = "" 

  def plugin_init():
    wordlist = []
    for line in open('pluginmanager/plugins/jan-keno_janssen.txt', 'r'):
      wordlist += [ ' '.join(line.split()) ] 
    JanKenoJannsen.words = "|".join(wordlist)

  def match():
    return JanKenoJannsen.words

  def send_message(message,match,nick):
    return "Jan-Keno Janssen regt das auf! - http://i.imgur.com/rO22R9u.png"

  def help():
    return "Write a Jan-Keno Jannsen word like these" + ",".join(wordlist)

register_plugin(JanKenoJannsen,True)
