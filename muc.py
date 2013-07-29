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

# Deps for reading the messages and save links into db
import re
import urllib.request
from boten_anna_db import boten_anna_db

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
    def muc_message(self, msg):
        if msg['mucnick'] != self.nick:

          # Parse Message

          # Contains Message an URL
          url_page_title = get_url_page_title(msg['body'],msg['mucnick'])
          if url_page_title != None:
            self.send_message(mto=msg['from'].bare,
                              mbody= url_page_title,
                              mtype='groupchat')
            return

          # Commands starting with !
          if re.match("^!links",msg['body']):
            self.send_message(mto=msg['from'],
                              mbody=command_links(),
                              mtype='chat')
            return

          if re.match("^!link",msg['body']):
            self.send_message(mto=msg['from'].bare,
                              mbody=command_link(msg['body']),
                              mtype='groupchat')
            return
          l = ['aufregen','regt','dumm','mist','abfuck','dreck','kack','scp','doof','social','credit','points','point','note','leistung','w[u]*t']
          if re.search("|".join(l),msg['body'],re.IGNORECASE) != None:
            self.send_message(mto=msg['from'].bare,
                              mbody="Jan-Keno Janssen regt das auf!",
                              mtype='groupchat')
            return
"""
 Opens the URL and returns the page title from the given url page
 Returns page title
"""
def get_url_page_title(chat,user):
  contains_url, url, message = has_url(chat)

  if contains_url == False:
    return None

  try:
    byte_content = urllib.request.urlopen(url)
    content = byte_content.read()
    content = detect_decoding(content)
    page_title = re.findall(r'<title>(.*?)</title>',content,re.DOTALL)
    if len(page_title) == 0:
      page_title = ['Dieser Link besitzt kein title tag! :)']
  except:
    return "Die URL %s ist irgendwie komisch!" % url

  duplicated, uid, old_page_title, old_message, submitted_user, time = check_duplicated(str(url))

  if duplicated == False:
    uid = save_url(str(url),str(page_title[0]).rstrip(),str(message),str(user))
    return str(page_title[0]).rstrip() + " (!link "+str(uid)+" )"
  else:
    output = "(" + old_page_title + ") " + user + " du BOB! " + submitted_user + " hat das bereits am: " + time
    if len(old_message) > 0:
      output += " mit der Nachricht: " + old_message
    return output + " gepostet (!link "+str(uid)+")"

"""
Try to find the right decoding ...
"""
def detect_decoding(content):
  try:
    return content.decode("utf-8")
  except UnicodeDecodeError:
    pass

  try:
    return content.decode("ISO-8859-15")
  except UnicodeDecodeError:
    pass

  return str(content)

"""
 Check if a given message contains an URL (RFC 1808)
 Returns Boolean, URL, Message
"""
def has_url(message):

  # Search URL Pattern (RFC 1808)
  contains_url = re.search('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)

  if contains_url == None:
    return False, None, None

  range_url = contains_url.span()

  return True, message[range_url[0]:range_url[1]], message[0:range_url[0]] + message[range_url[1]+1:len(message)]

"""
 Check duplicated URL
 returns boolean, uid, page title, message, user, time
"""
def check_duplicated(url):
  db = boten_anna_db()
  data = db.search_duplicated(url)
  if data != None:
    return True, data[0], data[1], data[2], data[3], data[4]
  else:
    return False, None, None, None, None, None

"""
 Save URL in Database
"""
def save_url(url,url_page_title,message,user):
  db = boten_anna_db()
  return db.insert(url,url_page_title,message,user)

"""
 Get specific link
"""
def command_link(message):
  message_without_command = message[5:len(message)]

  uid_list = re.findall('\d+',message_without_command)
  db = boten_anna_db()
  message = ""

  for uid in uid_list:
    # data contains url, page_title, message and user
    data = db.search_uid(uid)
    if data != None:
      message += "\n" + data[0] + " ("+data[1]+")"
      if len(data[2]) > 0:
        message += ": " + data[2]
      message += " - " + data[3]

  return message

"""
 Get all links from db
 Returns formatted message
"""
def command_links():
  db = boten_anna_db()
  links = db.get_links()
  message = ""
  for link in links:
    message += "\n"
    for column in link:
      message += str(column) + " - "
    message = message[:len(message)-3]
  return message

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
