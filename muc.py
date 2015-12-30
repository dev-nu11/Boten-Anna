#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Boten Anna
    Boten Anna MUC is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    Copyright (C) 2015 H8H https://github.com/h8h
"""

import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
import re

'''
 Load the plugins
'''
from pluginmanager.pluginmanager import commands,noises

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input

class MUCBot(sleekxmpp.ClientXMPP):

    """
     Boten Anna - a simple plugin based XMPP MUC Bot using SleekXMPP
    """

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

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
        self.add_event_handler("groupchat_message", self.muc_message)

    def start(self, event):
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
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)
        # Load all commands
        for command in commands:
            command.plugin_init()
            logging.info("Command registered: %s" % command.name)

        # Load all noises
        for noise in noises:
            noise.plugin_init()
            logging.info("Noise registered: %s" % noise.name)

    def muc_message(self, msg):
        '''
        Anna is listening to you
        '''
        if msg['mucnick'] != self.nick:
            self.help_needed(msg)
            res = self.check_commands(msg)
            if res is False:
                self.check_noises(msg) 

    def help_needed(self, msg):
        if re.search('^!help', msg['body'], re.IGNORECASE) != None:
            splitted_body =  msg['body'].rstrip().split(' ', 1)

            if len(splitted_body) < 2 or re.search('^help$', splitted_body[1], re.IGNORECASE) !=None:
                self.send_msg(msg, "!help <plugin>")
            else:
                for plugin in commands:
                    if re.search('^%s$' % plugin.name, ' '.join(splitted_body[1:]), re.IGNORECASE) != None:
                        self.send_msg(msg, plugin.help())
                    elif re.search(plugin.match(), msg['body'], re.IGNORECASE) != None:
                        self.send_msg(msg, plugin.help())

    def check_commands(self, msg):
        # check for commands
        for command in commands:
            match = re.search(command.match(), msg['body'], re.IGNORECASE)
            if match != None:
                self.send_msg(msg, "%s" % command.send_message(msg['body'], match, msg['mucnick']))
                return True
        return False

    def check_noises(self, msg):
        response = ""
        # check for noises
        for noise in noises:
            match = re.search(noise.match(), msg['body'], re.IGNORECASE)
            if match != None:
                response += "%s\n" % noise.send_message(msg['body'], match, msg['mucnick'])
        if len(response) > 0:
            # Response all without leading \n
            self.send_msg(msg, response[:-1])

    def send_msg(self, msg, response):
        self.send_message(mto=msg['from'].bare,
            mbody=response, mtype="groupchat")

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
