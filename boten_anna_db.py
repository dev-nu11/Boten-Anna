import sqlite3

class boten_anna_db:

  # Constructor
  def __init__(self):
    self.conn = sqlite3.connect('boten_anna.db')

  def insert(self, links, page_title, message, user):
    c = self.conn.cursor()
    data = (links, page_title, message, user)
    id = c.execute('insert into urls (url,page_title,message,user) values (?, ?, ?, ?)', data)
    self.conn.commit()
    return c.lastrowid

  def get_links(self):
    c = self.conn.cursor()
    return c.execute('select * from urls').fetchall()

  def search_uid(self,uid):
    c = self.conn.cursor()
    return c.execute('select url,page_title,message,user from urls where uid=?', (uid,)).fetchone()

  def search_duplicated(self,url):
    c = self.conn.cursor()
    return c.execute('select uid,page_title,message,user,timestamp from urls where url=?', (url,)).fetchone()

  # Destructor
  def __del__(self):
    c = self.conn.cursor()
    c.close()
