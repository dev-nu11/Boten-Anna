from pluginmanager.pluginmanager import register_plugin, plugin
from databasemanager.boten_anna_db import boten_anna_db
import re
import urllib.request

class WebsiteTitleGrabber(plugin):
   
  name = 'Website Title Grabber'
  permissions = [False,True] # 0: Match on Private Messages | 1: Match on Group Chat   
  
  def plugin_init():
    DatabaseLayer.init_db()

  def match():
    return 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

  def send_message(message,match,nick):
    range_url = match.span()
    message_without_url = message[0:range_url[0]] + message[range_url[1]+1:len(message)]
    url = str(message[range_url[0]:range_url[1]])

    return WebsiteTitleGrabber.get_url_page_title(message_without_url,url,nick)

  '''  
  Opens the URL and returns the page title from the given url page
  Returns page title
  '''
  def get_url_page_title(message,url,nick):
    is_duplicated, uid, stored_page_title, stored_message, stored_nick, timestamp = WebsiteTitleGrabber.check_duplicated(url)
    if is_duplicated:
      output = "(" + stored_page_title + ") " + nick + " du BOB! " + stored_nick + " hat das bereits am: " + timestamp
      if len(stored_message) > 0:
        output += " mit der Nachricht: " + stored_message
      return output + " gepostet (!link "+str(uid)+")"

    try:
      byte_content = urllib.request.urlopen(url)
      content = byte_content.read()
      content = WebsiteTitleGrabber.detect_decoding(content)
      page_title = re.findall(r'<title>(.*?)</title>',content,re.DOTALL)
      if len(page_title) == 0:
        page_title = ['Dieser Link besitzt kein title tag! :)']
      page_title = ' '.join(page_title[0].split())
    except:
      return "Die URL %s ist irgendwie komisch!" % url
    
    uid = WebsiteTitleGrabber.save_url(url,page_title,message,nick)
    return page_title + " (!link "+str(uid)+")"

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
  Check duplicated URL
  returns boolean, uid, page title, message, user, time
  """
  def check_duplicated(url):
    data = DatabaseLayer.search_duplicated(url)
    if data != None:
      return True, data[0], data[1], data[2], data[3], data[4]
    else:
      return False, None, None, None, None, None
  """
   Save URL in Database
  """
  def save_url(url,url_page_title,message,user):
    return DatabaseLayer.insert(url,url_page_title,message,user)

  def help():
    pass

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
