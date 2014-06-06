from pluginmanager.pluginmanager import register_plugin, plugin
from databasemanager.boten_anna_db import boten_anna_db
from bs4 import BeautifulSoup
import urllib.request

class WebsiteTitleGrabber(plugin):
   
    name = 'Website Title Grabber'

    # 0: Match on Private Messages | 1: Match on Group Chat
    permissions = [False,True]
  
    def plugin_init():
        DatabaseLayer.init_db()

    def match():
        return 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def send_message(message,match,nick):
        range_url = match.span()
        message_without_url = message[0:range_url[0]] + message[range_url[1]+1:len(message)]
        url = str(message[range_url[0]:range_url[1]])
        return WebsiteTitleGrabber.get_url_page_title(message_without_url,url,nick)

    def get_url_page_title(message,url,nick):

        '''  
        Opens the URL and returns the page title from the given url page
        :return the page title
        '''
        is_duplicated, uid, stored_page_title, stored_message, stored_nick, timestamp = WebsiteTitleGrabber.check_duplicated(url)
        if is_duplicated and stored_nick:
            output = "(" + stored_page_title + ") " + nick + " du BOB! " + stored_nick + " hat das bereits am: " + timestamp
            if len(stored_message) > 0:
                output += " mit der Nachricht: " + stored_message
            return output + " gepostet (!link "+str(uid)+")"

        try:
            page = urllib.request.urlopen(url)
            if not page:
                raise Exception()

            buf = page.read();
            if not buf:
                raise Exception()

            soup = BeautifulSoup(buf)
            if not soup:
                raise Exception()

            page_raw_title = soup.title

            if not page_raw_title:
                raise Exception()

            page_title = page_raw_title.string

            if len(page_title) == 0:
                page_title = ['Das leckere Sueppchen konnte kein <title>-Tag finden! :(']

        except:
            if buf:
                page_title = 'Das leckere Sueppchen konnte kein <title>-Tag finden, da es sich um keine HTML Seite handelt!'
            else:
                return "Die URL %s ist toootaaal komisch!" % url
    
        uid = WebsiteTitleGrabber.save_url(url,page_title,message,nick)

        return page_title + " (!link "+str(uid)+")"

    def check_duplicated(url):

        """
        Check duplicated URL
        :return bool, uid, page title, message, user, time
        """
        data = DatabaseLayer.search_duplicated(url)
        if data != None:
            return True, data[0], data[1], data[2], data[3], data[4]
        else:
            return False, None, None, None, None, None

    def save_url(url,url_page_title,message,user):
        """
        Save URL in Database
        """
        return DatabaseLayer.insert(url,url_page_title,message,user)

    def help():
        return 'Store links in database, pattern: http://www.url.tld/something/somepage.html#anchor or http://127.0.0.1/s/sp.html#anchor' 

register_plugin(WebsiteTitleGrabber,True)

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

    def insert(links, page_title, message, user):
        data = [links, page_title, message, user]
        return DatabaseLayer.db.insert(['url','page_title','message,user'],'url',data)

    def search_duplicated(url):
        return DatabaseLayer.db.search(['uid','page_title','message','user','timestamp'],'url','url=?',[url])
