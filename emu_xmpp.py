#!/usr/bin/env python
import sys
import re
from pluginmanager.pluginmanager import features, plugins

def init_plugins():
    for plugin in plugins:
        plugin.plugin_init()
        print("Plugin registered: %s" % plugin.name)

    for feature in features:
        feature.plugin_init()
        print("Feature registered: %s" % feature.name)

def get_message(message,nick,is_private_message):
    """
    Receives a message from all features and one from the first matching plugin
    :param message: Message received from XMPP chat
    :param nick: Nick which sends the message
    :param is_private_message: Message received from normal chat or muc? 

    :return response: Answers from Boten Anna
    """
    if is_private_message and re.search('^!help',message,re.IGNORECASE) != None:
        msg = message.rstrip().split(' ',1)
        if len(msg) < 2 or re.search('^help$',msg[1],re.IGNORECASE) !=None:
            return '!help <plugin>'

        return pluginhelp(msg[1])

    response = ""
    # Feature based plugins
    for feature in features:
        if is_private_message != feature.permissions[0] and not is_private_message != feature.permissions[1]:
            continue
        # Find matching
        match = re.search(feature.match(),message,re.IGNORECASE)
        if match != None:
            # Receives message from feature
            response += feature.send_message(message,match,nick) + '\n'

    # Plugin based plugins
    for plugin in plugins:
        if is_private_message != plugin.permissions[0] and not is_private_message != plugin.permissions[1]:
            continue
        # Find matching
        match = re.search(plugin.match(),message,re.IGNORECASE)
        if match != None:
            # Receives message from plugin
            response += plugin.send_message(message,match,nick) + '\n'
            return response[:-1] # without \n
    return response[:-1] # without \n

def pluginhelp(message):
    for allPlugins in plugins, features:
        for plugin in allPlugins:
            try:
                if re.search('^%s$' % plugin.name,message,re.IGNORECASE) != None:
                    return plugin.help()
                if re.search(plugin.match(),message,re.IGNORECASE) != None:
                    return plugin.help()
            except:
                return 'Plugin error, something went wrong :('

    return 'No Plugin "%s" found ...' % message 

print("===== Plugin Tester ======")
init_plugins()
print("==========================")
print("Private messages: 'p:Your message'")
print("Group messages: 'g:Your message'")
print("==========================")
print("OK? Lets start, type:")

while(1):
    message = sys.stdin.readline()
    
    message = message.rstrip().split(':',1)

    is_private_message = False
    if len(message) > 1:
        if message[0] == 'p' or message[0] == 'P':
            is_private_message = True
        message = message[1]
    else:
        message = message[0]

    if message == 'quit' or message == 'exit':
        print('Bye ...')
        break 

    print("Boten Anna: %s" % get_message(message,'TestUser',is_private_message))
