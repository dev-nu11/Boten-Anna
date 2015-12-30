from pluginmanager.pluginmanager import register_plugin, plugin
from bs4 import BeautifulSoup
import urllib.request
import re
import logging
import sqlite3

class WebsiteTitleGrabber(plugin):
    name = 'Website Title Grabber'
    db = None

    def plugin_init():
        WebsiteTitleGrabber.db = LinkDatabase()

    def match():
        return "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    def send_message(message, match, nick):
        range_url = match.span()
        message_without_url = message[0:range_url[0]] + message[range_url[1]+1:len
(message)]
        url = str(message[range_url[0]:range_url[1]])
        return WebsiteTitleGrabber.grabTitle(message_without_url, url, nick)

    def grabTitle(message_without_url, url, nick):
        print("First check url for duplicate")
        result = WebsiteTitleGrabber.check_for_duplicate(url, nick)
        print("Finished check url for duplicate")
        if result['is_duplicated']:
            print("Is duplicate, inform user")
            return result['reply']
        try:
            print("Open URL")
            page = urllib.request.urlopen(url)

            if not page:
                raise Exception()

        except:
            logging.warn("Failed opening URL")
            return "Schäm dich du hast Anna weh getan. Der Link was auch immer das war, wurde nicht gespeichert."

        if not re.search('^text/html.*$',page.headers["Content-Type"],re.IGNORECASE):
            page_title = "Cyber Cyber Cyber ... kein <title>-Tag, da %s. Ich speichere die URL trotzdem mal." % page.headers["Content-Type"]

            WebsiteTitleGrabber.db.save_url(url, page_title, message_without_url, nick)
            return page_title

        page_size = page.headers["Content-Length"]

        if page_size and int (page_size) > 500000:
            page_title = "Cyber Cyber Cyber ... dat Ding scheint mega zu sein. Es ist %s Byte oder so gross. Ich speichere die URL trotzdem mal." % page.headers["Content-Length"]
            WebsiteTitleGrabber.db.save_url(url, page_title, message_without_url, nick)
            return page_title

        try:
            buf = page.read();
            
            if not buf:
                raise Exception()
    
        except:
            logging.warn("Failed downloading URL")
            return "Schäm dich du hast Anna weh getan. Beim downloaded des Links ist was übelst schief gegangen. Der Link oder was auch immer das war, wurde nicht gespeichert."

        try:
            soup = BeautifulSoup(buf, "html.parser")
            if not soup:
                raise Exception()

            page_raw_title = soup.title

            if not page_raw_title:
                raise Exception()

            page_title = page_raw_title.string

            if len(page_title) == 0:
                raise Exception()

            page_title = page_title.rstrip()

        except:
            page_title = 'Kein <title>-Tag'

        WebsiteTitleGrabber.db.save_url(url, page_title, message_without_url, nick)
        return page_title

    def check_for_duplicate(url, nick):
        """
         Check duplicated URL
         :return bool, uid, page title, message, user, time
        'uid','page_title','message','user','timestamp'
          0       1            2       3       4
        """
        data = WebsiteTitleGrabber.db.search_for_duplicated(url)
        if data is None:
            return dict(is_duplicated = False, reply = "")
        else:
            if len(data[1]) <= 0 or len(nick) <= 0:
                    return dict(is_duplicated=False, reply="")
            else:
                if len(data[2]) > 0:
                    stored_message = data[2]
                else:
                    stored_message = "- Keine -"

                return dict(is_duplicated = True, reply = "%s du BoB! %s hat den Link: %s mit dem Titel: %s bereits %s geposted. Die Nachricht lautete %s" % (nick, data[3], url, data[1], data[4], stored_message))

register_plugin(WebsiteTitleGrabber, True)

class LinkDatabase:
    
    db = None

    def __init__(self):
        logging.info("Initialized database")
        # Create new database and tables if not exists
        self.conn = sqlite3.connect("boten_anna.db", check_same_thread = False)
        self.__create_table__()

    def __create_table__(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS url (uid integer PRIMARY KEY, url text, page_title text, message text, user text, timestamp datetime default current_timestamp)")
        return self.conn.commit()

    def __insert__(self, fields, table, data):
        """
        Insert data in given table
        :param list fields: name of fields in which data should be inserted
        :param str  table: name of the table
        :param list data: data / values for fields
        """
        if fields == None or table == None:
            return False

        c = self.conn.cursor()
        c.execute("INSERT INTO url (%s) VALUES %s " % (','.join(fields), self.__generate_values__(len(data))), data)

        self.conn.commit()

    def __select__(self, fields, table, fetchall=True):
        """
        Select data in given table
        :param list fields: name of fields
        :param str  table: name of the table
        :param bool fetchall: returns the result of all found data or returns only
    the first result?
        """
        if fields == None or table == None:
            return False

        c = self.conn.cursor()
        query = c.execute("SELECT %s FROM url" % ','.join(fields))
        
        if fetchall:
            return query.fetchall()
        else:
            return query.fetchone()

    def search(self, fields, table, search_param, data, fetchall=False):
        """
        Search data in given table
        :param list fields: name of fields which should selected 
        :param str  table: name of the table
        :param str  search_param: python sqlite3 param search (example: 'uid=?')
        :param list data: data which fill the search_param placeholders with data
        :param bool fetchall: returns the result of all found data or returns only
    the first result?
        """
        if fields == None or table == None:
            return False

        c = self.conn.cursor()
        query = c.execute("SELECT %s FROM url WHERE %s" % (','.join(fields), search_param), data)

        if fetchall:
            return query.fetchall()
        else:
            return query.fetchone()

    def __generate_values__(self, size):
        """
        Help function to generate values placeholder for given fields (?,?,?) 
        :param int size: How many placeholders should I create, sir?
        """
        values = "("
        for i in range(0,size-1):
            values +='?,'
        values += '?)' 
        return values

    def __del__(self):
        """
        Destructor: Close db connection
        """
        c = self.conn.cursor()
        c.close()

    def search_for_duplicated(self, url):
        return self.search(['uid','page_title','message','user','timestamp'],'url','url=?',[url])

    def save_url(self, links, page_title, message, user):
        data = [links, page_title, message, user]
        return self.__insert__(['url','page_title','message,user'],'url',data)
