from pluginmanager.pluginmanager import register_plugin, plugin 
import re

class JanKenoJannsen(plugin):
  
  name = 'Jan Keno Jannsen'
  permissions = [False,True] # 0: Match on Private Message | 1: Match on Group Chat
  
  words = "" 

  def plugin_init():
    global words
    wordlist = []
    for line in open('pluginmanager/plugins/jan-keno_janssen.txt', 'r'):
      wordlist += [ ' '.join(line.split()) ] 
    words = "|".join(wordlist)

  def match(message):
    global words
    return re.search(words,message,re.IGNORECASE)

  def send_message(nick):
    return "Jan-Keno Janssen regt das auf!"

  def help():
    return "Write a Jan-Keno Jannsen word like these" + ",".join(wordlist)

register_plugin(JanKenoJannsen)

