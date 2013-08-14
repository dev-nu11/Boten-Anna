from pluginmanager.pluginmanager import register_plugin, plugin
from databasemanager.boten_anna_db import boten_anna_db

class Links(plugin):
   
    name = 'Get Links'

    # 0: Match on Private Messages | 1: Match on Group Chat
    permissions = [True,False]
  
    def plugin_init():
        DatabaseLayer.init_db()

    def match():
        return '^!links'

    def send_message(message,match,nick):
        links = DatabaseLayer.get_links()
        response  = ""
        for link in links:
            response += "\n"
            for column in link:
                response += str(column) + " - "
            response = response[:len(response)-3]
        return response 

    def help():
        pass

register_plugin(Links)

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

    def get_links():
        return DatabaseLayer.db.select(['*'],'url')
