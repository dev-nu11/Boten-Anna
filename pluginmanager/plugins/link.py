from pluginmanager.pluginmanager import register_plugin, plugin
from databasemanager.boten_anna_db import boten_anna_db
import re

class Link(plugin):
   
    name = 'Link'

    # 0: Match on Private Messages | 1: Match on Group Chat
    permissions = [True,True]
  
    def plugin_init():
        DatabaseLayer.init_db()

    def match():
        return '^!link(?!s)' 

    def send_message(message,match,nick):
        message_without_command = message[5:len(message)]

        uid_list = re.findall('\d+',message_without_command)
        response = ""

        for uid in uid_list:
            # data contains url, page_title, message and user
            data = DatabaseLayer.search_uid(uid)
            if data != None:
                response += "\n" + data[0] + " ("+data[1]+")"
                if len(data[2]) > 0:
                    response += ": " + data[2]
                response += " - " + data[3]
        return response 

    def help():
        return '!link <link-numbers>, see !links'

register_plugin(Link)

class DatabaseLayer:
  
    db = None
    
    def init_db():
        # Create new database and tables
        DatabaseLayer.db = boten_anna_db("boten_anna.db",'url',['uid integer PRIMARY KEY',
                                                                'url text',
                                                                'page_title text',
                                                                'message text',
                                                                'user text',
                                                                'timestamp datetime default current_timestamp'])

    def search_uid(uid):
        return DatabaseLayer.db.search(['url','page_title','message','user'],'url','uid=?',[uid])
