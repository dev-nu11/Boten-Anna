Boten Anna
===

This is a simple XMPP MUC Bot especially written for thatsapp.org, but you can of course use it for your own purposes :).

Dependency
---
* SleekXMPP (https://github.com/fritzy/SleekXMPP)
* BeautifulSoup4 (https://pypi.python.org/pypi/beautifulsoup4) for the "website_title_grabber" feature-plugin

Features
---
* Plug-in / Feature based
* Persistent data storage (sqlite databases)

Plugin System
---
#### Differences between Plug-in and Features:  
* Features: All come - all serve (example: url matching, funny words responses ...)  
* Plug-ins: First come - first serve (example: commands like !link or !links)  

The plugin system checks all **feature plugins** which match and concatenates them for the response. If you write some feature based-plugin register it with:   
````
register_plugin(My_Feature,True)  
````

For the **plug-in** based plugins the system only searchs for the first plugin which matches and return its response to the chat. The other plug-ins won't be check. You can register it with:  
````
register_plugin(My_Plugin,False)  
````

or  

````
register_plugin(My_Plugin)  
````

#### Template  
````
from pluginmanager.pluginmanager import register_plugin, plugin

class Plug_IN(plugin):
   
  name = 'Greets the nick'
  permissions = [True,True] # 0: Match on Private Messages | 1: Match on Group Chat   
  
  def plugin_init():
    pass

  def match():
    return '^!greet($|\s)'

  def send_message(message,match,nick):
    return 'Hello ' + nick

  def help():
    return 'Some help'

register_plugin(Plug_IN)
````
Put your py-file into the folder *pluginmanager/plugins*  
Test
---
If you only want to test your plugin, just start **emu_xmpp.py**, it doesn't need SleekXMPP and you can test your nice plugin easily :)  
Install
---
* Install SleekXMPP and start muc.py with the following parameters:  
````
python muc.py -j user@jabberid.tld -p secret_password -r room@domain.tld -n nickname  
````

License
---
GPL3 license.
Feel free to use it and even contribute bug fixes or enhancements if you want. Enjoy!
