from pluginmanager.pluginmanager import register_plugin, plugin 

class JanKenoJanssen(plugin):
    
    name = 'Jan-Keno Janssen'

    def plugin_init():
        JanKenoJanssen.wordlist = set() 
        for line in open('pluginmanager/plugins/jan-keno_janssen.txt', 'r'):
            JanKenoJanssen.wordlist.add(''.join(line.split()))
        filter("", JanKenoJanssen.wordlist)
        JanKenoJanssen.words = '(^|\s+)('
        JanKenoJanssen.words += "|".join(JanKenoJanssen.wordlist)
        JanKenoJanssen.words += ')'
    def match():
        return JanKenoJanssen.words

    def send_message(message, match, nick):
        return "Jan-Keno Janssen regt das auf! - http://i.imgur.com/rO22R9u.png"

    def help():
        return "Write a Jan-Keno Janssen word like these " + ", ".join(JanKenoJanssen.wordlist)

register_plugin(JanKenoJanssen, True)
