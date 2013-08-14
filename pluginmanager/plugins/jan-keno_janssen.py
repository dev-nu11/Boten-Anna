from pluginmanager.pluginmanager import register_plugin, plugin 

class JanKenoJanssen(plugin):
    
    name = 'Jan-Keno Janssen'

    # 0: Match on Private Message | 1: Match on Group Chat
    permissions = [True,True]
  
    words = "" 

    def plugin_init():
        wordlist = set() 
        for line in open('pluginmanager/plugins/jan-keno_janssen.txt', 'r'):
            wordlist.add(' '.join(line.split()))
        JanKenoJanssen.words = '(^|\s+)('
        JanKenoJanssen.words += "|".join(wordlist)
        JanKenoJanssen.words += ')'
    def match():
        return JanKenoJanssen.words

    def send_message(message,match,nick):
        return "Jan-Keno Janssen regt das auf! - http://i.imgur.com/rO22R9u.png"

    def help():
        return "Write a Jan-Keno Janssen word like these" + ",".join(wordlist)

register_plugin(JanKenoJanssen)
