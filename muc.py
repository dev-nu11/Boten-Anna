#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
"""

"""
    Boten Anna
    Boten Anna MUC is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Copyright (C) 2013 H8H https://github.com/h8h
"""

import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp

# Pluginmanager with plugins 
from pluginmanager.pluginmanager import features, plugins
import re
# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


"""
Boten Anna - a simple XMPP MUC Bot
"""
class MUCBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        for plugin in plugins:
          plugin.plugin_init()
          print("Plugin registered: %s" % plugin.name)

        for feature in features:
          feature.plugin_init()
          print("Feature registered: %s" % feature.name)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("message", self.message)

    """
      Process the session_start event.

      Typical actions for the session_start event are
      requesting the roster and broadcasting an initial
      presence stanza.

      Arguments:
          event -- An empty dictionary. The session_start
                   event does not provide any additional
                   data.
    """
    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    """
     Process incoming message stanzas from any chat room. Be aware
     that if you also have any handlers for the 'message' event,
     message stanzas may be processed by both handlers, so check
     the 'type' attribute when using a 'message' event handler.

     Arguments:
        msg -- The received message stanza. See the documentation
               for stanza objects and the Message stanza to see
               how it may be used.
    """
    def message(self, msg):
        
      if msg['type'] in ('chat', 'normal'):
        msg.reply(self.get_message(msg['body'],msg['mucnick'],True)).send()
        return

      if msg['mucnick'] != self.nick:
        self.send_message(mto=msg['from'].bare,
                          mbody=self.get_message(msg['body'],msg['mucnick'],False), 
                          mtype='groupchat')

    def get_message(self,message,nick,is_private_message):
      response = ""
      for feature in features:
        if is_private_message != feature.permissions[0] and not is_private_message != feature.permissions[1]:
           continue
        try:
           match = re.search(feature.match(),message,re.IGNORECASE)
           if match != None:
              response += feature.send_message(message,match,nick) + '\n'
        except:
           print('ERROR in Feature: ' + feature.name + ' '  + str(sys.exc_info()[0]))

      for plugin in plugins:
        if is_private_message != plugin.permissions[0] and not is_private_message != plugin.permissions[1]:
           continue
        try:
           match = re.search(plugin.match(),message,re.IGNORECASE)
           if match != None:
              response += plugin.send_message(message,match,nick) + '\n'
              return response[:-1] 
        except:
           print('ERROR in Plugin: ' + plugin.name + ' ' + str(sys.exc_info()[0]))

        return response[:-1]

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
