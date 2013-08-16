from pluginmanager.pluginmanager import register_plugin, plugin
from databasemanager.boten_anna_db import boten_anna_db

class Links(plugin):
   
    name = 'Links'

    # 0: Match on Private Messages | 1: Match on Group Chat
    permissions = [True,False]
  
    def plugin_init():
        DatabaseLayer.init_db()

    def match():
        return '^!links'

    def send_message(message,match,nick):
        msg = message.split(' ',1)
        if len(msg) > 1:
            msg = msg[1].split(' ')
            if msg[0].isdecimal():
              if len(msg) > 1 and msg[1].isdecimal():
                links = DatabaseLayer.get_links_in_range(msg[0],msg[1])
              else:
                links = DatabaseLayer.get_links_in_range(0,msg[0])
            else:
              links = DatabaseLayer.get_links_by_nick(msg)
        else:
            links = DatabaseLayer.get_links()

        response  = ""
        for link in links:
            response += "\n"
            for column in link:
                response += str(column) + " - "
            response = response[:len(response)-3]
        return response 

    def help():
        return '!links - Show all stored links with message, time and nick' 

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
    
    def get_links_by_nick(nick):
        placeholders = DatabaseLayer.__generate_values(len(nick))
        return DatabaseLayer.db.search(['*'], 'url',placeholders,nick,True)

    def get_links_in_range(begin,end):
        return DatabaseLayer.db.search(['*'],'url','uid between ? and ?',[begin,end],True)

    """ 
    Help function to generate search values placeholder for given fields user=? or user=? 
    :param int size: How many placeholders should I create, sir?
    """
    def __generate_values(size):
        values=""
        for i in range(0,size):
            values +='user=? or '
        return values[:-4] #without or
