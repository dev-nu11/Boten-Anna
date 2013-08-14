import sqlite3

class boten_anna_db:
    """
    Boten Anna DB, SQLITE3 Database Interface,
    provides functions for create, insert, select and search statements
    """

    def __init__(self,database,table,columns):
        """
        Constructor
        :param str  database: sqlite3 filename
        :param str  table: name of the new table
        :param list columns: list of columns
        """
        self.conn = sqlite3.connect(database,check_same_thread=False)
        self.create_table(table,columns)


    def create_table(self,table,columns):
        """
        Creates a new table if not exists
        :param str  table: name of the new table
        :param list columns: columns which should be created
        """ 
        if table == None or columns == None:
            return False
        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + table  + '('+ ','.join(columns) + ')')
        return self.conn.commit()

    def insert(self,fields,table,data):
        """
        Insert data in given table
        :param list fields: name of fields in which data should be inserted
        :param str  table: name of the table
        :param list data: data / values for fields
        """
        if fields == None or table == None:
            return False    

        c = self.conn.cursor()
        id = c.execute('insert into '+table+' ('+','.join(fields)+') values '+ self.__generate_values(len(data)), data)
        self.conn.commit()
        return c.lastrowid

    def select(self,fields,table,fetchall=True):
        """
        Select data in given table
        :param list fields: name of fields
        :param str  table: name of the table
        :param bool fetchall: returns the result of all found data or returns only the first result?
        """
        if fields == None or table == None:
            return False

        c = self.conn.cursor()
        query = c.execute('select '+','.join(fields)+' from '+table)

        if fetchall:
            return query.fetchall()
        else:
            return query.fetchone()

    def search(self,fields,table,search_param, data,fetchall=False):
        """
        Search data in given table
        :param list fields: name of fields which should selected 
        :param str  table: name of the table
        :param str  search_param: python sqlite3 param search (example: 'uid=?')
        :param list data: data which fill the search_param placeholders with data
        :param bool fetchall: returns the result of all found data or returns only the first result?
        """
        if fields == None or table == None:
            return False    

        c = self.conn.cursor()
        query = c.execute('select '+','.join(fields)+' from '+table+' where ' + search_param,data)

        if fetchall:
            return query.fetchall()
        else:
            return query.fetchone()

    """
    Help function to generate values placeholder for given fields (?,?,?) 
    :param int size: How many placeholders should I create, sir?
    """
    def __generate_values(self,size):
        values = "("
        for i in range(0,size-1):
            values +='?,'
        values += '?)' 
        return values

    """
    Destructor: Close db connection
    """
    def __del__(self):
        c = self.conn.cursor()
        c.close()
