import sqlite3

class boten_anna_db:

  # Constructor
  def __init__(self,database,table,columns):
    self.conn = sqlite3.connect(database,check_same_thread=False)
    self.__create_table(table,columns)

  def __create_table(self,table,columns):
    if table == None or columns == None:
      return False
    c = self.conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS ' + table  + '('+ ','.join(columns) + ')')
    return self.conn.commit()
   
  def insert(self,fields,table,data):
    if fields == None or table == None:
      return False    
    c = self.conn.cursor()
    id = c.execute('insert into '+table+' ('+','.join(fields)+') values '+ self.__generate_values(len(data)), data)
    self.conn.commit()
    return c.lastrowid

  def select(self,fields,table,fetchall=True):
    if fields == None or table == None:
      return False
    c = self.conn.cursor()
    query = c.execute('select '+','.join(fields)+' from '+table)
    if fetchall:
      return query.fetchall()
    else:
      return query.fetchone()

  def search(self,fields,table,search_param, data,fetchall=False):
    if fields == None or table == None:
      return False    
    c = self.conn.cursor()
    query = c.execute('select '+','.join(fields)+' from '+table+' where ' + search_param,data)
    if fetchall:
      return query.fetchall()
    else:
      return query.fetchone()

  def __generate_values(self,size):
    values = "("
    for i in range(0,size-1):
      values +='?,'
    values += '?)' 
    return values

  # Destructor
  def __del__(self):
    c = self.conn.cursor()
    c.close()
