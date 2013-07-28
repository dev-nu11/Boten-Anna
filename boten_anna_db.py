import sqlite3

class boten_anna_db:

  # Constructor
  def __init__(self):
    self.conn = sqlite3.connect('boten_anna.db')

  def insert(self, links, page_title, message, user):
    c = self.conn.cursor()
    data = (links, page_title, message, user)
    c.execute('insert into links (link,page_title,message,user) values (?, ?, ?, ?)', data)
    self.conn.commit()

  def get_links(self):
    c = self.conn.cursor()
    return c.execute('select * from links').fetchall()

  # Destructor
  def __del__(self):
    c = self.conn.cursor()
    c.close()
